"""Scraper for RedMart brand listings (Lazada JSON endpoint)."""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin, urlparse, parse_qsl, urlunparse

import urllib3

from .base import BaseScraper
from .models import ProductRecord

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RedMartBrandScraper(BaseScraper):
    """Parses RedMart brand pages that return JSON when `ajax=true` is set."""

    HOST = "https://redmart.lazada.sg"
    PLY_PATTERN = re.compile(r"(\d+)\s*-\s*ply|(\d+)\s*ply", re.IGNORECASE)
    SIZE_PATTERNS = [
        re.compile(r"(\d+\s*(?:x|X)\s*\d+\s*[^\s,]+)", re.IGNORECASE),
        re.compile(
            r"(\d+\s*(?:Rolls?|Sheets?|Boxes?|Packs?|pcs|Per\s+Pack))",
            re.IGNORECASE,
        ),
    ]

    def _scrape(self) -> list[ProductRecord]:
        url = self.job.options["api_url"]
        records: list[ProductRecord] = []
        seen_ids: set[str] = set()

        while url:
            response = self.fetch(url, headers=self._headers(), verify=False)
            payload = response.json()
            items = self._extract_items(payload)
            if not items:
                break

            for item in items:
                nid = item.get("nid") or item.get("itemId")
                if not nid or nid in seen_ids:
                    continue
                seen_ids.add(nid)
                records.append(self._to_record(item))

            url = self._next_url(payload)

        return records

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": self.session.headers.get("User-Agent", "Mozilla/5.0"),
        }

    def _extract_items(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        try:
            return payload["mods"]["listItems"]
        except (KeyError, TypeError):
            return []

    def _next_url(self, payload: dict[str, Any]) -> str | None:
        seo_info = payload.get("seoInfo") or {}
        next_href = seo_info.get("nextHref")
        if not next_href:
            main_info = payload.get("mainInfo") or {}
            if main_info.get("noMorePages"):
                return None
            return None
        parsed = urlparse(urljoin(self.HOST, next_href))
        query = dict(parse_qsl(parsed.query))
        query["ajax"] = "true"
        query.setdefault("m", "redmart")
        rebuilt = parsed._replace(query=urlencode(query))
        return urlunparse(rebuilt)

    def _to_record(self, item: dict[str, Any]) -> ProductRecord:
        name = (item.get("name") or "").strip()
        url = item.get("productUrl") or ""
        if url.startswith("//"):
            source_url = "https:" + url
        else:
            source_url = urljoin(self.HOST, url)

        price = self._parse_price(item.get("priceShow") or item.get("price"))
        rating = self._safe_float(item.get("ratingScore"))
        reviews = self._safe_int(item.get("review"))

        metadata = {
            "job_description": self.job.description,
            "raw_name": name,
            "price_display": item.get("priceShow"),
            "seller": item.get("sellerName"),
            "item_sold": item.get("itemSoldCntShow"),
            "description": item.get("description"),
            "badges": item.get("icons"),
            "categories": item.get("categories"),
            "package_info": item.get("packageInfo"),
        }

        return ProductRecord(
            brand=self.job.brand,
            description=name,
            site=self.job.site_name,
            size=self._extract_size(item),
            ply=self._extract_ply(name),
            price=price,
            total_reviews=reviews,
            total_rating=rating,
            source_url=source_url,
            metadata=metadata,
        )

    def _parse_price(self, value: str | float | None) -> float | None:
        if value is None:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        match = re.search(r"[\d.]+", value)
        if match:
            try:
                return float(match.group())
            except ValueError:
                return None
        return None

    def _extract_ply(self, text: str) -> str | None:
        if not text:
            return None
        match = self.PLY_PATTERN.search(text)
        if match:
            return next(filter(None, match.groups()))
        return None

    def _extract_size(self, item: dict[str, Any]) -> str | None:
        package_info = item.get("packageInfo")
        if package_info:
            return package_info
        name = item.get("name") or ""
        for pattern in self.SIZE_PATTERNS:
            match = pattern.search(name)
            if match:
                return match.group(1).strip()
        description = item.get("description") or []
        if isinstance(description, list):
            joined = " ".join(description)
            for pattern in self.SIZE_PATTERNS:
                match = pattern.search(joined)
                if match:
                    return match.group(1).strip()
        return None

    def _safe_float(self, value: Any) -> float | None:
        try:
            if value is None or value == "":
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    def _safe_int(self, value: Any) -> int | None:
        try:
            if value is None or value == "":
                return None
            return int(float(value))
        except (TypeError, ValueError):
            return None

