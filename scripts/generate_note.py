#!/usr/bin/env python3
"""Generate Phase 3 weekly note (Groq)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase3_note.run import main

if __name__ == "__main__":
    raise SystemExit(main())
