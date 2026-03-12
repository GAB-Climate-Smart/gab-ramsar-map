-- Enable PostGIS for geometry support
create extension if not exists postgis with schema extensions;

-- ============================================================
-- user_features: stores user-drawn points and polygons
-- ============================================================
create table public.user_features (
    id              uuid primary key default gen_random_uuid(),
    name            text not null,
    description     text,
    feature_type    text not null check (feature_type in ('point', 'polygon')),
    geojson         jsonb not null,
    area_hectares   numeric(12, 4),
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);

alter table public.user_features enable row level security;

-- Allow anonymous reads and writes (public map - no auth required)
create policy "Public read user_features"
    on public.user_features for select using (true);

create policy "Public insert user_features"
    on public.user_features for insert with check (true);

create policy "Public delete user_features"
    on public.user_features for delete using (true);

-- ============================================================
-- coastal_ecosystem_features: coastal data layer (admin-populated)
-- ============================================================
create table public.coastal_ecosystem_features (
    id              uuid primary key default gen_random_uuid(),
    name            text not null,
    description     text,
    feature_type    text not null check (feature_type in ('point', 'polygon')),
    geojson         jsonb not null,
    ecosystem_type  text,   -- e.g. 'seagrass', 'saltmarsh', 'tidal flat', 'coral'
    site            text,   -- e.g. 'Keta', 'Ada/Songor'
    area_hectares   numeric(12, 4),
    source          text,
    created_at      timestamptz not null default now()
);

alter table public.coastal_ecosystem_features enable row level security;

create policy "Public read coastal_ecosystem_features"
    on public.coastal_ecosystem_features for select using (true);

-- Trigger to auto-update updated_at on user_features
create or replace function public.handle_updated_at()
returns trigger language plpgsql as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

create trigger user_features_updated_at
    before update on public.user_features
    for each row execute procedure public.handle_updated_at();

-- Indexes
create index idx_user_features_type on public.user_features(feature_type);
create index idx_user_features_created on public.user_features(created_at desc);
create index idx_coastal_features_site on public.coastal_ecosystem_features(site);
create index idx_coastal_features_type on public.coastal_ecosystem_features(ecosystem_type);
