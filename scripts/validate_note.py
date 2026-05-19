#!/usr/bin/env python3
"""Validate Phase 3 weekly note artifacts."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase3_note.note.config import Phase3Config
from pipelines.phase3_note.note.validate import validate_note


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    config = Phase3Config.load()
    errors, summary = validate_note(config)
    if errors:
        for e in errors:
            logging.error("%s", e)
        return 1
    logging.info("Validation OK: %s", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
