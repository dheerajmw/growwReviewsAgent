from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .config import Phase3Config
from .render import count_words, note_body_for_word_count, render_note_md

ADVISORY_PATTERNS = re.compile(
    r"\b(should invest|buy this|sell now|recommend (?:buying|selling)|you should buy)\b",
    re.IGNORECASE,
)


def validate_note_structure(note: dict[str, Any], top3_ids: list[str] | None = None) -> list[str]:
    errors: list[str] = []
    for key in ("title", "themes", "quotes", "actions"):
        if key not in note:
            errors.append(f"missing key: {key}")

    themes = note.get("themes")
    quotes = note.get("quotes")
    actions = note.get("actions")

    if not isinstance(themes, list) or len(themes) != 3:
        errors.append(f"themes must have length 3, got {len(themes) if isinstance(themes, list) else type(themes)}")
    if not isinstance(quotes, list) or len(quotes) != 3:
        errors.append(f"quotes must have length 3, got {len(quotes) if isinstance(quotes, list) else type(quotes)}")
    if not isinstance(actions, list) or len(actions) != 3:
        errors.append(f"actions must have length 3, got {len(actions) if isinstance(actions, list) else type(actions)}")

    if top3_ids and isinstance(themes, list):
        note_ids = [t.get("id") for t in themes if isinstance(t, dict)]
        if note_ids != top3_ids[:3]:
            errors.append(f"theme ids {note_ids!r} must match top3 {top3_ids[:3]!r}")

    return errors


def validate_note_files(
    config: Phase3Config | None = None,
    *,
    max_words: int | None = None,
) -> tuple[list[str], dict[str, Any]]:
    cfg = config or Phase3Config.load()
    limit = max_words if max_words is not None else cfg.max_words
    errors: list[str] = []
    summary: dict[str, Any] = {}

    if not cfg.note_json_path.is_file():
        errors.append(f"missing {cfg.note_json_path}")
    if not cfg.note_md_path.is_file():
        errors.append(f"missing {cfg.note_md_path}")
    if errors:
        return errors, summary

    note: dict[str, Any] = json.loads(cfg.note_json_path.read_text(encoding="utf-8"))
    md = cfg.note_md_path.read_text(encoding="utf-8")
    top3: list[str] | None = None
    if cfg.ranked_path.is_file():
        ranked_data = json.loads(cfg.ranked_path.read_text(encoding="utf-8"))
        top3 = (ranked_data.get("metadata") or {}).get("top3")
        if not top3 and ranked_data.get("ranked"):
            top3 = [r["id"] for r in ranked_data["ranked"][:3]]

    errors.extend(validate_note_structure(note, top3))
    wc = count_words(note_body_for_word_count(md))
    summary["word_count"] = wc
    if wc > limit:
        errors.append(f"word count {wc} exceeds max {limit}")

    if ADVISORY_PATTERNS.search(md):
        errors.append("advisory language detected in note.md")

    summary["title"] = note.get("title")
    return errors, summary


def validate_note(
    config: Phase3Config | None = None,
    *,
    max_words: int | None = None,
) -> tuple[list[str], dict[str, Any]]:
    return validate_note_files(config, max_words=max_words)
