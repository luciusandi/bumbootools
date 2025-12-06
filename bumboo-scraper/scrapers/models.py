"""Data models shared by all scrapers."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Protocol


@dataclass(slots=True)
class ProductRecord:
    """Normalized record representing a single toilet paper product."""

    brand: str
    description: str
    site: str
    size: str | None
    ply: str | None
    price: float | None
    total_reviews: int | None
    total_rating: float | None
    source_url: str
    metadata: dict[str, str] = field(default_factory=dict)
    collected_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(slots=True)
class ScrapeJob:
    """
    Job definition for a single run.

    Allows the user to override the brand / description metadata while
    wiring up a site-specific scraper implementation.
    """

    name: str
    brand: str
    description: str
    site_name: str
    scraper: type["BaseScraper"]
    options: dict[str, str] = field(default_factory=dict)


class BaseScraper(Protocol):
    """Protocol implemented by every scraper class."""

    def __init__(self, job: ScrapeJob):
        ...

    def scrape(self) -> list[ProductRecord]:
        ...

