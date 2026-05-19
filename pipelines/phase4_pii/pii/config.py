from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "phase4_pii.yaml"


@dataclass
class Phase4Config:
    note_md_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/note.md")
    note_json_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/note.json")
    blockers_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/blockers.json")
    redact_prompt_path: Path = field(default_factory=lambda: REPO_ROOT / "prompts/pii_redact.md")
    name_blocklist_path: Path | None = None
    min_numeric_id_length: int = 10
    redact_model: str = "llama-3.3-70b-versatile"
    redact_temperature: float = 0.2
    redact_max_tokens: int = 2048

    @classmethod
    def load(cls, path: Path | None = None) -> Phase4Config:
        config_path = path or DEFAULT_CONFIG_PATH
        if not config_path.is_file():
            return cls()
        with config_path.open(encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}
        paths = raw.get("paths") or {}
        scan = raw.get("scan") or {}
        redact = raw.get("redact") or {}
        blocklist = raw.get("name_blocklist")
        block_path = Path(blocklist) if blocklist else None
        if block_path and not block_path.is_absolute():
            block_path = REPO_ROOT / block_path
        return cls(
            note_md_path=REPO_ROOT / paths.get("note_md", "data/weekly/note.md"),
            note_json_path=REPO_ROOT / paths.get("note_json", "data/weekly/note.json"),
            blockers_path=REPO_ROOT / paths.get("blockers", "data/weekly/blockers.json"),
            redact_prompt_path=REPO_ROOT / paths.get("redact_prompt", "prompts/pii_redact.md"),
            name_blocklist_path=block_path if block_path and block_path.is_file() else None,
            min_numeric_id_length=int(scan.get("min_numeric_id_length", 10)),
            redact_model=str(redact.get("model", "llama-3.3-70b-versatile")),
            redact_temperature=float(redact.get("temperature", 0.2)),
            redact_max_tokens=int(redact.get("max_tokens", 2048)),
        )
