#!/usr/bin/env python3
"""Ingest App Store & Play Store review exports (Phase 1 entry point)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pipelines.phase1_ingest.run import main

if __name__ == "__main__":
    raise SystemExit(main())
