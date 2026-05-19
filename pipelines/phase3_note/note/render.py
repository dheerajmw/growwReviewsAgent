from __future__ import annotations

import re
from typing import Any


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w']+\b", text))


def render_note_md(note: dict[str, Any]) -> str:
    title = note.get("title") or "Groww — Weekly Review Pulse"
    lines = [f"# {title}", ""]

    lines.append("## Top themes")
    for i, theme in enumerate(note.get("themes") or [], start=1):
        headline = theme.get("headline") or theme.get("line") or theme.get("label", "")
        lines.append(f"{i}. {headline}")
    lines.append("")

    lines.append("## What users are saying")
    for q in note.get("quotes") or []:
        text = q.get("paraphrased") or q.get("text") or ""
        lines.append(f"- {text}")
    lines.append("")

    lines.append("## Suggested actions")
    for i, action in enumerate(note.get("actions") or [], start=1):
        text = action.get("text") or action.get("action") or ""
        lines.append(f"{i}. {text}")

    return "\n".join(lines).strip() + "\n"


def note_body_for_word_count(md: str) -> str:
    """Count words in full note (title + sections)."""
    return md
