-- Schema for the price watch pipeline.
-- Run this in Supabase SQL editor (database exists already).

create table if not exists public.tissue_prices (
  id uuid primary key default gen_random_uuid(),
  brand varchar(200) not null,
  description text not null,
  site varchar(200) not null,
  size varchar(200),
  ply varchar(200),
  price numeric,
  total_reviews integer,
  total_rating numeric,
  source_url text not null,
  metadata jsonb,
  collected_at timestamptz not null default now()
);

create index if not exists tissue_prices_brand_desc_site_idx
  on public.tissue_prices (brand, description, site);

create index if not exists tissue_prices_brand_idx on public.tissue_prices (brand);
create index if not exists tissue_prices_site_idx on public.tissue_prices (site);
create index if not exists tissue_prices_size_idx on public.tissue_prices (size);
create index if not exists tissue_prices_ply_idx on public.tissue_prices (ply);

