#!/usr/bin/env python3
"""
NDVI Monitoring Script — GAB Ramsar Map
Fetches latest Sentinel-2 L2A scene from Element84 Earth Search STAC,
computes NDVI per drone AOI, and stores results in Supabase ndvi_snapshots.
"""

import os
import sys
import json
import datetime
import warnings
import numpy as np
import requests

import rasterio
from rasterio.mask import mask as rio_mask
from rasterio.crs import CRS
from rasterio.warp import transform_geom
import pystac_client
from shapely.geometry import shape, mapping
from supabase import create_client, Client

warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)

# ─── Config ────────────────────────────────────────────────────────────────
SUPABASE_URL             = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_ROLE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

STAC_API_URL = "https://earth-search.aws.element84.com/v1"
COLLECTION   = "sentinel-2-l2a"

# Bounding box covering all four drone AOIs (Keta Lagoon region, Ghana)
STUDY_BBOX = [0.59, 5.77, 1.15, 6.13]

# Max cloud cover % to accept a scene
MAX_CLOUD   = 30

# Alert thresholds (change from 90-day baseline)
THRESH_CRITICAL = -0.20
THRESH_WARNING  = -0.10

# ─── Drone AOI Polygons (GeoJSON, WGS84) ───────────────────────────────────
DRONE_AOIS = [
    {
        "name": "Agatsivi-Agortoe Stretch",
        "area_ha": 762,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [0.730589,5.831254],[0.729559,5.831212],[0.729258,5.832166],[0.72843,5.834068],
                [0.727558,5.834068],[0.726429,5.835191],[0.725472,5.837437],[0.724301,5.837823],
                [0.723259,5.838595],[0.722603,5.840069],[0.722131,5.841371],[0.721445,5.841971],
                [0.720932,5.843188],[0.720589,5.844791],[0.720246,5.847033],[0.720332,5.850277],
                [0.720975,5.856591],[0.721832,5.859491],[0.72297,5.863706],[0.723699,5.866177],
                [0.724514,5.868262],[0.725558,5.869948],[0.726558,5.870948],[0.727558,5.871305],
                [0.729387,5.871305],[0.730687,5.870219],[0.731602,5.868605],[0.732816,5.866905],
                [0.734244,5.864662],[0.735015,5.861805],[0.735015,5.858948],[0.734501,5.856434],
                [0.733458,5.853920],[0.733072,5.851406],[0.733201,5.848892],[0.733330,5.845949],
                [0.733330,5.843006],[0.733072,5.840320],[0.732172,5.837848],[0.731487,5.835377],
                [0.731144,5.833334],[0.730589,5.831254]
            ]]
        }
    },
    {
        "name": "Salo-Agortoe Stretch",
        "area_ha": 525,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [0.755739,5.826254],[0.754625,5.826997],[0.753168,5.828683],[0.751711,5.830797],
                [0.750683,5.833168],[0.750083,5.835968],[0.749997,5.838768],[0.750340,5.841568],
                [0.751197,5.844454],[0.752397,5.847083],[0.753940,5.849454],[0.755482,5.851397],
                [0.757082,5.852911],[0.759025,5.854768],[0.761054,5.855882],[0.763169,5.856425],
                [0.765283,5.856254],[0.767054,5.855140],[0.768311,5.853311],[0.768997,5.851225],
                [0.769340,5.848968],[0.769083,5.846625],[0.768311,5.844368],[0.767025,5.842111],
                [0.765397,5.840025],[0.763597,5.838111],[0.761711,5.836454],[0.759826,5.834883],
                [0.758254,5.833311],[0.757082,5.831654],[0.756340,5.829654],[0.755739,5.826254]
            ]]
        }
    },
    {
        "name": "Anyanui Combine System",
        "area_ha": 128,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [0.71557,5.795081],[0.717545,5.80029],[0.718918,5.800375],[0.719347,5.801656],
                [0.720162,5.801912],[0.723252,5.801742],[0.72454,5.797899],[0.725355,5.793416],
                [0.726256,5.789274],[0.72381,5.784407],[0.721922,5.784791],[0.721793,5.786584],
                [0.720763,5.787908],[0.719905,5.790171],[0.719562,5.792348],[0.718532,5.793928],
                [0.71557,5.795081]
            ]]
        }
    },
    {
        "name": "Aborlove Nolopi Mangrove",
        "area_ha": 52,
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [0.930877,6.038352],[0.934224,6.041767],[0.93652,6.041212],[0.936649,6.040017],
                [0.939202,6.039675],[0.939095,6.038374],[0.937335,6.038288],[0.936584,6.037798],
                [0.934653,6.034661],[0.934181,6.034021],[0.932336,6.032762],[0.930941,6.032698],
                [0.929739,6.034746],[0.931113,6.036347],[0.930877,6.038352]
            ]]
        }
    }
]


