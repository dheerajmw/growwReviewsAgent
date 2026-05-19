from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import THEME_IDS, Phase2Config
from .sample import load_jsonl


def validate_clusters(
    clusters_path: Path,
    sample_path: Path,
    *,
    allowed_theme_ids: frozenset[str] = THEME_IDS,
) -> list[str]:
    errors: list[str] = []
    if not clusters_path.is_file():
        return [f"missing {clusters_path}"]
    if not sample_path.is_file():
        return [f"missing {sample_path}"]

    clusters: dict[str, Any] = json.loads(clusters_path.read_text(encoding="utf-8"))
    themes = clusters.get("themes")
    if not isinstance(themes, list):
        return ["clusters.themes must be a list"]

    if len(themes) > 5:
        errors.append(f"more than 5 themes: {len(themes)}")

    sample_ids = {r["review_id"] for r in load_jsonl(sample_path)}
    seen: set[str] = set()
    covered: set[str] = set()

    for i, theme in enumerate(themes):
        prefix = f"themes[{i}]"
        for field in ("id", "label", "review_ids"):
            if field not in theme:
                errors.append(f"{prefix} missing {field}")
        tid = theme.get("id", "")
        if tid not in allowed_theme_ids:
            errors.append(f"{prefix} invalid theme id: {tid!r}")
        for rid in theme.get("review_ids") or []:
            if rid in seen:
                errors.append(f"duplicate review_id across themes: {rid}")
            seen.add(rid)
            covered.add(rid)

    orphans = sample_ids - covered
    if orphans:
        errors.append(f"unassigned review_ids: {len(orphans)} (e.g. {list(orphans)[:3]})")

    extra = covered - sample_ids
    if extra:
        errors.append(f"review_ids not in sample: {len(extra)}")

    return errors


def validate_ranked(ranked_path: Path, min_entries: int = 3) -> list[str]:
    errors: list[str] = []
    if not ranked_path.is_file():
        return [f"missing {ranked_path}"]
    data: dict[str, Any] = json.loads(ranked_path.read_text(encoding="utf-8"))
    ranked = data.get("ranked")
    if not isinstance(ranked, list):
        return ["ranked.ranked must be a list"]
    if len(ranked) < min_entries:
        errors.append(f"expected at least {min_entries} ranked themes, got {len(ranked)}")
    for i, row in enumerate(ranked):
        for field in ("id", "label", "review_count", "score"):
            if field not in row:
                errors.append(f"ranked[{i}] missing {field}")
    return errors


def validate_all(config: Phase2Config | None = None) -> tuple[list[str], dict[str, Any]]:
    cfg = config or Phase2Config.load()
    errors: list[str] = []
    errors.extend(validate_clusters(cfg.clusters_path, cfg.sample_path))
    errors.extend(validate_ranked(cfg.ranked_path))
    summary: dict[str, Any] = {}
    if cfg.clusters_path.is_file():
        c = json.loads(cfg.clusters_path.read_text(encoding="utf-8"))
        summary["theme_count"] = len(c.get("themes", []))
        summary["groq_tokens_used"] = (c.get("metadata") or {}).get("groq_tokens_used")
    if cfg.ranked_path.is_file():
        r = json.loads(cfg.ranked_path.read_text(encoding="utf-8"))
        summary["top3"] = (r.get("metadata") or {}).get("top3")
    return errors, summary
