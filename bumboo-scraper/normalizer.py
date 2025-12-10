"""Top-level normalizer wrapper (duplicate of scrapers.normalizer for module path resolution)."""

from __future__ import annotations

from dataclasses import replace
import re
from typing import Iterable, List, Tuple

from scrapers.models import ProductRecord


NORMALIZATION_MAP: list[dict[str, str]] = [
    {"brand": "Beautex", "description": "Bathroom Tissue Rolls", "size": "20 x 220"},
    {"brand": "Cloversoft", "description": "Plant-Based Unbleached Bamboo", "size": "10 x 200"},
    {"brand": "FairPrice", "description": "Onwards Toilet Rolls", "size": "30 x 220"},
    {"brand": "FairPrice", "description": "DeluxSoft Bathroom Tissue", "size": "20 x 200"},
    {"brand": "FairPrice", "description": "DeluxSoft Bathroom Tissue", "size": "10 x 200"},
    {"brand": "FairPrice", "description": "Silky Soft Bathroom", "size": "24 x 200"},
    {"brand": "FairPrice", "description": "Silky Soft Bathroom", "size": "10 x 200"},
    {"brand": "FairPrice", "description": "DeluxSoft Bathroom", "size": "100 x 200"},
    {"brand": "FairPrice", "description": "DeluxSoft Bathroom", "size": "120 (CTN)"},
    {"brand": "FairPrice", "description": "Silky Soft Bathroom", "size": "100 x 200"},
    {"brand": "Kleenex", "description": "Toilet Rolls - Ultra Soft", "size": "20 x 200"},
    {"brand": "Kleenex", "description": "Ultra Soft Cottony", "size": "30 x 200"},
    {"brand": "Kleenex", "description": "Ultra Soft & Thick", "size": "20 x 180"},
    {"brand": "Kleenex", "description": "Ultra Soft Aloe", "size": "20 x 190"},
    {"brand": "Kleenex", "description": "Toilet Rolls - Ultra Soft", "size": "10 x 200"},
    {"brand": "Kleenex", "description": "Ultra Soft Aloe", "size": "22 x 190"},
    {"brand": "Kleenex", "description": "Toilet Rolls (4ply) + Moist Wipes", "size": "30 x 180"},
    {"brand": "Kleenex", "description": "Supreme Soft", "size": "16 x 190"},
    {"brand": "Kleenex", "description": "Green Tea", "size": "20 x 190"},
    {"brand": "Kleenex", "description": "Ultra Soft Aloe", "size": "10 x 190"},
    {"brand": "Neutra", "description": "Bathroom Tissue Rolls", "size": "20 x 190"},
    {"brand": "NooTrees", "description": "Bamboo Toilet Tissue", "size": "10 x 220"},
    {"brand": "Paseo", "description": "Bathroom Roll", "size": "10 x 200"},
    {"brand": "Paseo", "description": "Bathroom Roll", "size": "30 x 200"},
    {"brand": "Paseo", "description": "Sensitive Skin", "size": "10 x 200"},
    {"brand": "Paseo", "description": "Sensitive Skin", "size": "20 x 200"},
    {"brand": "Paseo", "description": "Luxury Pure Pulp", "size": "24 x 180"},
    {"brand": "Pursoft", "description": "100% Virgin Pulp Unscented", "size": "24 x 1"},
    {"brand": "Pursoft", "description": "Lavender Vanilla", "size": "24 x 180"},
    {"brand": "Pursoft", "description": "Bathroom Toilet R - Unscented", "size": "24 x 220"},
    {"brand": "Pursoft", "description": "Green Tea", "size": "24 x 180"},
    {"brand": "Pursoft", "description": "Citrus Verbena", "size": "24 x 180"},
    {"brand": "Pursoft", "description": "Bathroom Toilet R - Unscented", "size": "10 x 220"},
    {"brand": "Pursoft", "description": "Bathroom Toilet R - Unscented", "size": "10 x 200"},
    {"brand": "Pursoft", "description": "Charcoal Floral", "size": "10 x 220"},
    {"brand": "Pursoft", "description": "Lavender Vanilla", "size": "10 x 180"},
    {"brand": "Pursoft", "description": "Citrus Verbena", "size": "10 x 180"},
    {"brand": "Pursoft", "description": "Green Tea", "size": "10 x 180"},
    {"brand": "Pursoft", "description": "Charcoal Floral", "size": "24 x 220"},
    {"brand": "Tempo", "description": "Bathroom Tissue - Neutral", "size": "10 x 1"},
    {"brand": "Vinda", "description": "Deluxe Smooth Feel Toilet T", "size": "20 x 240"},
    {"brand": "Vinda", "description": "Deluxe Smooth Feel Mega Val", "size": "24 x 1"},
    {"brand": "Vinda", "description": "Prestige Bathroom - 4D Emboss Camillia", "size": "16 x 200"},
    {"brand": "Vinda", "description": "Prestige Toilet Tissue", "size": "8 x 200"},
    {"brand": "Vinda", "description": "Prestige Bathroom - 4D Emboss Camillia", "size": "8 x 200"},
    {"brand": "Vinda", "description": "Prestige Bathroom - 4D Emboss Camillia", "size": "8 x 200"},
]

# Keyword-based fallbacks
KEYWORD_RULES: list[dict[str, object]] = [
    {"brand": "Pursoft", "keywords": ["green", "tea"], "description": "Green Tea", "size": "24 x 180"},
    {"brand": "Pursoft", "keywords": ["lavender", "vanilla"], "description": "Lavender Vanilla", "size": "24 x 180"},
]


def _clean(s: str) -> str:
    return re.sub(r"[^\w\d]+", " ", (s or "").strip().lower())


def _matches(rule: dict[str, str], record: ProductRecord) -> bool:
    if (rule["brand"] or "").strip().lower() != (record.brand or "").strip().lower():
        return False
    rsize = (record.size or "").strip().lower()
    if rsize and rule["size"].strip().lower() == rsize:
        return True
    rd = _clean(record.description)
    if _clean(rule["description"]) in rd:
        return True
    ns = re.sub(r"[^\d x]", "", (rsize or ""))
    if ns and re.sub(r"[^\d x]", "", rule["size"].lower()) in ns:
        return True
    return False


def normalize_record(record: ProductRecord) -> ProductRecord:
    return record


def normalize_records(records: Iterable[ProductRecord]) -> Tuple[List[ProductRecord], List[ProductRecord]]:
    matched: List[ProductRecord] = []
    for r in records:
        matched.append(r)
    return matched, []


