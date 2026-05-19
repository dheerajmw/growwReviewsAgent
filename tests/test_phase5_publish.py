from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]


def test_format_and_dry_run_publish(tmp_path: Path):
    from pipelines.phase5_docs_mcp.docs.config import Phase5Config
    from pipelines.phase5_docs_mcp.docs.publish import publish_weekly_doc

    note = tmp_path / "note.md"
    note.write_text(
        "# Groww — Weekly Review Pulse (2026-05-19)\n\n## Top themes\n1. Payments\n",
        encoding="utf-8",
    )
    state_path = tmp_path / "publish_state.json"

    cfg = Phase5Config(
        mcp_server_url="https://example.com",
        note_md_path=note,
        publish_state_path=state_path,
        doc_id="abc123doc",
        skip_if_same_week=False,
    )

    state = publish_weekly_doc(cfg, dry_run=True, skip_pii=True)
    assert state["doc_id"] == "abc123doc"
    assert state["doc_url"] == "https://docs.google.com/document/d/abc123doc/edit"
    assert "published_at" in state
    assert state["week_ending"] == "2026-05-19"

    on_disk = json.loads(state_path.read_text())
    assert all(k in on_disk for k in ("doc_id", "doc_url", "published_at"))


def test_same_week_skip(tmp_path: Path):
    from pipelines.phase5_docs_mcp.docs.config import Phase5Config
    from pipelines.phase5_docs_mcp.docs.publish import publish_weekly_doc, write_publish_state

    note = tmp_path / "note.md"
    note.write_text("# Groww — Weekly Review Pulse (2026-05-19)\n", encoding="utf-8")
    state_path = tmp_path / "publish_state.json"

    write_publish_state(
        state_path,
        doc_id="abc123doc",
        doc_url="https://docs.google.com/document/d/abc123doc/edit",
        week_ending="2026-05-19",
        mcp_response={"status": "success"},
        mcp_server="https://example.com",
    )

    cfg = Phase5Config(
        mcp_server_url="https://example.com",
        note_md_path=note,
        publish_state_path=state_path,
        doc_id="abc123doc",
        skip_if_same_week=True,
    )

    with patch("pipelines.phase5_docs_mcp.docs.publish.append_to_doc") as mock_append:
        state = publish_weekly_doc(cfg, skip_pii=True)
        mock_append.assert_not_called()
    assert state.get("skipped") is True


def test_no_googleapis_in_phase5():
    root = REPO / "pipelines" / "phase5_docs_mcp"
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*.py"))
    assert "googleapiclient" not in text
    assert "google.docs" not in text.lower()
