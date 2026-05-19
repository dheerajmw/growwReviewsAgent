from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipelines.phase4_pii.pii.gate import run_pii_gate

from .client import McpServerError, append_to_doc, health_check
from .config import Phase5Config

logger = logging.getLogger(__name__)

DATE_IN_TITLE = re.compile(r"\((\d{4}-\d{2}-\d{2})\)")


def extract_week_ending(note_md: str) -> str:
    for line in note_md.splitlines():
        m = DATE_IN_TITLE.search(line)
        if m:
            return m.group(1)
    return datetime.now(timezone.utc).date().isoformat()


def format_publish_body(note_md: str, cfg: Phase5Config, week_ending: str) -> str:
    title_line = f"{cfg.title_prefix} — {week_ending}"
    body = note_md.strip()
    if not body.startswith("#"):
        body = f"# {title_line}\n\n{body}"
    return f"{title_line}\n\n---\n\n{body}\n"


def load_publish_state(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_publish_state(
    path: Path,
    *,
    doc_id: str,
    doc_url: str,
    week_ending: str,
    mcp_response: dict[str, Any],
    mcp_server: str,
    skipped: bool = False,
) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "doc_id": doc_id,
        "doc_url": doc_url,
        "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "week_ending": week_ending,
        "skipped": skipped,
        "mcp_server": mcp_server,
        "mcp_response": mcp_response,
    }
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return state


def ensure_pii_gate(cfg: Phase5Config) -> None:
    if cfg.blockers_path.is_file():
        blockers = json.loads(cfg.blockers_path.read_text(encoding="utf-8"))
        if blockers.get("publish_blocked"):
            raise RuntimeError(
                f"PII gate blocked publish; fix note and re-run check_pii.py ({cfg.blockers_path})"
            )

    result = run_pii_gate(cfg.note_md_path, write_blockers_file=True)
    if not result.passed:
        raise RuntimeError(
            "PII check failed on note.md; run: python scripts/check_pii.py data/weekly/note.md"
        )


def publish_weekly_doc(
    config: Phase5Config | None = None,
    *,
    force: bool = False,
    dry_run: bool = False,
    skip_pii: bool = False,
) -> dict[str, Any]:
    cfg = config or Phase5Config.load()

    if not cfg.note_md_path.is_file():
        raise FileNotFoundError(f"Missing note: {cfg.note_md_path}")

    if not skip_pii:
        ensure_pii_gate(cfg)

    if not cfg.doc_id:
        raise RuntimeError(
            "GROWW_PULSE_DOC_ID is not set. Create a Google Doc, copy the ID from the URL "
            "(.../document/d/DOC_ID/edit), and set GROWW_PULSE_DOC_ID in .env"
        )

    note_md = cfg.note_md_path.read_text(encoding="utf-8")
    week_ending = extract_week_ending(note_md)
    doc_url = cfg.doc_url(cfg.doc_id)

    prev = load_publish_state(cfg.publish_state_path)
    if (
        cfg.skip_if_same_week
        and not force
        and prev
        and prev.get("week_ending") == week_ending
        and prev.get("doc_id") == cfg.doc_id
        and not prev.get("skipped")
    ):
        logger.info("Already published for week %s; use --force to append again", week_ending)
        return write_publish_state(
            cfg.publish_state_path,
            doc_id=cfg.doc_id,
            doc_url=doc_url,
            week_ending=week_ending,
            mcp_response={"status": "skipped", "message": "same week already published"},
            mcp_server=cfg.mcp_server_url,
            skipped=True,
        )

    content = format_publish_body(note_md, cfg, week_ending)

    if dry_run:
        return write_publish_state(
            cfg.publish_state_path,
            doc_id=cfg.doc_id,
            doc_url=doc_url,
            week_ending=week_ending,
            mcp_response={"status": "dry_run", "content_preview": content[:200]},
            mcp_server=cfg.mcp_server_url,
            skipped=False,
        )

    logger.info("Checking MCP server %s", cfg.mcp_server_url)
    health_check(cfg.mcp_server_url)

    logger.info("Appending to doc_id=%s via MCP", cfg.doc_id)
    response = append_to_doc(cfg.mcp_server_url, doc_id=cfg.doc_id, content=content)

    if response.get("status") == "rejected":
        raise McpServerError(response.get("message", "MCP action rejected"))

    if response.get("status") not in ("success", None):
        if "error" in str(response.get("status", "")).lower():
            raise McpServerError(str(response))

    return write_publish_state(
        cfg.publish_state_path,
        doc_id=cfg.doc_id,
        doc_url=doc_url,
        week_ending=week_ending,
        mcp_response=response,
        mcp_server=cfg.mcp_server_url,
        skipped=False,
    )


def run_publish(
    config: Phase5Config | None = None,
    *,
    force: bool = False,
    dry_run: bool = False,
    skip_pii: bool = False,
) -> Path:
    state = publish_weekly_doc(config, force=force, dry_run=dry_run, skip_pii=skip_pii)
    cfg = config or Phase5Config.load()
    logger.info("Publish state: doc_url=%s week=%s skipped=%s", state["doc_url"], state["week_ending"], state.get("skipped"))
    return cfg.publish_state_path
