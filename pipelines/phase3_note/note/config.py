from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "phase3_note.yaml"


@dataclass
class Phase3Config:
    model: str = "llama-3.3-70b-versatile"
    max_words: int = 250
    temperature: float = 0.3
    max_tokens: int = 2048
    ranked_path: Path = field(default_factory=lambda: REPO_ROOT / "data/themes/ranked.json")
    clusters_path: Path = field(default_factory=lambda: REPO_ROOT / "data/themes/clusters.json")
    sample_path: Path = field(default_factory=lambda: REPO_ROOT / "data/reviews/phase2_sample.jsonl")
    note_md_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/note.md")
    note_json_path: Path = field(default_factory=lambda: REPO_ROOT / "data/weekly/note.json")
    system_prompt_path: Path = field(default_factory=lambda: REPO_ROOT / "prompts/system.md")
    weekly_prompt_path: Path = field(default_factory=lambda: REPO_ROOT / "prompts/weekly_note.md")
    candidates_per_theme: int = 8
    prefer_low_ratings: bool = True

    @classmethod
    def load(cls, path: Path | None = None) -> Phase3Config:
        config_path = path or DEFAULT_CONFIG_PATH
        if not config_path.is_file():
            return cls()
        with config_path.open(encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}
        paths = raw.get("paths") or {}
        qs = raw.get("quote_selection") or {}
        return cls(
            model=str(raw.get("model", "llama-3.3-70b-versatile")),
            max_words=int(raw.get("max_words", 250)),
            temperature=float(raw.get("temperature", 0.3)),
            max_tokens=int(raw.get("max_tokens", 2048)),
            ranked_path=REPO_ROOT / paths.get("ranked", "data/themes/ranked.json"),
            clusters_path=REPO_ROOT / paths.get("clusters", "data/themes/clusters.json"),
            sample_path=REPO_ROOT / paths.get("sample", "data/reviews/phase2_sample.jsonl"),
            note_md_path=REPO_ROOT / paths.get("note_md", "data/weekly/note.md"),
            note_json_path=REPO_ROOT / paths.get("note_json", "data/weekly/note.json"),
            system_prompt_path=REPO_ROOT / paths.get("system_prompt", "prompts/system.md"),
            weekly_prompt_path=REPO_ROOT / paths.get("weekly_prompt", "prompts/weekly_note.md"),
            candidates_per_theme=int(qs.get("candidates_per_theme", 8)),
            prefer_low_ratings=bool(qs.get("prefer_low_ratings", True)),
        )
