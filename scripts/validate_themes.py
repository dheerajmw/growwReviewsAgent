#!/usr/bin/env python3
"""Validate Phase 2 theme artifacts."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase2_themes.themes.config import Phase2Config
from pipelines.phase2_themes.themes.validate import validate_all


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = Phase2Config.load()
    errors, summary = validate_all(config)
    if errors:
        for e in errors:
            logging.error("%s", e)
        return 1
    logging.info("Validation OK: %s", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
