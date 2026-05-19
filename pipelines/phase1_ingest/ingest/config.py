from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "phase1_ingest.yaml"

CANONICAL_FIELDS = ("rating", "title", "text", "date", "store", "review_id")


@dataclass
class NormalizationConfig:
    min_words: int = 6
    english_only: bool = True
    reject_emoji: bool = True


@dataclass
class IngestConfig:
    weeks: int = 12
    min_weeks: int = 8
    raw_dir: Path = field(default_factory=lambda: REPO_ROOT / "data" / "raw")
    app_store_glob: str = "app_store*"
    play_store_glob: str = "play_store*"
    output: Path = field(default_factory=lambda: REPO_ROOT / "data" / "reviews" / "normalized.jsonl")
    column_aliases: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    normalization: NormalizationConfig = field(default_factory=NormalizationConfig)

    @classmethod
    def load(cls, path: Path | None = None) -> IngestConfig:
        config_path = path or DEFAULT_CONFIG_PATH
        if not config_path.is_file():
            return cls()
        with config_path.open(encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}
        paths = raw.get("paths") or {}
        norm_raw = raw.get("normalization") or {}
        normalization = NormalizationConfig(
            min_words=int(norm_raw.get("min_words", 6)),
            english_only=bool(norm_raw.get("english_only", True)),
            reject_emoji=bool(norm_raw.get("reject_emoji", True)),
        )
        return cls(
            weeks=int(raw.get("weeks", 12)),
            min_weeks=int(raw.get("min_weeks", 8)),
            raw_dir=REPO_ROOT / paths.get("raw_dir", "data/raw"),
            app_store_glob=str(paths.get("app_store_glob", "app_store*")),
            play_store_glob=str(paths.get("play_store_glob", "play_store*")),
            output=REPO_ROOT / paths.get("output", "data/reviews/normalized.jsonl"),
            column_aliases=raw.get("column_aliases") or {},
            normalization=normalization,
        )
