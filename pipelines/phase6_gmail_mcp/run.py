#!/usr/bin/env python3
"""Phase 6 CLI — Gmail draft via HTTP MCP server."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pipelines.phase5_docs_mcp.docs.client import health_check, list_tools
from pipelines.phase6_gmail_mcp.gmail.config import Phase6Config
from pipelines.phase6_gmail_mcp.gmail.draft import run_draft


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phase 6: create Gmail draft via MCP HTTP server (create_email_draft)",
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--force", action="store_true", help="Create draft even if same week exists")
    parser.add_argument("--dry-run", action="store_true", help="Update publish_state without MCP call")
    parser.add_argument("--skip-pii", action="store_true", help="Skip Phase 4 gate (not for production)")
    parser.add_argument("--health", action="store_true", help="Only check MCP server health")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    cfg = Phase6Config.load(args.config)

    if args.health:
        info = health_check(cfg.mcp_server_url)
        tools = list_tools(cfg.mcp_server_url)
        logging.info("MCP OK: %s tools=%s", info, tools)
        return 0

    try:
        out = run_draft(cfg, force=args.force, dry_run=args.dry_run, skip_pii=args.skip_pii)
        logging.info("Updated %s", out)
        return 0
    except Exception as exc:
        logging.error("%s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
