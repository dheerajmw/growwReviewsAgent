from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
DATA_ROOT = Path(os.environ.get("PULSE_DATA_ROOT", REPO_ROOT))


def _data_path(*parts: str) -> Path:
    return DATA_ROOT.joinpath(*parts)


PATHS = {
    "note_json": _data_path("data/weekly/note.json"),
    "note_md": _data_path("data/weekly/note.md"),
    "ranked": _data_path("data/themes/ranked.json"),
    "clusters": _data_path("data/themes/clusters.json"),
    "publish_state": _data_path("data/weekly/publish_state.json"),
    "blockers": _data_path("data/weekly/blockers.json"),
    "normalized": _data_path("data/reviews/normalized.jsonl"),
    "history": _data_path("data/weekly/history"),
}


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def count_words(text: str) -> int:
    return len(re.findall(r"\b[\w']+\b", text))


def get_pulse_latest() -> dict[str, Any]:
    note = _load_json(PATHS["note_json"])
    md = ""
    if PATHS["note_md"].is_file():
        md = PATHS["note_md"].read_text(encoding="utf-8")
    if not note:
        return {"error": "note not found", "markdown": md, "note": None}
    return {
        "note": note,
        "markdown": md,
        "word_count": count_words(md),
        "max_words": 250,
    }


def get_pulse_weeks() -> list[str]:
    weeks: list[str] = []
    state = _load_json(PATHS["publish_state"])
    if state and state.get("week_ending"):
        weeks.append(str(state["week_ending"]))
    if PATHS["history"].is_dir():
        for d in sorted(PATHS["history"].iterdir(), reverse=True):
            if d.is_dir():
                weeks.append(d.name)
    note = _load_json(PATHS["note_json"])
    if note:
        title = note.get("title", "")
        m = re.search(r"\((\d{4}-\d{2}-\d{2})\)", title)
        if m and m.group(1) not in weeks:
            weeks.insert(0, m.group(1))
    return list(dict.fromkeys(weeks))


def get_ranked() -> dict[str, Any]:
    data = _load_json(PATHS["ranked"])
    return data or {"ranked": [], "metadata": {}}


def get_clusters_summary() -> dict[str, Any]:
    data = _load_json(PATHS["clusters"])
    if not data:
        return {"themes": [], "metadata": {}}
    themes_out = []
    for t in data.get("themes") or []:
        themes_out.append(
            {
                "id": t.get("id"),
                "label": t.get("label"),
                "review_count": t.get("review_count"),
            }
        )
    return {"themes": themes_out, "metadata": data.get("metadata", {})}


def get_publish_state() -> dict[str, Any]:
    return _load_json(PATHS["publish_state"]) or {}


def get_pipeline_status() -> dict[str, Any]:
    blockers = _load_json(PATHS["blockers"])
    pii_passed = not (blockers and blockers.get("publish_blocked"))
    if PATHS["blockers"].is_file() and blockers is None:
        blockers = _load_json(PATHS["blockers"])

    def exists(key: str) -> bool:
        return PATHS[key].is_file()

    normalized_count = 0
    if exists("normalized"):
        with PATHS["normalized"].open(encoding="utf-8") as f:
            normalized_count = sum(1 for line in f if line.strip())

    state = get_publish_state()
    phases = [
        {"id": 1, "name": "Ingest reviews", "complete": exists("normalized")},
        {"id": 2, "name": "Theme clustering", "complete": exists("ranked") and exists("clusters")},
        {"id": 3, "name": "Weekly note", "complete": exists("note_json")},
        {"id": 4, "name": "PII gate", "complete": pii_passed and exists("note_md")},
        {"id": 5, "name": "Google Doc", "complete": bool(state.get("doc_id"))},
        {"id": 6, "name": "Gmail draft", "complete": bool(state.get("draft_id"))},
        {"id": 7, "name": "E2E scheduler", "complete": True},
    ]
    return {
        "pii_passed": pii_passed,
        "blockers": blockers,
        "phases": phases,
        "normalized_count": normalized_count,
        "sample_count": (_load_json(PATHS["ranked"]) or {}).get("metadata", {}).get("sample_count"),
        "publish_state": state,
        "scheduler": {"cron": "0 6 * * 1", "description": "Monday 06:00 UTC"},
    }
