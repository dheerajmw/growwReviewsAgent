from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

from .config import IngestConfig

STORE_APP = "app_store"
STORE_PLAY = "play_store"


def _normalize_header(name: str) -> str:
    return re.sub(r"\s+", " ", (name or "").strip().lower())


def _resolve_column(row: dict[str, str], aliases: list[str]) -> str | None:
    if not row:
        return None
    normalized = {_normalize_header(k): v for k, v in row.items()}
    for alias in aliases:
        key = _normalize_header(alias)
        if key in normalized:
            val = (normalized[key] or "").strip()
            if val:
                return val
    return None


def _parse_rating(raw: str | None) -> int | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    # "5", "5.0", "5 stars"
    match = re.search(r"([1-5])", text)
    if not match:
        return None
    return int(match.group(1))


def _parse_date(raw: str | None) -> datetime | None:
    if not raw or not str(raw).strip():
        return None
    text = str(raw).strip()
    formats = (
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%d/%m/%Y",
        "%d/%m/%Y %H:%M:%S",
        "%B %d, %Y",
        "%b %d, %Y",
    )
    for fmt in formats:
        try:
            dt = datetime.strptime(text[:19] if "T" in fmt else text, fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    # ISO partial
    try:
        cleaned = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


def _stable_review_id(store: str, review_id: str | None, date: str, title: str, text: str) -> str:
    if review_id:
        return f"{store}:{review_id}"
    payload = f"{store}|{date}|{title}|{text}".encode("utf-8")
    return f"{store}:hash:{hashlib.sha256(payload).hexdigest()[:16]}"


def _read_csv_rows(path: Path) -> Iterator[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return
        for row in reader:
            yield {k: (v or "") for k, v in row.items() if k}


def _read_json_rows(path: Path) -> Iterator[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                yield {str(k): str(v) if v is not None else "" for k, v in item.items()}
    elif isinstance(data, dict):
        for item in data.get("reviews") or data.get("data") or []:
            if isinstance(item, dict):
                yield {str(k): str(v) if v is not None else "" for k, v in item.items()}


def iter_source_rows(path: Path) -> Iterator[dict[str, str]]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        yield from _read_json_rows(path)
    elif suffix in {".csv", ".tsv"}:
        yield from _read_csv_rows(path)
    else:
        raise ValueError(f"Unsupported export format: {path}")


def parse_row(
    row: dict[str, str],
    store: str,
    config: IngestConfig,
) -> tuple[dict[str, Any] | None, str | None]:
    """Return (canonical_record, skip_reason). skip_reason set if row invalid."""
    store_key = "app_store" if store == STORE_APP else "play_store"
    aliases = config.column_aliases.get(store_key, {})

    raw_id = _resolve_column(row, aliases.get("review_id", []))
    raw_rating = _resolve_column(row, aliases.get("rating", []))
    raw_title = _resolve_column(row, aliases.get("title", [])) or ""
    raw_text = _resolve_column(row, aliases.get("text", []))
    raw_date = _resolve_column(row, aliases.get("date", []))

    rating = _parse_rating(raw_rating)
    if rating is None:
        return None, "invalid_rating"

    if not raw_text or not raw_text.strip():
        return None, "empty_text"

    dt = _parse_date(raw_date)
    if dt is None:
        return None, "invalid_date"

    iso_date = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    review_id = _stable_review_id(store, raw_id, iso_date, raw_title, raw_text.strip())

    return {
        "rating": rating,
        "title": raw_title.strip(),
        "text": raw_text.strip(),
        "date": iso_date,
        "store": store,
        "review_id": review_id,
    }, None


def discover_raw_files(raw_dir: Path, glob_pattern: str) -> list[Path]:
    if not raw_dir.is_dir():
        return []
    files = sorted(raw_dir.glob(glob_pattern))
    return [p for p in files if p.is_file() and p.suffix.lower() in {".csv", ".json", ".tsv"}]
