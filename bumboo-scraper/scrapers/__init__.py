"""
Reusable scraping package for the price watch pipeline.

Modules
-------
models
    Shared dataclasses for scraped products and scrape jobs.
base
    Base scraper definitions and helper utilities.
registry
    Registry of available scrapers that runner can execute.
storage
    Persistence layer, currently targeting Supabase.
runner
    Command-line entry-point to run selected scrapers.
"""

from .models import ProductRecord, ScrapeJob

__all__ = ["ProductRecord", "ScrapeJob"]

