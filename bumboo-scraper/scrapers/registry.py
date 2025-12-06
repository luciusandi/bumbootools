"""Central place to register scrape jobs."""

from __future__ import annotations

from collections.abc import Iterable

from .catalog import ProductConfig, get_product
from .coldstorage import ColdStorageCategoryScraper
from .example import ExampleScraper
from .fairprice import FairPriceCategoryScraper
from .models import ScrapeJob
from .redmart import RedMartBrandScraper

COLD_STORAGE_SLUGS = [
    "coldstorage-kleenex",
    "coldstorage-nootrees",
    "coldstorage-paseo",
    "coldstorage-pursoft",
    "coldstorage-vinda",
    "coldstorage-tempo",
    "coldstorage-cloversoft",
]

FAIRPRICE_SLUGS = [
    "fairprice-kleenex",
    "fairprice-paseo",
    "fairprice-pursoft",
    "fairprice-fairprice",
    "fairprice-beautex",
    "fairprice-neutra",
    "fairprice-cloversoft",
    "fairprice-nootrees",
    "fairprice-tempo",
]

REDMART_SLUGS = [
    "redmart-tempo",
    "redmart-kleenex",
    "redmart-pursoft",
    "redmart-vinda",
    "redmart-beautex",
    "redmart-paseo",
    "redmart-cloversoft",
    "redmart-nootrees",
]


def _options_from_config(config: ProductConfig) -> dict[str, str]:
    options: dict[str, str] = {"url": config.url}
    if config.size:
        options["size"] = config.size
    if config.ply:
        options["ply"] = config.ply
    options.update(config.extra_options)
    return options


def _build_example_job() -> ScrapeJob:
    config = get_product("example-ultra-soft")
    return ScrapeJob(
        name="example",
        brand=config.brand,
        description=config.description,
        site_name=config.site_name,
        scraper=ExampleScraper,
        options=_options_from_config(config),
    )


def _build_coldstorage_job(slug: str) -> ScrapeJob:
    config = get_product(slug)
    return ScrapeJob(
        name=slug,
        brand=config.brand,
        description=config.description,
        site_name=config.site_name,
        scraper=ColdStorageCategoryScraper,
        options=_options_from_config(config),
    )


def _build_coldstorage_jobs() -> dict[str, ScrapeJob]:
    return {slug: _build_coldstorage_job(slug) for slug in COLD_STORAGE_SLUGS}


def _build_fairprice_job(slug: str) -> ScrapeJob:
    config = get_product(slug)
    return ScrapeJob(
        name=slug,
        brand=config.brand,
        description=config.description,
        site_name=config.site_name,
        scraper=FairPriceCategoryScraper,
        options=_options_from_config(config),
    )


def _build_fairprice_jobs() -> dict[str, ScrapeJob]:
    return {slug: _build_fairprice_job(slug) for slug in FAIRPRICE_SLUGS}


def _build_redmart_job(slug: str) -> ScrapeJob:
    config = get_product(slug)
    return ScrapeJob(
        name=slug,
        brand=config.brand,
        description=config.description,
        site_name=config.site_name,
        scraper=RedMartBrandScraper,
        options=_options_from_config(config),
    )


def _build_redmart_jobs() -> dict[str, ScrapeJob]:
    return {slug: _build_redmart_job(slug) for slug in REDMART_SLUGS}


SCRAPE_JOBS: dict[str, ScrapeJob] = {
    "example": _build_example_job(),
    **_build_coldstorage_jobs(),
    **_build_fairprice_jobs(),
    **_build_redmart_jobs(),
}


def get_job(name: str) -> ScrapeJob:
    try:
        return SCRAPE_JOBS[name]
    except KeyError as exc:
        msg = f"Scrape job '{name}' is not registered"
        raise KeyError(msg) from exc


def list_jobs() -> Iterable[ScrapeJob]:
    return SCRAPE_JOBS.values()

