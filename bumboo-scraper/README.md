# Bumboo Price Watch

Pipeline for scraping toilet paper prices, persisting them to Supabase, and
feeding a (future) dashboard.

## 1. Install dependencies

```bash
cd /Users/lucius/www/bumboo/bumboo-scraper
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2. Configure Supabase

1. Copy `env.example` to `.env` and fill in your Supabase project URL and
   service role key (service key avoids RLS headaches per request).
2. Create the target table (default name `tissue_prices`):

```sql
create table public.tissue_prices (
  id uuid primary key default gen_random_uuid(),
  brand varchar(200) not null,
  description text not null,
  site varchar(200) not null,
  size varchar(200),
  ply varchar(200),
  price numeric,
  total_reviews int,
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
```

Column lengths are capped at 200 chars where we plan to index so Postgres can
build efficient b-tree indexes without extra work. Adjust numeric types
(e.g., switch to `float8`) whenever you prefer.

## 3. Run the scrapers

```bash
python -m scrapers.runner
# or target a specific job
python -m scrapers.runner --jobs coldstorage-kleenex --skip-supabase --local-dump
# or run multiple Cold Storage brands at once
python -m scrapers.runner --jobs \
  coldstorage-kleenex coldstorage-nootrees coldstorage-paseo \
  coldstorage-pursoft coldstorage-vinda coldstorage-tempo \
  coldstorage-cloversoft --skip-supabase --local-dump
```

Key flags:

- `--jobs example other_site` &mdash; run only specific jobs.
- `--skip-supabase` &mdash; dry-run without writing to Supabase.
- `--local-dump` &mdash; always save a JSON snapshot under `data/raw/`.
- `--table custom_table` &mdash; target a different table name.

By default the runner will:

1. Load environment variables from `.env`.
2. Execute each registered job sequentially.
3. Upsert all records into Supabase (fallback to local JSON if credentials are
   missing or you pass `--skip-supabase`).

## 4. Adding a new site

1. Add or update the canonical product entry inside `scrapers/catalog.py`
   (brand, description, site, size, ply, and canonical URL).
2. Create a new module under `scrapers/` (e.g., `scrapers/target_store.py`).
3. Subclass `BaseScraper` and implement `_scrape`, returning
   `list[ProductRecord]`.
4. Register the scraper by adding a `ScrapeJob` entry (or generator) to
   `scrapers/registry.py` that reads from the catalog entry.
5. Run `python -m scrapers.runner --jobs your-job --skip-supabase --local-dump`
   to inspect the JSON output before enabling Supabase writes.

Each `ScrapeJob` lets you set the brand/description/site manually while keeping
the scraper logic focused on parsing the storefront HTML or API. The `options`
dictionary is a convenient place to pass site-specific knobs (CSS selectors,
API endpoints, etc.).

### Current job catalog

- `example` – static sample.
- `coldstorage-kleenex`
- `coldstorage-nootrees`
- `coldstorage-paseo`
- `coldstorage-pursoft`
- `coldstorage-vinda`
- `coldstorage-tempo`
- `coldstorage-cloversoft`
- `fairprice-kleenex`
- `fairprice-paseo`
- `fairprice-pursoft`
- `fairprice-fairprice`
- `fairprice-beautex`
- `fairprice-neutra`
- `fairprice-cloversoft`
- `fairprice-nootrees`
- `fairprice-tempo`
- `redmart-tempo`
- `redmart-kleenex`
- `redmart-pursoft`
- `redmart-vinda`
- `redmart-beautex`
- `redmart-paseo`
- `redmart-cloversoft`
- `redmart-nootrees`

## 5. Dashboard stub (coming soon)

Once the scraping layer is finalized we can scaffold a lightweight dashboard
(Next.js, SvelteKit, or similar) that queries Supabase and shows:

- Current prices by brand / store
- Historical trends (line charts)
- Review volume & rating comparisons

Because the data already lives in Supabase, the dashboard can connect via
Supabase REST or directly through a serverless function.

## Repository layout

```
scrapers/
  base.py         # shared HTTP helpers
  catalog.py      # hardcoded mapping of brand/site targets
  coldstorage.py  # Cold Storage category listings scraper
  example.py      # placeholder scraper, replace with real ones
  models.py       # dataclasses for jobs and product records
  registry.py     # declares jobs available to the runner
  runner.py       # CLI entry-point
  storage.py      # Supabase + JSON persistence
requirements.txt  # python dependencies
env.example       # copy to .env and fill in secrets
```

## Run Scrapers

0 3 * * * cd /Users/lucius/www/bumboo/bumboo-scraper && /Users/lucius/www/bumboo/bumboo-scraper/.venv/bin/python -m scrapers.runner --jobs ... --local-dump >> logs/scraper.log 2>&1

cd /Users/lucius/www/bumboo/bumboo-scraper
source .venv/bin/activate
python -m scrapers.runner --jobs \
  coldstorage-kleenex coldstorage-nootrees coldstorage-paseo \
  coldstorage-pursoft coldstorage-vinda coldstorage-tempo coldstorage-cloversoft \
  fairprice-kleenex fairprice-paseo fairprice-pursoft fairprice-fairprice \
  fairprice-beautex fairprice-neutra fairprice-cloversoft fairprice-nootrees fairprice-tempo \
  redmart-tempo redmart-kleenex redmart-pursoft redmart-vinda \
  redmart-beautex redmart-paseo redmart-cloversoft redmart-nootrees \
  --local-dump --table tissue_prices