from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]


def test_dry_run_draft(tmp_path: Path):
    from pipelines.phase6_gmail_mcp.gmail.config import Phase6Config
    from pipelines.phase6_gmail_mcp.gmail.draft import create_gmail_draft

    note = tmp_path / "note.md"
    note.write_text("# Groww — Weekly Review Pulse (2026-05-19)\n\nBody\n", encoding="utf-8")
    state_path = tmp_path / "publish_state.json"

    cfg = Phase6Config(
        mcp_server_url="https://example.com",
        note_md_path=note,
        publish_state_path=state_path,
        draft_to="test@example.com",
        skip_if_same_week=False,
    )

    state = create_gmail_draft(cfg, dry_run=True, skip_pii=True)
    assert state["draft_id"]
    assert state["draft_to"] == "test@example.com"
    assert "draft_created_at" in state

    on_disk = json.loads(state_path.read_text())
    assert "draft_id" in on_disk


def test_no_gmail_api_in_phase6():
    root = REPO / "pipelines" / "phase6_gmail_mcp"
    text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*.py"))
    assert "googleapiclient" not in text
    assert "gmail.googleapis" not in text


def test_create_draft_payload():
    from pipelines.phase6_gmail_mcp.gmail.client import create_email_draft

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_resp = mock_urlopen.return_value.__enter__.return_value
        mock_resp.read.return_value = json.dumps(
            {"status": "success", "draft_id": "draft123"}
        ).encode()

        result = create_email_draft(
            "https://example.com",
            to="a@b.com",
            subject="Test",
            body="Hello",
        )
        assert result["draft_id"] == "draft123"
