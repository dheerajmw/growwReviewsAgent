from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .config import IngestConfig
from .filters import content_filter_reason
from .parsers import STORE_APP, STORE_PLAY, discover_raw_files, iter_source_rows, parse_row

logger = logging.getLogger(__name__)


@dataclass
class IngestStats:
    files_read: int = 0
    rows_read: int = 0
    rows_in_window: int = 0
    rows_out_of_window: int = 0
    rows_invalid: dict[str, int] = field(default_factory=dict)
    rows_filtered: dict[str, int] = field(default_factory=dict)
    rows_deduped: int = 0
    rows_written: int = 0

    def log_summary(self) -> None:
        logger.info("=== Phase 1 ingest summary ===")
        logger.info("Files read: %s", self.files_read)
        logger.info("Rows read: %s", self.rows_read)
        logger.info("In window: %s", self.rows_in_window)
        logger.info("Out of window: %s", self.rows_out_of_window)
        logger.info("Invalid: %s", dict(self.rows_invalid))
        logger.info("Filtered (normalization): %s", dict(self.rows_filtered))
        logger.info("Deduped: %s", self.rows_deduped)
        logger.info("Written: %s", self.rows_written)


def _window_bounds(weeks: int, reference: datetime | None = None) -> tuple[datetime, datetime]:
    ref = reference or datetime.now(timezone.utc)
    start = ref - timedelta(weeks=weeks)
    return start, ref


def _in_window(iso_date: str, start: datetime, end: datetime) -> bool:
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return start <= dt <= end


def _ingest_files(
    paths: list[Path],
    store: str,
    config: IngestConfig,
    start: datetime,
    end: datetime,
    stats: IngestStats,
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in paths:
        stats.files_read += 1
        logger.info("Reading %s (%s)", path.name, store)
        try:
            rows = list(iter_source_rows(path))
        except Exception as exc:
            logger.error("Failed to read %s: %s", path, exc)
            raise
        for row in rows:
            stats.rows_read += 1
            record, skip = parse_row(row, store, config)
            if skip:
                stats.rows_invalid[skip] = stats.rows_invalid.get(skip, 0) + 1
                logger.debug("Skip row in %s: %s", path.name, skip)
                continue
            assert record is not None
            if not _in_window(record["date"], start, end):
                stats.rows_out_of_window += 1
                continue
            stats.rows_in_window += 1

            norm = config.normalization
            filter_reason = content_filter_reason(
                record,
                min_words=norm.min_words,
                english_only=norm.english_only,
                reject_emoji=norm.reject_emoji,
            )
            if filter_reason:
                stats.rows_filtered[filter_reason] = stats.rows_filtered.get(filter_reason, 0) + 1
                logger.debug("Filtered row in %s: %s", path.name, filter_reason)
                continue

            records.append(record)
    return records


def run_ingest(
    config: IngestConfig | None = None,
    weeks: int | None = None,
    reference: datetime | None = None,
) -> IngestStats:
    cfg = config or IngestConfig.load()
    window_weeks = weeks if weeks is not None else cfg.weeks
    if window_weeks < cfg.min_weeks or window_weeks > 12:
        raise ValueError(f"weeks must be between {cfg.min_weeks} and 12 (got {window_weeks})")

    start, end = _window_bounds(window_weeks, reference)
    stats = IngestStats()

    app_files = discover_raw_files(cfg.raw_dir, cfg.app_store_glob)
    play_files = discover_raw_files(cfg.raw_dir, cfg.play_store_glob)

    if not app_files:
        raise FileNotFoundError(
            f"No App Store export found in {cfg.raw_dir} matching {cfg.app_store_glob}"
        )
    if not play_files:
        raise FileNotFoundError(
            f"No Play Store export found in {cfg.raw_dir} matching {cfg.play_store_glob}"
        )

    all_records: list[dict[str, Any]] = []
    all_records.extend(_ingest_files(app_files, STORE_APP, cfg, start, end, stats))
    all_records.extend(_ingest_files(play_files, STORE_PLAY, cfg, start, end, stats))

    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for rec in sorted(all_records, key=lambda r: r["date"]):
        rid = rec["review_id"]
        if rid in seen:
            stats.rows_deduped += 1
            continue
        seen.add(rid)
        unique.append(rec)

    cfg.output.parent.mkdir(parents=True, exist_ok=True)
    with cfg.output.open("w", encoding="utf-8") as f:
        for rec in unique:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            stats.rows_written += 1

    stats.log_summary()
    return stats
