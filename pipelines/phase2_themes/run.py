#!/usr/bin/env python3
"""Phase 2 CLI — sample, Groq cluster, rank, validate."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pipelines.phase2_themes.themes.cluster import run_clustering
from pipelines.phase2_themes.themes.config import Phase2Config
from pipelines.phase2_themes.themes.rank import write_ranked
from pipelines.phase2_themes.themes.sample import write_sample
from pipelines.phase2_themes.themes.validate import validate_all


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2: theme clustering (Groq)")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--sample-only", action="store_true")
    parser.add_argument("--cluster-only", action="store_true")
    parser.add_argument("--resample", action="store_true", help="Force new phase2_sample.jsonl")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Heuristic themes only (no Groq calls)",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    level = logging.INFO
    if args.verbose:
        level = logging.INFO
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai").setLevel(logging.WARNING)
        logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.basicConfig(level=level, format="%(levelname)s %(message)s")

    config = Phase2Config.load(args.config)

    if not args.cluster_only:
        write_sample(config, force=args.resample)

    if args.sample_only:
        return 0

    clusters = run_clustering(config, dry_run=args.dry_run)
    write_ranked(clusters, config)

    errors, summary = validate_all(config)
    if errors:
        for e in errors:
            logging.error("Validation: %s", e)
        return 1

    logging.info("Phase 2 validation OK: %s", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
