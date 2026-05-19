#!/usr/bin/env python3
"""
PII sanitization gate (Phase 4).

Scans weekly note text for:
  - email addresses
  - phone numbers
  - @handles (social/reviewer handles)
  - long numeric IDs (>=10 consecutive digits)
  - review_id literals and app_store:/play_store: prefixes

On failure writes data/weekly/blockers.json and exits non-zero (blocks MCP publish).

Usage:
  python scripts/check_pii.py data/weekly/note.md
  echo 'Contact user@example.com' | python scripts/check_pii.py -
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase4_pii.run import main

if __name__ == "__main__":
    raise SystemExit(main())
