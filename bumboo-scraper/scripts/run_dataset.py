"""Utility script to run every row in dataset.csv via scrapers.runner."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scrapers.catalog import load_dataset_rows


def iter_indexes(start: int | None, end: int | None) -> Iterable[int]:
    rows = load_dataset_rows()
    last = len(rows) - 1
    if start is None:
        start = 0
    if end is None or end > last:
        end = last
    if start < 0:
        raise ValueError("start must be >= 0")
    if start > end:
        raise ValueError("start must be <= end")
    return range(start, end + 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--start",
        type=int,
        help="Start index (0-based) of dataset rows to run",
    )
    parser.add_argument(
        "--end",
        type=int,
        help="End index (inclusive) of dataset rows to run",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Log level forwarded to scrapers.runner",
    )
    parser.add_argument(
        "--local-dump",
        action="store_true",
        help="Forward --local-dump to the runner",
    )
    parser.add_argument(
        "--dump-first",
        action="store_true",
        help="Forward --dump-first to the runner",
    )
    parser.add_argument(
        "--table",
        default="tissue_prices",
        help="Supabase table name to upsert into",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without executing them",
    )

    args = parser.parse_args()

    python_cmd = [ROOT_DIR / "venv" / "bin" / "python"]
    if not python_cmd[0].exists():
        python_cmd = ["python"]

    for idx in iter_indexes(args.start, args.end):
        cmd = [
            *python_cmd,
            "-m",
            "scrapers.runner",
            "--dataset-row",
            str(idx),
            "--table",
            args.table,
            "--log-level",
            args.log_level,
        ]
        # forward dump-first and local-dump flags if provided to this script
        if args.dump_first:
            cmd.append("--dump-first")
        if args.local_dump:
            cmd.append("--local-dump")
        print(f"Running row {idx}: {' '.join(cmd)}")
        if not args.dry_run:
            subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()

