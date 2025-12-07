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
        "--skip-supabase",
        action="store_true",
        help="Skip Supabase persistence (useful for dry runs)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser.parse_args(argv)


def run_job(job: ScrapeJob) -> list[ProductRecord]:
    logger.info("Running job '%s' for brand '%s'", job.name, job.brand)
    scraper = job.scraper(job)
    records = scraper.scrape()
    logger.info("Job '%s' produced %d record(s)", job.name, len(records))
    return records


def persist_records(
    records: Iterable[ProductRecord],
    *,
    table: str,
    skip_supabase: bool,
    force_local_dump: bool,
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
        output_path_unmatched = LocalJSONStorage().dump_with_prefix(unmatched, prefix="unmatched")
        logger.info("Wrote %d unmatched record(s) to %s", len(unmatched), output_path_unmatched)

    stored = False
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
        # write matched set (normalized) for auditing
        if matched:
            output_path = LocalJSONStorage().dump_with_prefix(matched, prefix="scrape")
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
    if args.jobs:
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

