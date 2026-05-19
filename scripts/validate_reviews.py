#!/usr/bin/env python3
"""Validate normalized review JSONL (Phase 1)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pipelines.phase1_ingest.ingest.config import IngestConfig
from pipelines.phase1_ingest.ingest.validate import validate_normalized_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate data/reviews/normalized.jsonl")
    parser.add_argument("--path", type=Path, default=None, help="JSONL path (default from config)")
    parser.add_argument("--min-rows", type=int, default=1)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = IngestConfig.load()
    path = args.path or config.output

    errors, summary = validate_normalized_file(path, min_rows=args.min_rows)
    if errors:
        for err in errors:
            logging.error("%s", err)
        return 1

    logging.info("Validation OK: %s", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
