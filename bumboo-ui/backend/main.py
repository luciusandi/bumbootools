"""Lightweight FastAPI app to expose scraped price data."""

from __future__ import annotations

import os
import glob
import json
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import re

try:
    from supabase import create_client
except Exception:
    create_client = None  # type: ignore

# load environment from .env if present
load_dotenv()


def _parse_iso_datetime(value: str) -> datetime | None:
    """Robustly parse various ISO datetime strings into datetime.
    Returns None if parsing fails.
    """
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    s = value.strip()
    # handle trailing Z as UTC
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    # try fromisoformat first
    try:
        return datetime.fromisoformat(s)
    except Exception:
        pass
    # normalize timezone like +00:00 -> +0000 for strptime %z
    tz_match = re.search(r"([+-]\d{2}):(\d{2})$", s)
    s2 = s
    if tz_match:
        s2 = s[: tz_match.start(1)] + tz_match.group(1) + tz_match.group(2)
    # try common strptime formats
    formats = [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S.%f%z",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S",
    ]
    for fm in formats:
        try:
            return datetime.strptime(s2, fm)
        except Exception:
            continue
    return None

APP = FastAPI(title="Bumboo API")
APP.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SUPA_URL = os.getenv("SUPABASE_URL")
SUPA_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPA_CLIENT = None
if SUPA_URL and SUPA_KEY and create_client:
    try:
        SUPA_CLIENT = create_client(SUPA_URL, SUPA_KEY)
    except Exception:
        SUPA_CLIENT = None

# Basic auth using environment credentials
SECURITY = HTTPBasic()
API_USER = os.getenv("API_USER")
API_PASS = os.getenv("API_PASS")


def require_auth(credentials: HTTPBasicCredentials = Depends(SECURITY)) -> None:
    if not API_USER or not API_PASS:
        raise HTTPException(status_code=500, detail="API_USER/API_PASS not configured")
    valid_user = secrets.compare_digest(credentials.username, API_USER)
    valid_pass = secrets.compare_digest(credentials.password, API_PASS)
    if not (valid_user and valid_pass):
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"WWW-Authenticate": "Basic"})


class PriceRow(BaseModel):
    brand: str
    description: str
    site: str
    size: str | None
    ply: str | None
    price: float | None
    total_reviews: int | None
    total_rating: float | None
    source_url: str
    metadata: dict[str, Any] | None
    collected_at: str


def _load_latest_json() -> list[dict[str, Any]]:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../bumboo-scraper/data/raw"))
    pattern = os.path.join(root, "scrape_*.json")
    files = glob.glob(pattern)
    if not files:
        return []
    latest = max(files, key=os.path.getmtime)
    with open(latest, "r", encoding="utf-8") as fh:
        return json.load(fh)


@APP.get("/api/health")
def health(credentials: HTTPBasicCredentials = Depends(SECURITY)):
    # allow health only if auth configured and valid
    require_auth(credentials)
    return {"ok": True, "supabase": bool(SUPA_CLIENT)}


@APP.get("/api/prices", response_model=list[PriceRow])
def prices(
    brand: str | None = Query(None),
    site: str | None = Query(None),
    date: str | None = Query(None, description="YYYY-MM-DD (UTC)"),
    limit: int = Query(500, ge=1, le=5000),
    credentials: HTTPBasicCredentials = Depends(SECURITY),
) -> list[PriceRow]:
    require_auth(credentials)
    # Prefer Supabase if configured
    if SUPA_CLIENT:
        table = SUPA_CLIENT.table("tissue_prices")
        query = table.select("*")
        if brand:
            query = query.eq("brand", brand)
        if site:
            query = query.eq("site", site)
        if date:
            try:
                d = datetime.fromisoformat(date)
            except Exception:
                # accept YYYY-MM-DD
                d = datetime.fromisoformat(date + "T00:00:00")
            start = d.replace(tzinfo=timezone.utc).isoformat()
            end = (d + timedelta(days=1)).replace(tzinfo=timezone.utc).isoformat()
            query = query.gte("collected_at", start).lt("collected_at", end)
        try:
            resp = query.limit(limit).execute()
            data = getattr(resp, "data", None) or resp[0] if isinstance(resp, (list, tuple)) else resp
            if isinstance(data, dict) and "data" in data:
                rows = data["data"]
            else:
                rows = data or []
            return [PriceRow(**r) for r in rows]
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

    # Fallback to latest local JSON
    rows = _load_latest_json()
    if not rows:
        return []
    filtered = []
    for r in rows:
        if brand and r.get("brand") != brand:
            continue
        if site and r.get("site") != site:
            continue
        if date:
            ca = r.get("collected_at")
            try:
                dt = datetime.fromisoformat(ca)
            except Exception:
                continue
            if dt.date().isoformat() != date:
                continue
        filtered.append(r)
        if len(filtered) >= limit:
            break
    return [PriceRow(**r) for r in filtered]


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:APP", host="0.0.0.0", port=port, log_level="info")


