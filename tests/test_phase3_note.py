from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def phase3_config(tmp_path: Path):
    from pipelines.phase3_note.note.config import Phase3Config

    ranked = REPO / "data/themes/ranked.json"
    clusters = REPO / "data/themes/clusters.json"
    sample = REPO / "data/reviews/phase2_sample.jsonl"
    if not all(p.is_file() for p in (ranked, clusters, sample)):
        pytest.skip("Phase 2 artifacts required")

    return Phase3Config(
        ranked_path=ranked,
        clusters_path=clusters,
        sample_path=sample,
        note_md_path=tmp_path / "note.md",
        note_json_path=tmp_path / "note.json",
        system_prompt_path=REPO / "prompts/system.md",
        weekly_prompt_path=REPO / "prompts/weekly_note.md",
        max_words=250,
    )


def test_dry_run_generate_and_validate(phase3_config):
    from pipelines.phase3_note.note.generate import run_generate
    from pipelines.phase3_note.note.validate import validate_note

    run_generate(phase3_config, dry_run=True)
    errors, summary = validate_note(phase3_config)
    assert not errors, errors
    assert summary["word_count"] <= 250

    note = json.loads(phase3_config.note_json_path.read_text())
    assert len(note["themes"]) == 3
    assert len(note["quotes"]) == 3
    assert len(note["actions"]) == 3


def test_render_word_count():
    from pipelines.phase3_note.note.render import count_words, render_note_md

    note = {
        "title": "Groww — Weekly Review Pulse (2026-05-19)",
        "themes": [{"id": "a", "headline": "Short theme line."}] * 3,
        "quotes": [{"paraphrased": "User concern one."}] * 3,
        "actions": [{"text": "Fix the flow."}] * 3,
    }
    md = render_note_md(note)
    assert count_words(md) < 100
    assert "## Top themes" in md
