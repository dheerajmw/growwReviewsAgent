from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "tests" / "fixtures"
PYTHON = sys.executable
CHECK = REPO / "scripts" / "check_pii.py"


def test_clean_note_snippet_passes():
    from pipelines.phase4_pii.pii.scan import scan_text

    text = (FIXTURES / "clean_note_snippet.txt").read_text(encoding="utf-8")
    assert scan_text(text) == []


def test_pii_samples_fail():
    from pipelines.phase4_pii.pii.scan import scan_text

    text = (FIXTURES / "pii_samples.txt").read_text(encoding="utf-8")
    findings = scan_text(text)
    types = {f.pii_type for f in findings}
    assert "email" in types
    assert "phone" in types
    assert "at_handle" in types
    assert "long_numeric_id" in types
    assert "store_review_id" in types


def test_cli_negative_email():
    proc = subprocess.run(
        [PYTHON, str(CHECK), "-", "--no-blockers"],
        input="Contact user@example.com\n",
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert proc.returncode != 0


def test_cli_at_handle():
    proc = subprocess.run(
        [PYTHON, str(CHECK), "-", "--no-blockers"],
        input="@groww_user_123\n",
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert proc.returncode != 0


def test_cli_phone():
    proc = subprocess.run(
        [PYTHON, str(CHECK), "-", "--no-blockers"],
        input="+91 98765 43210\n",
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert proc.returncode != 0


def test_blockers_written_on_failure(tmp_path: Path):
    from pipelines.phase4_pii.pii.config import Phase4Config
    from pipelines.phase4_pii.pii.gate import run_pii_gate

    dirty = tmp_path / "dirty.md"
    dirty.write_text("Email: bad@evil.com\n", encoding="utf-8")
    blockers = tmp_path / "blockers.json"
    cfg = Phase4Config(note_md_path=dirty, blockers_path=blockers)
    result = run_pii_gate(dirty, cfg)
    assert not result.passed
    assert blockers.is_file()
    data = json.loads(blockers.read_text())
    assert data["publish_blocked"] is True
    assert len(data["findings"]) >= 1


def test_weekly_note_passes_if_present():
    note = REPO / "data/weekly/note.md"
    if not note.is_file():
        return
    proc = subprocess.run(
        [PYTHON, str(CHECK), str(note), "--no-blockers"],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
