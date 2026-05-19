#!/usr/bin/env python3
"""Phase 5 CLI — publish note.md to Google Doc via HTTP MCP server."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pipelines.phase5_docs_mcp.docs.client import health_check, list_tools
from pipelines.phase5_docs_mcp.docs.config import Phase5Config
from pipelines.phase5_docs_mcp.docs.publish import run_publish


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Phase 5: publish weekly note via MCP HTTP server (append_to_doc)",
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--force", action="store_true", help="Append even if same week already published")
    parser.add_argument("--dry-run", action="store_true", help="Write publish_state without calling MCP")
    parser.add_argument("--skip-pii", action="store_true", help="Skip Phase 4 gate (not for production)")
    parser.add_argument("--health", action="store_true", help="Only check MCP server health")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    cfg = Phase5Config.load(args.config)

    if args.health:
        info = health_check(cfg.mcp_server_url)
        tools = list_tools(cfg.mcp_server_url)
        logging.info("MCP OK: %s tools=%s", info, tools)
        return 0

    try:
        out = run_publish(cfg, force=args.force, dry_run=args.dry_run, skip_pii=args.skip_pii)
        logging.info("Wrote %s", out)
        return 0
    except Exception as exc:
        logging.error("%s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
