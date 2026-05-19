from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "phase6_gmail.yaml"


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    env_path = REPO_ROOT / ".env"
    if env_path.is_file():
        load_dotenv(env_path)


@dataclass
class Phase6Config:
    mcp_server_url: str = "https://mcp-server-p01x.onrender.com"
    note_md_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/note.md")
    publish_state_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/publish_state.json")
    blockers_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/blockers.json")
    draft_to: str | None = None
    skip_if_same_week: bool = True
    subject_prefix: str = "Groww Weekly Review Pulse"

    @classmethod
    def load(cls, path: Path | None = None) -> Phase6Config:
        _load_dotenv()
        config_path = path or DEFAULT_CONFIG_PATH
        raw: dict[str, Any] = {}
        if config_path.is_file():
            with config_path.open(encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}

        paths = raw.get("paths") or {}
        draft_cfg = raw.get("draft") or {}
        to_addr = (os.environ.get("PULSE_DRAFT_TO") or raw.get("draft_to") or "").strip() or None

        url = (os.environ.get("MCP_SERVER_URL") or raw.get("mcp_server_url") or "").strip()
        if not url:
            url = "https://mcp-server-p01x.onrender.com"

        return cls(
            mcp_server_url=url.rstrip("/"),
            note_md_path=REPO_ROOT / paths.get("note_md", "data/weekly/note.md"),
            publish_state_path=REPO_ROOT / paths.get("publish_state", "data/weekly/publish_state.json"),
            blockers_path=REPO_ROOT / paths.get("blockers", "data/weekly/blockers.json"),
            draft_to=to_addr,
            skip_if_same_week=bool(draft_cfg.get("skip_if_same_week", True)),
            subject_prefix=str(draft_cfg.get("subject_prefix", "Groww Weekly Review Pulse")),
        )
