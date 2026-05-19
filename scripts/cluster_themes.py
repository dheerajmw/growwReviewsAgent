#!/usr/bin/env python3
"""Run Phase 2 Groq theme clustering + ranking."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase2_themes.run import main

if __name__ == "__main__":
    raise SystemExit(main())