@APP.get("/api/products")
def products(
    brand: str | None = Query(None),
    site: str | None = Query(None),
    days: int = Query(30, ge=1, le=365),
    credentials: HTTPBasicCredentials = Depends(SECURITY),
):
    """Aggregate products (brand+description+site) over the past `days` days."""
    require_auth(credentials)
    now = datetime.now(timezone.utc)
    start_dt = now - timedelta(days=days)
    start = start_dt.isoformat()
    end = now.isoformat()

    rows = []
    if SUPA_CLIENT:
        try:
            resp = SUPA_CLIENT.table("tissue_prices").select("*").gte("collected_at", start).lt("collected_at", end).execute()
            # normalize response: try .data, then dict["data"], then list
            if hasattr(resp, "data"):
                rows = resp.data or []
            elif isinstance(resp, dict) and "data" in resp:
                rows = resp["data"] or []
            elif isinstance(resp, (list, tuple)):
                # some clients return (data, count)
                rows = list(resp[0]) if resp and isinstance(resp[0], list) else list(resp)
            else:
                rows = []
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
    else:
        # load local files
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../bumboo-scraper/data/raw"))
        files = sorted(glob.glob(os.path.join(root, "scrape_*.json")))
        for f in files:
            with open(f, "r", encoding="utf-8") as fh:
                try:
                    items = json.load(fh)
                except Exception:
                    continue
                for it in items:
                    ca = it.get("collected_at")
                    try:
                        dt = _parse_iso_datetime(ca)
                        if dt is None:
                            continue
                    except Exception:
                        continue
                    if dt.replace(tzinfo=timezone.utc) >= start_dt and dt.replace(tzinfo=timezone.utc) <= now:
                        rows.append(it)

    # apply filters
    filtered = []
    for r in rows:
        if brand and r.get("brand") != brand:
            continue
        if site and r.get("site") != site:
            continue
        filtered.append(r)

    # aggregate by (brand, description, size) — group across sites
    agg = {}
    for r in filtered:
        key = (r.get("brand"), r.get("description"), r.get("size"))
        price = r.get("price")
        ca = r.get("collected_at")
        if key not in agg:
            agg[key] = {
                "brand": key[0],
                "description": key[1],
                "size": key[2],
                "count": 0,
                "sites": set(),
                "prices": [],
                "latest_price": None,
                "latest_ts": None,
            }
        a = agg[key]
        a["count"] += 1
        site = r.get("site")
        if site:
            a["sites"].add(site)
        if isinstance(price, (int, float)):
            a["prices"].append(float(price))
        # latest across sites
        try:
            ts = _parse_iso_datetime(ca)
            if ts is not None and (a["latest_ts"] is None or ts > a["latest_ts"]):
                a["latest_ts"] = ts
                a["latest_price"] = price
        except Exception:
            pass

    out = []
    for k, v in agg.items():
        prices = v["prices"]
        out.append({
            "brand": v["brand"],
            "description": v["description"],
            "size": v["size"],
            "sites": list(v["sites"]),
            "sites_count": len(v["sites"]),
            "image": "/static/placeholder.jpg",
            "count": v["count"],
            "avg_price": sum(prices)/len(prices) if prices else None,
            "min_price": min(prices) if prices else None,
            "max_price": max(prices) if prices else None,
            "latest_price": v["latest_price"],
        })
    return out


