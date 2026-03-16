-- NDVI monitoring snapshots per AOI
create table public.ndvi_snapshots (
    id              uuid primary key default gen_random_uuid(),
    observed_date   date not null,
    aoi_name        text not null,
    mean_ndvi       numeric(6,4),
    min_ndvi        numeric(6,4),
    max_ndvi        numeric(6,4),
    std_ndvi        numeric(6,4),
    cloud_cover     numeric(5,2),
    alert_level     text not null default 'normal' check (alert_level in ('normal','warning','critical')),
    baseline_ndvi   numeric(6,4),
    ndvi_change     numeric(6,4),
    scene_id        text,
    created_at      timestamptz not null default now()
);

alter table public.ndvi_snapshots enable row level security;

create policy "Public read ndvi_snapshots"
    on public.ndvi_snapshots for select using (true);

create policy "Service role insert ndvi_snapshots"
    on public.ndvi_snapshots for insert with check (true);

create index idx_ndvi_snapshots_aoi_date on public.ndvi_snapshots(aoi_name, observed_date desc);
create index idx_ndvi_snapshots_date on public.ndvi_snapshots(observed_date desc);
