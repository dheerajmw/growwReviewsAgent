#!/usr/bin/env python3
"""Publish Phase 3 note to Google Doc via deployed MCP server (Phase 5)."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase5_docs_mcp.run import main

if __name__ == "__main__":
    raise SystemExit(main())
