from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import CANONICAL_FIELDS

REQUIRED_STORES = {"app_store", "play_store"}


def validate_record(record: dict[str, Any], line_no: int) -> list[str]:
    errors: list[str] = []
    for field in CANONICAL_FIELDS:
        if field not in record:
            errors.append(f"line {line_no}: missing field '{field}'")
    if errors:
        return errors

    rating = record["rating"]
    if not isinstance(rating, int) or rating < 1 or rating > 5:
        errors.append(f"line {line_no}: rating must be 1-5, got {rating!r}")

    if not str(record.get("text", "")).strip():
        errors.append(f"line {line_no}: text must be non-empty")

    store = record.get("store")
    if store not in REQUIRED_STORES:
        errors.append(f"line {line_no}: store must be app_store or play_store, got {store!r}")

    date = record.get("date", "")
    if not date.endswith("Z") or "T" not in date:
        errors.append(f"line {line_no}: date must be ISO 8601 UTC, got {date!r}")

    return errors


def validate_normalized_file(path: Path, min_rows: int = 1) -> tuple[list[str], dict[str, Any]]:
    """Return (errors, summary)."""
    if not path.is_file():
        return [f"file not found: {path}"], {}

    errors: list[str] = []
    stores: set[str] = set()
    line_count = 0

    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            line_count += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON — {exc}")
                continue
            if not isinstance(record, dict):
                errors.append(f"line {line_no}: expected JSON object")
                continue
            errors.extend(validate_record(record, line_no))
            stores.add(record.get("store", ""))

    if line_count < min_rows:
        errors.append(f"expected at least {min_rows} rows, got {line_count}")

    missing_stores = REQUIRED_STORES - stores
    if missing_stores:
        errors.append(f"missing stores in output: {sorted(missing_stores)}")

    summary = {
        "row_count": line_count,
        "stores": sorted(stores),
    }
    return errors, summary