# ─── STAC Search ────────────────────────────────────────────────────────────

def find_best_scene(days_back: int = 30) -> object | None:
    """Search for the most recent cloud-free Sentinel-2 L2A scene."""
    catalog = pystac_client.Client.open(STAC_API_URL)
    end_dt   = datetime.datetime.utcnow()
    start_dt = end_dt - datetime.timedelta(days=days_back)
    date_range = f"{start_dt.strftime('%Y-%m-%dT%H:%M:%SZ')}/{end_dt.strftime('%Y-%m-%dT%H:%M:%SZ')}"

    results = catalog.search(
        collections=[COLLECTION],
        bbox=STUDY_BBOX,
        datetime=date_range,
        query={"eo:cloud_cover": {"lt": MAX_CLOUD}},
        sortby=["-datetime"],
        max_items=10
    )

    items = list(results.items())
    if not items:
        print(f"No scenes found with cloud cover < {MAX_CLOUD}% in the last {days_back} days.")
        return None

    # Return scene with lowest cloud cover
    best = sorted(items, key=lambda i: i.properties.get("eo:cloud_cover", 100))[0]
    print(f"Best scene: {best.id}  date={best.datetime.date()}  cloud={best.properties.get('eo:cloud_cover', '?')}%")
    return best


# ─── Band Reading & NDVI ─────────────────────────────────────────────────────

def read_band_href(href: str) -> tuple:
    """Open a rasterio dataset from an HTTPS COG href."""
    env = rasterio.Env(
        GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
        CPL_VSIL_CURL_ALLOWED_EXTENSIONS="tif,tiff",
        GDAL_HTTP_UNSAFESSL="YES",
    )
    with env:
        ds = rasterio.open(href)
    return ds


def compute_ndvi_for_aoi(red_href: str, nir_href: str, aoi_geom: dict) -> dict | None:
    """
    Mask both bands to the AOI polygon, compute NDVI pixel stats.
    Returns dict with mean/min/max/std or None on failure.
    """
    try:
        env = rasterio.Env(
            GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
            CPL_VSIL_CURL_ALLOWED_EXTENSIONS="tif,tiff",
            GDAL_HTTP_UNSAFESSL="YES",
            GDAL_HTTP_MERGE_CONSECUTIVE_RANGES="YES",
        )
        with env:
            with rasterio.open(red_href) as red_ds, rasterio.open(nir_href) as nir_ds:
                # Reproject AOI geometry to match raster CRS
                raster_crs = red_ds.crs
                wgs84_crs  = CRS.from_epsg(4326)

                if raster_crs != wgs84_crs:
                    aoi_projected = transform_geom(
                        src_crs=wgs84_crs,
                        dst_crs=raster_crs,
                        geom=aoi_geom
                    )
                else:
                    aoi_projected = aoi_geom

                shapes = [aoi_projected]

                red_data, _ = rio_mask(red_ds, shapes, crop=True, nodata=0)
                nir_data, _ = rio_mask(nir_ds, shapes, crop=True, nodata=0)

                red = red_data[0].astype(np.float32)
                nir = nir_data[0].astype(np.float32)

                # Mask nodata (0) and saturated (65535) pixels
                valid = (red > 0) & (nir > 0) & (red < 65535) & (nir < 65535)
                if valid.sum() < 10:
                    print("  Warning: too few valid pixels after masking")
                    return None

                red_v = red[valid]
                nir_v = nir[valid]

                denominator = nir_v + red_v
                # Avoid division by zero
                safe = denominator != 0
                ndvi = np.full_like(red_v, np.nan)
                ndvi[safe] = (nir_v[safe] - red_v[safe]) / denominator[safe]

                ndvi_valid = ndvi[~np.isnan(ndvi)]
                if len(ndvi_valid) == 0:
                    return None

                return {
                    "mean_ndvi": float(round(float(np.mean(ndvi_valid)), 4)),
                    "min_ndvi":  float(round(float(np.min(ndvi_valid)), 4)),
                    "max_ndvi":  float(round(float(np.max(ndvi_valid)), 4)),
                    "std_ndvi":  float(round(float(np.std(ndvi_valid)), 4)),
                }
    except Exception as e:
        print(f"  Error computing NDVI: {e}")
        return None


