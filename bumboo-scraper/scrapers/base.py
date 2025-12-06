"""Abstract scraper helpers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import requests
from requests import Response

from .models import ProductRecord, ScrapeJob


class BaseScraper(ABC):
    """Base class containing shared HTTP helpers and metadata access."""

    #: Generic desktop UA to avoid blocks from some storefronts.
    DEFAULT_HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )
    }

    def __init__(self, job: ScrapeJob, *, timeout: float = 15.0) -> None:
        self.job = job
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)

    def fetch(self, url: str, **kwargs: Any) -> Response:
        """Fetch a URL using the shared session."""
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response

    def scrape(self) -> list[ProductRecord]:
        """Hook called by the runner."""
        records = self._scrape()
        if not isinstance(records, list):
            msg = "Scraper must return a list of ProductRecord instances"
            raise TypeError(msg)
        return records

    @abstractmethod
    def _scrape(self) -> list[ProductRecord]:
        """Implement site-specific scrape logic."""

