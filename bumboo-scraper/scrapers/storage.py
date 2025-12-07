"""Persistence helpers for scraper output."""

from __future__ import annotations

import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from supabase import Client, create_client

from .models import ProductRecord


class SupabaseStorage:
    """Simple Supabase upsert helper."""

    def __init__(self, table_name: str = "tissue_prices") -> None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            msg = "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set"
            raise RuntimeError(msg)
        self.table_name = table_name
        self.client: Client = create_client(url, key)

    def upsert(self, records: Iterable[ProductRecord]) -> None:
        payload = []
        for record in records:
            serialized = asdict(record)
            serialized["collected_at"] = record.collected_at.isoformat()
            payload.append(serialized)
        if not payload:
            return
        self.client.table(self.table_name).upsert(payload).execute()


class LocalJSONStorage:
    """Fallback storage that stores payloads under data/raw/*.json."""

    def __init__(self, base_dir: str = "data/raw") -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def dump(self, records: Iterable[ProductRecord]) -> Path:
        serialized = []
        for record in records:
            data = asdict(record)
            data["collected_at"] = record.collected_at.isoformat()
            serialized.append(data)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_path = self.base_path / f"scrape_{timestamp}.json"
        output_path.write_text(
            json.dumps(serialized, indent=2), encoding="utf-8"
        )
        return output_path

    def dump_with_prefix(self, records: Iterable[ProductRecord], prefix: str = "scrape") -> Path:
        """Dump records to data/raw/{prefix}_{timestamp}.json"""
        serialized = []
        for record in records:
            data = asdict(record)
            data["collected_at"] = record.collected_at.isoformat()
            serialized.append(data)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        output_path = self.base_path / f"{prefix}_{timestamp}.json"
        output_path.write_text(json.dumps(serialized, indent=2), encoding="utf-8")
        return output_path

