# Bumboo UI

Lightweight dashboard repo for the Bumboo price-watch pipeline. This folder contains a Next.js frontend and a small FastAPI backend that exposes scraped price data (from the `bumboo-scraper` pipeline or Supabase).

Contents
- `app/`, `components/`, `public/`, `styles/` — frontend application (Next.js).
- `backend/` — FastAPI app that serves `/api/prices` and `/api/health`.

Quick start

1) Prepare a Python venv (shared with the scraper or separate)

```bash
cd /Users/lucius/www/bumboo/bumboo-ui/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from the example and set credentials:

```env
SUPABASE_URL="https://<your>.supabase.co"
SUPABASE_SERVICE_ROLE_KEY="<service-role-key>"
API_USER="admin"
API_PASS="change-me"
PORT=8000
```

Run the backend:

```bash
uvicorn main:APP --reload --port 8000
```

Endpoints
- `GET /api/health` — requires Basic auth (see `.env`).
- `GET /api/prices?brand=&site=&date=YYYY-MM-DD&limit=NN` — returns list of price rows (requires Basic auth). If Supabase is configured backend will query the `tissue_prices` table; otherwise it falls back to the latest JSON snapshot produced by the scraper pipeline.

2) Frontend (Next.js)

The frontend lives at the project root. Install and run it with your package manager:

```bash
# from /Users/lucius/www/bumboo/bumboo-ui
# using pnpm (preferred if present)
pnpm install
pnpm dev

# or npm
npm install
npm run dev
```

If the frontend is served from a different origin than the backend, update the fetch URL in `frontend` or proxy `/api` to the backend host. The simple sample frontend included in the repo is a tiny static page that calls `/api/prices` (it expects Basic auth).

Security note
- The backend uses HTTP Basic auth backed by `API_USER` / `API_PASS` in the env for now — do not commit these values to git. We can switch to token auth or cookie sessions later.

Daily runs and reporting
- The scraper runner writes `collected_at` timestamps. For daily reports group by `date(collected_at)` in SQL or use a generated `collected_date` column:

```sql
ALTER TABLE public.tissue_prices
  ADD COLUMN collected_date date GENERATED ALWAYS AS (date(collected_at)) STORED;
```

FAQ / next steps
- Serve the frontend from the FastAPI app via static files (I can add that).
- Add Dockerfiles for backend/frontend for easier deployment.
- Add simple charts to the frontend (I can scaffold a small chart using Chart.js or similar).

If you'd like, I can:
- Mount the frontend under `backend/` static files and add a simple login UI, or
- Add a CI workflow to deploy nightly scrapes and refresh the dashboard.


