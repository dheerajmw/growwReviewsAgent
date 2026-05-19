#!/usr/bin/env python3
"""Sample reviews for Phase 2 (rate-limit safe subset)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase2_themes.themes.config import Phase2Config
from pipelines.phase2_themes.themes.sample import write_sample


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--config", type=Path, default=None)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = Phase2Config.load(args.config)
    meta = write_sample(config, force=args.force)
    logging.info("Done: %s", meta)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