# ─── Baseline from Supabase ──────────────────────────────────────────────────

def get_90day_baseline(sb: Client, aoi_name: str) -> float | None:
    """Return mean NDVI over last 90 days for an AOI, or None if no data."""
    cutoff = (datetime.date.today() - datetime.timedelta(days=90)).isoformat()
    resp = sb.table("ndvi_snapshots") \
             .select("mean_ndvi") \
             .eq("aoi_name", aoi_name) \
             .gte("observed_date", cutoff) \
             .execute()
    rows = resp.data or []
    if not rows:
        return None
    vals = [float(r["mean_ndvi"]) for r in rows if r["mean_ndvi"] is not None]
    return round(float(np.mean(vals)), 4) if vals else None


# ─── Alert Level ─────────────────────────────────────────────────────────────

def determine_alert(ndvi_change: float | None) -> str:
    if ndvi_change is None:
        return "normal"
    if ndvi_change < THRESH_CRITICAL:
        return "critical"
    if ndvi_change < THRESH_WARNING:
        return "warning"
    return "normal"


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    print("=== GAB Ramsar NDVI Monitor ===")
    print(f"Run date: {datetime.date.today().isoformat()}")

    # Connect to Supabase
    sb: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

    # Find best scene (try last 30 days, fallback to 60)
    scene = find_best_scene(days_back=30)
    if scene is None:
        scene = find_best_scene(days_back=60)
    if scene is None:
        print("ERROR: No suitable Sentinel-2 scene found. Exiting.")
        sys.exit(1)

    observed_date = scene.datetime.date().isoformat()
    scene_id      = scene.id
    cloud_cover   = scene.properties.get("eo:cloud_cover", None)

    # Get band hrefs
    assets = scene.assets
    red_href = assets.get("red", assets.get("B04", None))
    nir_href = assets.get("nir", assets.get("B08", None))

    if red_href is None or nir_href is None:
        print(f"ERROR: Could not find red/nir assets. Available: {list(assets.keys())}")
        sys.exit(1)

    # Handle pystac asset objects vs plain dicts
    red_url = red_href.href if hasattr(red_href, "href") else red_href
    nir_url = nir_href.href if hasattr(nir_href, "href") else nir_href

    print(f"Red band: {red_url[:80]}...")
    print(f"NIR band: {nir_url[:80]}...")

    records = []
    for aoi in DRONE_AOIS:
        print(f"\nProcessing AOI: {aoi['name']}")
        stats = compute_ndvi_for_aoi(red_url, nir_url, aoi["geometry"])

        if stats is None:
            print(f"  Skipping {aoi['name']} — no valid NDVI data")
            continue

        print(f"  mean_ndvi={stats['mean_ndvi']}  min={stats['min_ndvi']}  max={stats['max_ndvi']}  std={stats['std_ndvi']}")

        # Baseline comparison
        baseline = get_90day_baseline(sb, aoi["name"])
        ndvi_change = None
        if baseline is not None:
            ndvi_change = round(stats["mean_ndvi"] - baseline, 4)
            print(f"  baseline={baseline}  change={ndvi_change:+.4f}")
        else:
            print("  No baseline data yet (first run)")

        alert = determine_alert(ndvi_change)
        print(f"  alert_level={alert}")

        records.append({
            "observed_date": observed_date,
            "aoi_name":      aoi["name"],
            "mean_ndvi":     stats["mean_ndvi"],
            "min_ndvi":      stats["min_ndvi"],
            "max_ndvi":      stats["max_ndvi"],
            "std_ndvi":      stats["std_ndvi"],
            "cloud_cover":   round(float(cloud_cover), 2) if cloud_cover is not None else None,
            "alert_level":   alert,
            "baseline_ndvi": baseline,
            "ndvi_change":   ndvi_change,
            "scene_id":      scene_id,
        })

    if not records:
        print("\nNo records to insert. Exiting.")
        sys.exit(0)

    print(f"\nInserting {len(records)} records into ndvi_snapshots...")
    resp = sb.table("ndvi_snapshots").insert(records).execute()
    print(f"Inserted: {len(resp.data)} rows")

    # Print summary
    print("\n=== Summary ===")
    for r in records:
        flag = "ALERT" if r["alert_level"] != "normal" else "OK"
        change_str = f"{r['ndvi_change']:+.4f}" if r["ndvi_change"] is not None else "N/A"
        print(f"  [{flag}] {r['aoi_name']}: NDVI={r['mean_ndvi']} change={change_str} ({r['alert_level']})")

    print("\nDone.")


if __name__ == "__main__":
    main()
