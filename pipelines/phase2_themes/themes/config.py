from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = REPO_ROOT / "configs" / "phase2_themes.yaml"


@dataclass
class ThemeDef:
    id: str
    label: str


@dataclass
class Phase2Config:
    model: str = "llama-3.3-70b-versatile"
    normalized_path: Path = field(default_factory=lambda: REPO_ROOT / "data/reviews/normalized.jsonl")
    sample_path: Path = field(default_factory=lambda: REPO_ROOT / "data/reviews/phase2_sample.jsonl")
    clusters_path: Path = field(default_factory=lambda: REPO_ROOT / "data/themes/clusters.json")
    ranked_path: Path = field(default_factory=lambda: REPO_ROOT / "data/themes/ranked.json")
    prompts_path: Path = field(default_factory=lambda: REPO_ROOT / "prompts/themes.md")
    max_reviews_per_run: int = 450
    batch_size: int = 40
    text_max_chars: int = 200
    inter_request_delay_sec: float = 25.0
    daily_token_budget: int = 90_000
    tpm_soft_limit: int = 10_000
    max_tokens_per_response: int = 4096
    temperature: float = 0.1
    low_rating_weight: float = 1.5
    themes: list[ThemeDef] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path | None = None) -> Phase2Config:
        config_path = path or DEFAULT_CONFIG_PATH
        if not config_path.is_file():
            return cls(_default_themes())
        with config_path.open(encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}
        paths = raw.get("paths") or {}
        sampling = raw.get("sampling") or {}
        groq = raw.get("groq") or {}
        ranking = raw.get("ranking") or {}
        theme_rows = raw.get("themes") or _default_themes_raw()
        themes = [ThemeDef(id=str(t["id"]), label=str(t["label"])) for t in theme_rows]
        return cls(
            model=str(raw.get("model", "llama-3.3-70b-versatile")),
            normalized_path=REPO_ROOT / paths.get("normalized", "data/reviews/normalized.jsonl"),
            sample_path=REPO_ROOT / paths.get("sample", "data/reviews/phase2_sample.jsonl"),
            clusters_path=REPO_ROOT / paths.get("clusters", "data/themes/clusters.json"),
            ranked_path=REPO_ROOT / paths.get("ranked", "data/themes/ranked.json"),
            prompts_path=REPO_ROOT / paths.get("prompts", "prompts/themes.md"),
            max_reviews_per_run=int(sampling.get("max_reviews_per_run", 450)),
            batch_size=int(groq.get("batch_size", 40)),
            text_max_chars=int(groq.get("text_max_chars", 200)),
            inter_request_delay_sec=float(groq.get("inter_request_delay_sec", 25)),
            daily_token_budget=int(groq.get("daily_token_budget", 90_000)),
            tpm_soft_limit=int(groq.get("tpm_soft_limit", 10_000)),
            max_tokens_per_response=int(groq.get("max_tokens_per_response", 4096)),
            temperature=float(groq.get("temperature", 0.1)),
            low_rating_weight=float(ranking.get("low_rating_weight", 1.5)),
            themes=themes,
        )

    @property
    def theme_ids(self) -> list[str]:
        return [t.id for t in self.themes]

    @property
    def theme_labels(self) -> dict[str, str]:
        return {t.id: t.label for t in self.themes}


def _default_themes_raw() -> list[dict[str, str]]:
    return [
        {"id": "onboarding", "label": "Onboarding"},
        {"id": "kyc", "label": "KYC"},
        {"id": "payments", "label": "Payments"},
        {"id": "statements", "label": "Statements"},
        {"id": "withdrawals", "label": "Withdrawals"},
    ]


def _default_themes() -> list[ThemeDef]:
    return [ThemeDef(**t) for t in _default_themes_raw()]


THEME_IDS = frozenset(t["id"] for t in _default_themes_raw())
