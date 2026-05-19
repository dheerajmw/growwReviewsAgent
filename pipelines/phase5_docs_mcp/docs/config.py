from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "phase5_docs.yaml"


def _load_dotenv() -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    env_path = REPO_ROOT / ".env"
    if env_path.is_file():
        load_dotenv(env_path)


@dataclass
class Phase5Config:
    mcp_server_url: str = "https://mcp-server-p01x.onrender.com"
    note_md_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/note.md")
    publish_state_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/publish_state.json")
    blockers_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/blockers.json")
    doc_id: str | None = None
    skip_if_same_week: bool = True
    title_prefix: str = "Weekly Review Pulse — Groww"

    @classmethod
    def load(cls, path: Path | None = None) -> Phase5Config:
        _load_dotenv()
        config_path = path or DEFAULT_CONFIG_PATH
        raw: dict[str, Any] = {}
        if config_path.is_file():
            with config_path.open(encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}

        paths = raw.get("paths") or {}
        pub = raw.get("publish") or {}
        doc_id = (os.environ.get("GROWW_PULSE_DOC_ID") or raw.get("doc_id") or "").strip() or None

        url = (os.environ.get("MCP_SERVER_URL") or raw.get("mcp_server_url") or "").strip()
        if not url:
            url = "https://mcp-server-p01x.onrender.com"

        return cls(
            mcp_server_url=url.rstrip("/"),
            note_md_path=REPO_ROOT / paths.get("note_md", "data/weekly/note.md"),
            publish_state_path=REPO_ROOT / paths.get("publish_state", "data/weekly/publish_state.json"),
            blockers_path=REPO_ROOT / paths.get("blockers", "data/weekly/blockers.json"),
            doc_id=doc_id,
            skip_if_same_week=bool(pub.get("skip_if_same_week", True)),
            title_prefix=str(pub.get("title_prefix", "Weekly Review Pulse — Groww")),
        )

    def doc_url(self, doc_id: str | None = None) -> str:
        did = doc_id or self.doc_id or ""
        return f"https://docs.google.com/document/d/{did}/edit"
