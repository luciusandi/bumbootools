"""Example scraper that emits static data.

Used to validate the pipeline before wiring real storefronts.
"""

from __future__ import annotations

from .base import BaseScraper
from .models import ProductRecord


class ExampleScraper(BaseScraper):
    """Creates deterministic output using job metadata."""

    def _scrape(self) -> list[ProductRecord]:
        options = self.job.options
        record = ProductRecord(
            brand=self.job.brand,
            description=self.job.description,
            site=self.job.site_name,
            size=options.get("size", "24 mega rolls"),
            ply=options.get("ply", "3"),
            price=float(options.get("price", 29.99)),
            total_reviews=int(options.get("total_reviews", 1200)),
            total_rating=float(options.get("total_rating", 4.8)),
            source_url=options.get("url", "https://example.com/toilet-paper"),
            metadata={"note": "Replace with real scraper once ready"},
        )
        return [record]

