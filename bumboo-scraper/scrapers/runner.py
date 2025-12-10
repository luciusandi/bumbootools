"""CLI runner to execute registered scrapers."""

from __future__ import annotations

import argparse
import logging
import sys
from typing import Iterable

from dotenv import load_dotenv

from .models import ProductRecord, ScrapeJob
from .registry import get_job, list_jobs
from .storage import LocalJSONStorage, SupabaseStorage
# normalize_records may be dynamically imported at runtime to avoid module path issues
from .catalog import get_product, load_dataset_rows
from .fairprice import FairPriceCategoryScraper
from .coldstorage import ColdStorageCategoryScraper
from .redmart import RedMartBrandScraper
import re

logger = logging.getLogger("scraper-runner")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jobs",
        nargs="+",
        help="Names of the scrape jobs to run (default: all registered)",
    )
    parser.add_argument(
        "--table",
        default="tissue_prices",
        help="Supabase table name to upsert records into",
    )
    parser.add_argument(
        "--local-dump",
        action="store_true",
        help="Always write a JSON copy under data/raw for auditing",
    )
    parser.add_argument(
        "--dump-first",
        action="store_true",
        help="Write local dump before attempting Supabase (keeps DB insert)",
    )
    parser.add_argument(
        "--skip-supabase",
        action="store_true",
        help="Skip Supabase persistence (useful for dry runs)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    parser.add_argument(
        "--dataset-row",
        type=int,
        help="Run scrapers for a single CSV row (0-based index) from dataset.csv",
    )
    parser.add_argument(
        "--dataset-path",
        help="Path to dataset.csv (default: project dataset.csv)",
    )
    return parser.parse_args(argv)


def run_job(job: ScrapeJob) -> list[ProductRecord]:
    logger.info("Running job '%s' for brand '%s'", job.name, job.brand)
    scraper = job.scraper(job)
    records = scraper.scrape()
    logger.info("Job '%s' produced %d record(s)", job.name, len(records))
    return records


def _slugify(value: str) -> str:
    v = (value or "").strip().lower()
    v = re.sub(r"[^\w]+", "-", v)
    v = re.sub(r"-{2,}", "-", v).strip("-")
    return v or "unknown"


def build_jobs_from_dataset_row(row_index: int, dataset_path: str | None = None) -> list[ScrapeJob]:
    """
    Build ScrapeJob objects for a single CSV row. Returns jobs for FairPrice,
    Cold Storage, and RedMart only when the dataset row has a product URL for that site.
    Jobs reuse the existing ProductConfig entries (API-based).
    """
    rows = load_dataset_rows(dataset_path)
    if row_index < 0 or row_index >= len(rows):
        raise IndexError(f"dataset row {row_index} out of range (0..{len(rows)-1})")
    row = rows[row_index]
    brand = row.get("Brand") or row.get("brand") or ""
    size = row.get("Pack Size") or None
    ply = row.get("Ply") or None
    dataset_desc = row.get("Desc") or row.get("description") or ""

    site_configs: dict[str, tuple[str, type[ScrapeJob], str]] = {
        "Fairprice": ("fairprice", FairPriceCategoryScraper, "detail_url"),
        "ColdStorage": ("coldstorage", ColdStorageCategoryScraper, "detail_url"),
        "Redmart": ("redmart", RedMartBrandScraper, "product_name"),
    }
    jobs: list[ScrapeJob] = []
    for col_name, (slug_prefix, scraper_cls, data_kind) in site_configs.items():
        detail_value = (row.get(col_name) or "").strip()
        if not detail_value or detail_value in ("-", ""):
            continue
        slug = f"{slug_prefix}-{_slugify(brand)}"
        try:
            config = get_product(slug)
        except KeyError:
            logger.warning(
                "No ProductConfig for slug '%s' (brand=%s); skipping %s job from dataset row %d",
                slug,
                brand,
                col_name,
                row_index,
            )
            continue

        options: dict[str, str] = {"url": config.url}
        options.update(config.extra_options)
        if size:
            options["size"] = size
        if ply:
            options["ply"] = ply
        if dataset_desc:
            options["dataset_description"] = dataset_desc
        if data_kind == "product_name":
            options["dataset_product_name"] = detail_value
        elif data_kind == "url":
            options["dataset_detail_url"] = detail_value
        elif data_kind == "detail_url":
            options["url"] = detail_value
            options["dataset_detail_url"] = detail_value
            # If user explicitly provided a detail URL for this dataset row,
            # ensure we do not accidentally run the catalog/API path by removing
            # any api_url that comes from the ProductConfig.
            options.pop("api_url", None)

        job = ScrapeJob(
            name=f"{config.slug}-dataset-row-{row_index}",
            brand=config.brand,
            description=config.description,
            site_name=config.site_name,
            scraper=scraper_cls,
            options={**options},
        )
        jobs.append(job)
    return jobs


