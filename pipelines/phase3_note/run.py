#!/usr/bin/env python3
"""Phase 3 CLI — generate weekly note from ranked themes."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pipelines.phase3_note.note.config import Phase3Config
from pipelines.phase3_note.note.generate import run_generate
from pipelines.phase3_note.note.validate import validate_note


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 3: weekly note generation (Groq)")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true", help="Heuristic note without Groq API")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    config = Phase3Config.load(args.config)

    if args.validate_only:
        errors, summary = validate_note(config)
        if errors:
            for e in errors:
                logging.error("%s", e)
            return 1
        logging.info("Validation OK: %s", summary)
        return 0

    out = run_generate(config, dry_run=args.dry_run)
    logging.info("Wrote %s", out)

    errors, summary = validate_note(config)
    if errors:
        for e in errors:
            logging.error("%s", e)
        return 1
    logging.info("Validation OK: %s", summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
