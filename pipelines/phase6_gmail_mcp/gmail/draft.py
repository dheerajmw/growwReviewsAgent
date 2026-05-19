from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipelines.phase4_pii.pii.gate import run_pii_gate
from pipelines.phase5_docs_mcp.docs.client import health_check
from pipelines.phase5_docs_mcp.docs.publish import extract_week_ending, load_publish_state

from .client import McpServerError, create_email_draft
from .config import Phase6Config

logger = logging.getLogger(__name__)

DRAFTS_URL = "https://mail.google.com/mail/u/0/#drafts"


def ensure_pii_gate(cfg: Phase6Config) -> None:
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


def merge_publish_state(path: Path, updates: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    state: dict[str, Any] = {}
    if path.is_file():
        state = json.loads(path.read_text(encoding="utf-8"))
    state.update(updates)
    path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return state


def format_email_body(note_md: str, week_ending: str, doc_url: str | None) -> str:
    lines = [note_md.strip(), ""]
    if doc_url:
        lines.append(f"Google Doc: {doc_url}")
    lines.append(f"Week ending: {week_ending}")
    return "\n".join(lines)


def create_gmail_draft(
    config: Phase6Config | None = None,
    *,
    force: bool = False,
    dry_run: bool = False,
    skip_pii: bool = False,
) -> dict[str, Any]:
    cfg = config or Phase6Config.load()

    if not cfg.note_md_path.is_file():
        raise FileNotFoundError(f"Missing note: {cfg.note_md_path}")

    if not skip_pii:
        ensure_pii_gate(cfg)

    if not cfg.draft_to:
        raise RuntimeError(
            "PULSE_DRAFT_TO is not set. Add your email to .env, e.g. PULSE_DRAFT_TO=you@example.com"
        )

    note_md = cfg.note_md_path.read_text(encoding="utf-8")
    week_ending = extract_week_ending(note_md)
    subject = f"{cfg.subject_prefix} — {week_ending}"

    prev = load_publish_state(cfg.publish_state_path) or {}
    doc_url = prev.get("doc_url")

    if (
        cfg.skip_if_same_week
        and not force
        and prev.get("week_ending") == week_ending
        and prev.get("draft_id")
        and prev.get("draft_to") == cfg.draft_to
        and not prev.get("draft_skipped")
    ):
        logger.info("Draft already created for week %s; use --force to create again", week_ending)
        return merge_publish_state(
            cfg.publish_state_path,
            {
                "draft_skipped": True,
                "draft_id": prev["draft_id"],
                "draft_to": cfg.draft_to,
                "draft_url": prev.get("draft_url", DRAFTS_URL),
            },
        )

    body = format_email_body(note_md, week_ending, doc_url)

    if dry_run:
        return merge_publish_state(
            cfg.publish_state_path,
            {
                "week_ending": week_ending,
                "draft_to": cfg.draft_to,
                "draft_id": "dry-run-draft-id",
                "draft_url": DRAFTS_URL,
                "draft_created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "draft_skipped": False,
                "gmail_mcp_response": {"status": "dry_run", "subject": subject},
            },
        )

    logger.info("Checking MCP server %s", cfg.mcp_server_url)
    health_check(cfg.mcp_server_url)

    logger.info("Creating Gmail draft to=%s subject=%s", cfg.draft_to, subject)
    response = create_email_draft(
        cfg.mcp_server_url,
        to=cfg.draft_to,
        subject=subject,
        body=body,
    )

    if response.get("status") == "rejected":
        raise McpServerError(response.get("message", "MCP action rejected"))

    if response.get("status") == "error":
        raise McpServerError(str(response))

    draft_id = response.get("draft_id")
    if not draft_id and response.get("status") != "success":
        raise McpServerError(f"Unexpected MCP response: {response}")

    return merge_publish_state(
        cfg.publish_state_path,
        {
            "week_ending": week_ending,
            "draft_to": cfg.draft_to,
            "draft_id": draft_id,
            "draft_url": DRAFTS_URL,
            "draft_created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "draft_skipped": False,
            "gmail_mcp_response": response,
        },
    )


def run_draft(
    config: Phase6Config | None = None,
    *,
    force: bool = False,
    dry_run: bool = False,
    skip_pii: bool = False,
) -> Path:
    state = create_gmail_draft(config, force=force, dry_run=dry_run, skip_pii=skip_pii)
    cfg = config or Phase6Config.load()
    logger.info(
        "Draft: to=%s draft_id=%s skipped=%s",
        state.get("draft_to"),
        state.get("draft_id"),
        state.get("draft_skipped"),
    )
    return cfg.publish_state_path