def persist_records(
    records: Iterable[ProductRecord],
    *,
    table: str,
    skip_supabase: bool,
    force_local_dump: bool,
    dump_first: bool = False,
    dataset_row: int | None = None,
) -> None:
    records = list(records)
    if not records:
        logger.info("No records to persist")
        return
    # Import normalizer lazily so module resolution works when running as a module
    try:
        from .normalizer import normalize_records  # type: ignore
    except Exception:
        try:
            import normalizer as _normalizer  # type: ignore

            normalize_records = _normalizer.normalize_records  # type: ignore
        except Exception:
            logger.warning("Normalizer not available; skipping normalization")
            def normalize_records(x):
                return list(x), []

    # Normalize records first; write unmatched to a separate file for manual review
    matched, unmatched = normalize_records(records)
    if unmatched:
        prefix_unmatched = f"unmatched_row{dataset_row}" if dataset_row is not None else "unmatched"
        output_path_unmatched = LocalJSONStorage().dump_with_prefix(unmatched, prefix=prefix_unmatched)
        logger.info("Wrote %d unmatched record(s) to %s", len(unmatched), output_path_unmatched)

    stored = False
    # If requested, write matched set first for auditing before attempting Supabase
    matched_dump_written = False
    if matched and dump_first:
        prefix_matched = f"scrape_row{dataset_row}" if dataset_row is not None else "scrape"
        output_path = LocalJSONStorage().dump_with_prefix(matched, prefix=prefix_matched)
        logger.info("Wrote JSON copy to %s (dump-first)", output_path)
        matched_dump_written = True

    if matched and not skip_supabase:
        try:
            SupabaseStorage(table_name=table).upsert(matched)
        except RuntimeError as exc:
            logger.warning("Supabase disabled (%s); falling back to local dump", exc)
        else:
            stored = True
            logger.info("Persisted %d normalized record(s) to Supabase table '%s'", len(matched), table)

    # Always write a local dump if requested or Supabase not used for matched records.
    if force_local_dump or not stored:
        # write matched set (normalized) for auditing unless already written via dump-first
        if matched and not matched_dump_written:
            prefix_matched = f"scrape_row{dataset_row}" if dataset_row is not None else "scrape"
            output_path = LocalJSONStorage().dump_with_prefix(matched, prefix=prefix_matched)
            logger.info("Wrote JSON copy to %s", output_path)
        elif unmatched and not matched:
            # nothing matched and user wanted a local dump; unmatched already written
            logger.info("No matched records to dump; unmatched records available")


def main(argv: list[str] | None = None) -> None:
    try:
        load_dotenv()
    except PermissionError as exc:
        logger.warning("Could not read .env (%s); continuing without it", exc)
    args = parse_args(argv or sys.argv[1:])
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    selected_jobs: Iterable[ScrapeJob]
    if args.dataset_row is not None:
        # build jobs only for the requested dataset row
        try:
            selected_jobs = build_jobs_from_dataset_row(args.dataset_row, dataset_path=args.dataset_path)
        except Exception as exc:
            logger.error("Could not build jobs from dataset: %s", exc)
            return
    elif args.jobs:
        selected_jobs = [get_job(name) for name in args.jobs]
    else:
        selected_jobs = list_jobs()

    all_records: list[ProductRecord] = []
    for job in selected_jobs:
        all_records.extend(run_job(job))

    persist_records(
        all_records,
        table=args.table,
        skip_supabase=args.skip_supabase,
        force_local_dump=args.local_dump,
    )


if __name__ == "__main__":
    main()

