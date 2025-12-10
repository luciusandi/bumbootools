"""Scraper for FairPrice category API (brand-filtered)."""

from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urlencode, urljoin, urlparse, urlunparse, parse_qsl

import urllib3
from bs4 import BeautifulSoup

from .base import BaseScraper
from .models import ProductRecord

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class FairPriceCategoryScraper(BaseScraper):
    """Hits the FairPrice category API and normalizes items."""

    PLY_PATTERN = re.compile(r"(\d+)\s*ply", re.IGNORECASE)

    def _scrape(self) -> list[ProductRecord]:
        # Support two modes:
        # - category API (paged) via 'api_url' in options
        # - single product detail page via 'url' in options
        records: list[ProductRecord] = []
        api_template = self.job.options.get("api_url")
        product_page = self.job.options.get("url")

        if api_template:
            page = 1
            while True:
                url = api_template.format(page=page)
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

        if product_page:
            # Try to extract meaningful fields (title, price) from the product detail page.
            try:
                resp = self.fetch(product_page, headers=self._headers(), verify=False)
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")

                # Try JSON-LD first; prefer nodes where "@type" is "Product"
                price = None
                title = None
                rating = None
                review_count = None
                for tag in soup.find_all("script", {"type": "application/ld+json"}):
                    try:
                        data = json.loads(tag.string or "{}")
                    except Exception:
                        continue

                    # normalize to iterable of candidate nodes
                    candidates = data if isinstance(data, list) else [data]

                    def _process_node(node: dict) -> tuple[None | float, None | str, None | object, None | object]:
                        """Extract price, title, rating, review_count from a JSON-LD node if present."""
                        local_price = None
                        local_title = None
                        local_rating = None
                        local_review_count = None
                        if not isinstance(node, dict):
                            return local_price, local_title, local_rating, local_review_count
                        # if node contains @graph, inspect graph entries
                        graph = node.get("@graph") or node.get("graph")
                        if isinstance(graph, list):
                            for entry in graph:
                                p, t, r, rc = _process_node(entry)
                                local_price = local_price or p
                                local_title = local_title or t
                                local_rating = local_rating or r
                                local_review_count = local_review_count or rc
                            return local_price, local_title, local_rating, local_review_count

                        typ = node.get("@type") or node.get("type") or ""
                        # extract title
                        local_title = node.get("name") or (node.get("brand") or {}).get("name") or None
                        # offers may be dict or list
                        offers = node.get("offers")
                        if offers:
                            if isinstance(offers, list):
                                offers = offers[0] if offers else None
                            if isinstance(offers, dict):
                                p = offers.get("price") or (offers.get("priceSpecification") and offers["priceSpecification"].get("price"))
                                if p:
                                    try:
                                        local_price = float(str(p))
                                    except Exception:
                                        local_price = None
                        # aggregate rating
                        agg = node.get("aggregateRating") or node.get("aggregate_rating")
                        if isinstance(agg, dict):
                            local_rating = local_rating or agg.get("ratingValue")
                            local_review_count = local_review_count or agg.get("reviewCount")
                        # nested review -> reviewRating
                        rev = node.get("review")
                        if isinstance(rev, dict):
                            rr = rev.get("reviewRating") or {}
                            local_rating = local_rating or rr.get("ratingValue")
                        return local_price, local_title, local_rating, local_review_count

                    for node in candidates:
                        p, t, r, rc = _process_node(node)
                        if t and not title:
                            title = t
                        if p is not None and price is None:
                            price = p
                        if r is not None and rating is None:
                            rating = r
                        if rc is not None and review_count is None:
                            review_count = rc
                    if price is not None:
                        break
                # If rating/review_count not found yet, search JSON-LD blobs for AggregateRating nodes
                if (rating is None or review_count is None):
                    def _search_agg(obj):
                        if isinstance(obj, dict):
                            atype = obj.get("@type") or obj.get("type") or ""
                            if isinstance(atype, str) and atype.lower().startswith("aggregaterating"):
                                return obj.get("ratingValue"), obj.get("reviewCount")
                            # direct aggregateRating key
                            if "aggregateRating" in obj and isinstance(obj["aggregateRating"], dict):
                                ar = obj["aggregateRating"]
                                return ar.get("ratingValue"), ar.get("reviewCount")
                            for v in obj.values():
                                res = _search_agg(v)
                                if res and (res[0] is not None or res[1] is not None):
                                    return res
                        elif isinstance(obj, list):
                            for it in obj:
                                res = _search_agg(it)
                                if res and (res[0] is not None or res[1] is not None):
                                    return res
                        return (None, None)

                    for tag in soup.find_all("script", {"type": "application/ld+json"}):
                        try:
                            blob = json.loads(tag.string or "{}")
                        except Exception:
                            continue
                        r_rating, r_count = _search_agg(blob)
                        if r_rating is not None or r_count is not None:
                            rating = rating or r_rating
                            review_count = review_count or r_count
                            break

                # meta tags fallback
                if price is None:
                    meta_price = soup.find("meta", {"property": "og:price:amount"}) or soup.find("meta", {"itemprop": "price"})
                    if meta_price and meta_price.get("content"):
                        try:
                            price = float(re.search(r"[\d.]+", meta_price["content"]).group())
                        except Exception:
                            price = None

                # title fallback
                if not title:
                    og_title = soup.find("meta", {"property": "og:title"}) or soup.find("meta", {"name": "title"})
                    if og_title and og_title.get("content"):
                        title = og_title["content"]
                    else:
                        h1 = soup.find("h1")
                        if h1:
                            title = h1.get_text(strip=True)

                # Scoped JSON-LD/text search: try to find a Product JSON-LD block in the raw HTML
                if price is None:
                    prod_pos = -1
                    for marker in ('"@type":"Product"', "'@type':'Product'", '"@type": "Product"'):
                        prod_pos = html.find(marker)
                        if prod_pos != -1:
                            break
                    if prod_pos != -1:
                        window_start = max(0, prod_pos - 800)
                        window_end = min(len(html), prod_pos + 2000)
                        window = html[window_start:window_end]
                        m = re.search(r'"price"\s*:\s*"?([0-9]+(?:\.[0-9]+)?)"?', window)
                        if m:
                            try:
                                price = float(m.group(1))
                            except Exception:
                                price = None

                # loose regex fallback for visible price strings like $11.85 or 11.85 (last resort)
                if price is None:
                    m = re.search(r"(?<!\d)([0-9]{1,3}(?:\.[0-9]{1,2})?)(?!\d)", html)
                    if m:
                        # choose the first plausible price > 1.0 (exclude small integers like '1' which may be quantity)
                        cand = None
                        try:
                            cand = float(m.group(1))
                        except Exception:
                            cand = None
                        if cand and cand > 1.0:
                            price = cand

                metadata = {
                    "job_description": self.job.description,
                    "raw_html_snippet": html[:200],
                    "original_description": title,
                }
                # if JSON-LD extraction missed them, try regex window search
                if rating is None or review_count is None:
                    parsed_rating, parsed_reviews = self._parse_rating_from_html(html)
                    rating = rating or parsed_rating
                    review_count = review_count or parsed_reviews
                # coerce rating/review_count values (handle "null" strings)
                def _coerce_float(v):
                    if v is None:
                        return None
                    try:
                        s = str(v).strip()
                        if not s or s.lower() in ("null", "none", "n/a"):
                            return None
                        return float(s)
                    except Exception:
                        return None

                def _coerce_int(v):
                    if v is None:
                        return None
                    try:
                        s = str(v).strip()
                        if not s or s.lower() in ("null", "none", "n/a"):
                            return None
                        return int(float(s))
                    except Exception:
                        return None

                coerced_rating = _coerce_float(rating)
                coerced_reviews = _coerce_int(review_count)
                metadata.update({"extracted_rating": rating, "extracted_review_count": review_count})
                return [
                    ProductRecord(
                        brand=self.job.brand,
                        description=self.job.options.get("dataset_description") or title or (self.job.description or ""),
                        site=self.job.site_name,
                        size=self.job.options.get("size"),
                        ply=self.job.options.get("ply"),
                        price=price,
                        total_reviews=coerced_reviews,
                        total_rating=coerced_rating,
                        source_url=product_page,
                        metadata=metadata,
                    )
                ]
            except Exception:
                # If parsing fails, fall back to minimal record
                metadata = {"job_description": self.job.description, "source_note": "product-page-fallback"}
                return [
                    ProductRecord(
                        brand=self.job.brand,
                        description=self.job.description or "",
                        site=self.job.site_name,
                        size=self.job.options.get("size"),
                        ply=self.job.options.get("ply"),
                        price=None,
                        total_reviews=None,
                        total_rating=None,
                        source_url=product_page,
                        metadata=metadata,
                    )
                ]

        raise KeyError("Neither 'api_url' nor 'url' provided for FairPrice scraper options")

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
            "original_description": name,
        }
        record_description = self.job.options.get("dataset_description") or name
        return ProductRecord(
            brand=self.job.brand,
            description=record_description,
            site=self.job.site_name,
            size=self.job.options.get("size") or (item.get("metaData") or {}).get("DisplayUnit"),
            ply=self.job.options.get("ply") or self._extract_ply(name),
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

    def _parse_price_from_html(self, html: str) -> float | None:
        """
        Try several strategies to extract a price from a FairPrice product page HTML:
        1. JSON-LD / application/ld+json offers.price
        2. meta tags like product:price:amount or itemprop="price"
        3. inline JS variables like "final_price" or "price"
        4. visible price text patterns like $11.85 or 11.85
        """
        # 1. JSON-LD
        try:
            for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', html, re.I | re.S):
                try:
                    obj = json.loads(m.group(1))
                except Exception:
                    continue
                # object may be a list or dict
                candidates = obj if isinstance(obj, list) else [obj]
                for c in candidates:
                    offers = c.get("offers") if isinstance(c, dict) else None
                    if isinstance(offers, dict):
                        price = offers.get("price")
                        if price:
                            try:
                                return float(str(price).replace(",", ""))
                            except Exception:
                                pass
        except Exception:
            pass

        # 2. meta tags and itemprop
        m = re.search(r'<meta[^>]+property=["\']product:price:amount["\'][^>]+content=["\']([\d\.,]+)["\']', html, re.I)
        if m:
            try:
                return float(m.group(1).replace(",", ""))
            except Exception:
                pass
        m = re.search(r'itemprop=["\']price["\'][^>]*content=["\']?([\d\.,]+)["\']?', html, re.I)
        if m:
            try:
                return float(m.group(1).replace(",", ""))
            except Exception:
                pass

        # 3. inline JS "final_price" or "price" numeric tokens
        m = re.search(r'"final_price"\s*:\s*([0-9]+(?:\.[0-9]+)?)', html)
        if m:
            try:
                return float(m.group(1))
            except Exception:
                pass
        m = re.search(r'"price"\s*:\s*"?\$?([\d\.,]+)"?', html)
        if m:
            try:
                return float(m.group(1).replace(",", ""))
            except Exception:
                pass

        # 4. visible price like $11.85 or 11.85
        m = re.search(r'[$]\s*([\d]{1,3}(?:[,\d{3}]*)(?:\.\d{1,2})?)', html)
        if m:
            try:
                return float(m.group(1).replace(",", ""))
            except Exception:
                pass
        m = re.search(r'(\d+\.\d{1,2})\s*(?:per|per pack|per pkt)?', html)
        if m:
            try:
                return float(m.group(1))
            except Exception:
                pass

        return None

    def _parse_rating_from_html(self, html: str) -> tuple[float | None, int | None]:
        """
        Look for JSON-LD or inline snippets that expose aggregateRating / reviewRating.
        """
        rating = None
        reviews = None
        match = re.search(
            r'"aggregateRating"\s*:\s*\{[^}]*"ratingValue"\s*:\s*"([^"]+)"[^}]*"reviewCount"\s*:\s*"([^"]+)"',
            html,
            re.S,
        )
        if match:
            try:
                rating = float(match.group(1))
            except Exception:
                rating = None
            try:
                reviews = int(float(match.group(2)))
            except Exception:
                reviews = None
            return rating, reviews

        match = re.search(
            r'"reviewRating"\s*:\s*\{[^}]*"ratingValue"\s*:\s*"([^"]+)"',
            html,
            re.S,
        )
        if match:
            try:
                rating = float(match.group(1))
            except Exception:
                rating = None
        return rating, reviews

