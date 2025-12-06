"""Scraper for FairPrice category API (brand-filtered)."""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin, urlparse, urlunparse, parse_qsl

import urllib3

from .base import BaseScraper
from .models import ProductRecord

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FairPriceCategoryScraper(BaseScraper):
    """Hits the FairPrice category API and normalizes items."""

    PLY_PATTERN = re.compile(r"(\d+)\s*ply", re.IGNORECASE)

    def _scrape(self) -> list[ProductRecord]:
        template = self.job.options["api_url"]
        page = 1
        records: list[ProductRecord] = []

        while True:
            url = template.format(page=page)
            response = self.fetch(url, headers=self._headers(), verify=False)
            payload = response.json()
            collection = self._extract_collection(payload)
            if not collection:
                break

            products = collection.get("product", [])
            if not products:
                break

            for item in products:
                record = self._to_record(item)
                records.append(record)

            pagination = collection.get("pagination") or {}
            total_pages = pagination.get("total_pages", page)
            if page >= total_pages:
                break
            page += 1

        return records

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "User-Agent": self.session.headers.get("User-Agent", "Mozilla/5.0"),
        }

    def _extract_collection(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        try:
            layouts = payload["data"]["page"]["layouts"]
        except (KeyError, TypeError):
            return None
        for layout in layouts:
            value = layout.get("value") or layout.get("data")
            if not value:
                continue
            collection = value.get("collection")
            if collection:
                return collection
        return None

    def _to_record(self, item: dict[str, Any]) -> ProductRecord:
        name: str = item.get("name", "").strip()
        slug = item.get("slug", "")
        source_url = urljoin("https://www.fairprice.com.sg/product/", slug)

        pricing = self._extract_pricing(item)
        reviews = (item.get("reviews") or {}).get("statistics") or {}
        metadata = {
            "job_description": self.job.description,
            "raw_name": name,
            "list_price": pricing["list_price"],
            "promotion_price": pricing["promotion_price"],
            "display_unit": (item.get("metaData") or {}).get("DisplayUnit"),
            "country_of_origin": (item.get("metaData") or {}).get("Country of Origin"),
            "offers": item.get("offers", []),
        }

        return ProductRecord(
            brand=self.job.brand,
            description=name,
            site=self.job.site_name,
            size=(item.get("metaData") or {}).get("DisplayUnit"),
            ply=self._extract_ply(name),
            price=pricing["price"],
            total_reviews=self._safe_int(reviews.get("total")),
            total_rating=self._safe_float(reviews.get("average")),
            source_url=source_url,
            metadata=metadata,
        )

    def _extract_pricing(self, item: dict[str, Any]) -> dict[str, float | None]:
        price = self._safe_float(item.get("final_price"))
        list_price = None
        promotion_price = None

        if item.get("storeSpecificData"):
            mrp = item["storeSpecificData"][0].get("mrp")
            list_price = self._safe_float(mrp)

        offers = item.get("offers") or []
        if offers:
            promotion_price = self._safe_float(offers[0].get("price"))
            price = promotion_price or price

        return {"price": price, "list_price": list_price, "promotion_price": promotion_price}

    def _extract_ply(self, text: str) -> str | None:
        match = self.PLY_PATTERN.search(text)
        if match:
            return match.group(1)
        return None

    def _safe_float(self, value: Any) -> float | None:
        try:
            if value is None:
                return None
            return float(value)
        except (TypeError, ValueError):
            return None

    def _safe_int(self, value: Any) -> int | None:
        try:
            if value is None:
                return None
            return int(value)
        except (TypeError, ValueError):
            return None

