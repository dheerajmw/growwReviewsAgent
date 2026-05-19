from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import Phase2Config

logger = logging.getLogger(__name__)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def sample_reviews(
    all_reviews: list[dict[str, Any]],
    max_count: int,
) -> list[dict[str, Any]]:
    """Stratified sample by store; newest first within each store."""
    if len(all_reviews) <= max_count:
        return list(all_reviews)

    by_store: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in all_reviews:
        by_store[str(r.get("store", ""))].append(r)

    for store in by_store:
        by_store[store].sort(key=lambda r: r.get("date", ""), reverse=True)

    stores = sorted(by_store.keys())
    totals = {s: len(by_store[s]) for s in stores}
    grand = sum(totals.values())

    caps: dict[str, int] = {}
    assigned = 0
    for i, store in enumerate(stores):
        if i == len(stores) - 1:
            caps[store] = max_count - assigned
        else:
            share = int(round(max_count * totals[store] / grand))
            caps[store] = share
            assigned += share

    sampled: list[dict[str, Any]] = []
    for store in stores:
        sampled.extend(by_store[store][: caps[store]])

    if len(sampled) > max_count:
        sampled.sort(key=lambda r: r.get("date", ""), reverse=True)
        sampled = sampled[:max_count]

    return sampled


def write_sample(
    config: Phase2Config,
    *,
    force: bool = False,
) -> dict[str, Any]:
    if not config.normalized_path.is_file():
        raise FileNotFoundError(f"Missing normalized reviews: {config.normalized_path}")

    if config.sample_path.is_file() and not force:
        existing = load_jsonl(config.sample_path)
        logger.info("Sample already exists (%s rows); use force=True to resample", len(existing))
        return {
            "source_count": len(load_jsonl(config.normalized_path)),
            "sample_count": len(existing),
            "skipped": True,
        }

    all_reviews = load_jsonl(config.normalized_path)
    sampled = sample_reviews(all_reviews, config.max_reviews_per_run)
    write_jsonl(config.sample_path, sampled)

    meta = {
        "sampled_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_count": len(all_reviews),
        "sample_count": len(sampled),
        "max_reviews_per_run": config.max_reviews_per_run,
        "by_store": _count_by_store(sampled),
    }
    logger.info(
        "Sampled %s / %s reviews → %s",
        len(sampled),
        len(all_reviews),
        config.sample_path,
    )
    return meta


def _count_by_store(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for r in rows:
        out[str(r.get("store", "unknown"))] += 1
    return dict(out)
