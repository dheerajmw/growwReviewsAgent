#!/usr/bin/env python3
"""Create Gmail draft for weekly pulse via MCP server (Phase 6). Draft only — never sends."""

from __future__ import annotations

import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))

from pipelines.phase6_gmail_mcp.run import main

if __name__ == "__main__":
    raise SystemExit(main())
