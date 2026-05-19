#!/usr/bin/env python3
"""Run full weekly Groww review pulse pipeline (Phase 7)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase7_e2e.e2e.run_weekly import main

if __name__ == "__main__":
    raise SystemExit(main())
