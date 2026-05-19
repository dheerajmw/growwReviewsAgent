#!/usr/bin/env python3
"""Phase 1 CLI — ingest public review exports to normalized JSONL."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow running as `python pipelines/phase1_ingest/run.py`
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pipelines.phase1_ingest.ingest.config import IngestConfig
from pipelines.phase1_ingest.ingest.pipeline import run_ingest
from pipelines.phase1_ingest.ingest.validate import validate_normalized_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 1: ingest App Store & Play Store reviews")
    parser.add_argument("--weeks", type=int, default=None, help="Rolling window (8–12, default from config)")
    parser.add_argument("--config", type=Path, default=None, help="Path to phase1_ingest.yaml")
    parser.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip post-ingest validation (default: validate)",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    config = IngestConfig.load(args.config)
    try:
        stats = run_ingest(config=config, weeks=args.weeks)
    except FileNotFoundError as exc:
        logging.error("%s", exc)
        return 1
    except ValueError as exc:
        logging.error("%s", exc)
        return 1

    if not args.no_validate:
        errors, summary = validate_normalized_file(config.output)
        if errors:
            for err in errors:
                logging.error("Validation: %s", err)
            return 1
        logging.info("Validation OK: %s", summary)

    if stats.rows_written == 0:
        logging.error("No reviews written — check raw exports and date window")
        return 1

    logging.info("Wrote %s", config.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