@APP.get("/api/price-history")
def price_history(
    brand: str = Query(...),
    description: str = Query(...),
    site: str | None = Query(None),
    days: int = Query(30, ge=1, le=365),
    credentials: HTTPBasicCredentials = Depends(SECURITY),
):
    """Return daily aggregated price history for the selected product."""
    require_auth(credentials)
    now = datetime.now(timezone.utc)
    start_dt = now - timedelta(days=days)
    start = start_dt.isoformat()
    end = now.isoformat()

    rows = []
    if SUPA_CLIENT:
        try:
            resp = SUPA_CLIENT.table("tissue_prices").select("*").gte("collected_at", start).lt("collected_at", end).execute()
            if hasattr(resp, "data"):
                rows = resp.data or []
            elif isinstance(resp, dict) and "data" in resp:
                rows = resp["data"] or []
            elif isinstance(resp, (list, tuple)):
                rows = list(resp[0]) if resp and isinstance(resp[0], list) else list(resp)
            else:
                rows = []
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))
    else:
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../bumboo-scraper/data/raw"))
        files = sorted(glob.glob(os.path.join(root, "scrape_*.json")))
        for f in files:
            with open(f, "r", encoding="utf-8") as fh:
                try:
                    items = json.load(fh)
                except Exception:
                    continue
                for it in items:
                    ca = it.get("collected_at")
                    try:
                        dt = _parse_iso_datetime(ca)
                        if dt is None:
                            continue
                    except Exception:
                        continue
                    if dt.replace(tzinfo=timezone.utc) >= start_dt and dt.replace(tzinfo=timezone.utc) <= now:
                        rows.append(it)

    # filter and bucket by date
    # filter and bucket by date and site
    # buckets[date][site] = [prices...]
    buckets: dict[str, dict[str, list[float]]] = {}
    for r in rows:
        if r.get("brand") != brand:
            continue
        if r.get("description") != description:
            continue
        if site and r.get("site") != site:
            continue
        ca = r.get("collected_at")
        dt_obj = _parse_iso_datetime(ca)
        if not dt_obj:
            continue
        dt = dt_obj.date().isoformat()
        price = r.get("price")
        if price is None:
            continue
        site_name = (r.get("site") or "unknown").strip()
        buckets.setdefault(dt, {}).setdefault(site_name, []).append(float(price))

    # helper map site name to canonical fields used by frontend
    def site_field(site_name: str) -> str | None:
        s = (site_name or "").lower().strip()
        # normalize common variants
        s_norm = s.replace("-", " ").replace("_", " ")
        # explicit checks for known vendors
        if any(tok in s_norm for tok in ("fairprice", "fair price", "fair", "FairPrice")):
            return "fairprice"
        if any(tok in s_norm for tok in ("coldstorage", "cold storage", "cold")):
            return "coldStorage"
        if any(tok in s_norm for tok in ("redmart", "red mart", "red", "lazada", "lzd")):
            return "redmart"
        return None

    # build time series per day with per-site aggregates
    out: list[dict[str, object]] = []
    for i in range(days + 1):
        day = (start_dt + timedelta(days=i)).date().isoformat()
        per_site = buckets.get(day, {})
        entry: dict[str, object] = {"date": day, "count": 0}
        # initialize fields
        entry["fairprice"] = None
        entry["coldStorage"] = None
        entry["redmart"] = None
        total_count = 0
        for site_name, prices in per_site.items():
            fld = site_field(site_name)
            avg = sum(prices) / len(prices) if prices else None
            if fld:
                entry[fld] = avg
            total_count += len(prices)
        entry["count"] = total_count
        # only include days that have at least one price record
        if total_count > 0:
            out.append(entry)
    return out


