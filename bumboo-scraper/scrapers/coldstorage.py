"""Scraper for Cold Storage category listings."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urljoin

import urllib3
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

from .base import BaseScraper
from .models import ProductRecord


class ColdStorageCategoryScraper(BaseScraper):
    """Parses toilet paper listings from Cold Storage."""

    CARD_SELECTOR = "div.list-wrapper div.row-container a.ware-wrapper"
    PRICE_PATTERN = re.compile(r"[^\d]")
    PLY_PATTERN = re.compile(r"(\d+)\s*ply", re.IGNORECASE)
    SIZE_TOKEN_PATTERN = re.compile(r"\b\d+[^\s]*", re.IGNORECASE)

    def _scrape(self) -> list[ProductRecord]:
        detail_page = self.job.options.get("dataset_detail_url")
        if detail_page:
            return self._scrape_detail_page(detail_page)

        url = self.job.options["url"]
        response = self.fetch(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select(self.CARD_SELECTOR)
        records: list[ProductRecord] = []
        for card in cards:
            name = self._text(card.select_one(".name"))
            if not name:
                continue
            listing_url = urljoin(response.url, card.get("href", "").strip())
            price = self._parse_price(card)
            list_price = self._parse_line_price(card)
            metadata: dict[str, Any] = {
                "job_description": self.job.description,
                "raw_name": name,
                "list_price": list_price,
                "sold_out": bool(card.select_one(".sold")),
            }
            record = ProductRecord(
                brand=self.job.brand,
                description=name,
                site=self.job.site_name,
                size=self.job.options.get("size") or self._extract_size(name),
                ply=self.job.options.get("ply") or self._extract_ply(name),
                price=price,
                total_reviews=None,
                total_rating=None,
                source_url=listing_url,
                metadata=metadata,
            )
            records.append(record)
        return records

    def _scrape_detail_page(self, url: str) -> list[ProductRecord]:
        response = self.fetch(url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")
        info = soup.select_one(".info-content")
        if not info:
            return []
        title_node = info.select_one(".title")
        price_line = info.select_one(".price-line")
        if not title_node or not price_line:
            return []
        name = title_node.get_text(strip=True)
        price_val = self._parse_price_line(price_line)
        metadata: dict[str, Any] = {
            "job_description": self.job.description,
            "dataset_detail_url": url,
            "original_description": name,
        }
        record_description = self.job.options.get("dataset_description") or name
        record = ProductRecord(
            brand=self.job.brand,
            description=record_description,
            site=self.job.site_name,
            size=self.job.options.get("size") or self._extract_size(name),
            ply=self.job.options.get("ply") or self._extract_ply(name),
            price=price_val,
            total_reviews=None,
            total_rating=None,
            source_url=url,
            metadata=metadata,
        )
        return [record]

    def _text(self, node) -> str:
        return node.get_text(strip=True) if node else ""

    def _parse_price(self, card) -> float | None:
        price_node = card.select_one(".price-box .price")
        dollars = self._sanitize_number(price_node)
        if dollars is None:
            return None
        cents_node = card.select_one(".price-box .small-price")
        cents = self._sanitize_number(cents_node, allow_empty=True) or "00"
        return float(f"{dollars}.{cents.zfill(2)}")

    def _parse_line_price(self, card) -> float | None:
        node = card.select_one(".price-box .line-price")
        value = self._sanitize_number(node, allow_decimal=True)
        return float(value) if value else None

    def _sanitize_number(
        self, node, *, allow_empty: bool = False, allow_decimal: bool = False
    ) -> str | None:
        if not node:
            return None if not allow_empty else ""
        text = node.get_text(strip=True)
        if allow_decimal:
            cleaned = re.sub(r"[^\d.]", "", text)
        else:
            cleaned = re.sub(self.PRICE_PATTERN, "", text)
        if not cleaned and not allow_empty:
            return None
        return cleaned

    def _extract_ply(self, name: str) -> str | None:
        match = self.PLY_PATTERN.search(name)
        if match:
            return match.group(1)
        return None

    def _extract_size(self, name: str) -> str | None:
        normalized = name
        if normalized.lower().startswith(self.job.brand.lower()):
            normalized = normalized[len(self.job.brand) :].strip()
        tokens: list[str] = []
        for match in self.SIZE_TOKEN_PATTERN.finditer(normalized):
            token = match.group(0)
            if self._is_ply_token(token, normalized, match.start(), match.end()):
                continue
            tokens.append(token)
        value = " ".join(tokens).strip()
        return value or None

    def _is_ply_token(self, token: str, text: str, start: int, end: int) -> bool:
        if "ply" in token.lower():
            return True
        tail = text[end : end + 4].lower()
        if tail.startswith("ply"):
            return True
        head = text[max(0, start - 3) : start].lower()
        if head.endswith("ply"):
            return True
        return False

    def _parse_price_line(self, node) -> float | None:
        integer = node.select_one(".price")
        decimal = node.select_one(".price-small")
        if not integer:
            return None
        whole = self._sanitize_number(integer) or ""
        frac = self._sanitize_number(decimal, allow_empty=True) or ""
        if frac:
            frac = frac.lstrip(".")
        if not whole and not frac:
            return None
        denom = frac.ljust(2, "0") if frac else "00"
        value = whole or "0"
        try:
            return float(f"{value}.{denom}")
        except ValueError:
            return None

