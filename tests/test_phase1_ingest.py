#!/usr/bin/env python3
"""Phase 1 unit tests (stdlib only)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pipelines.phase1_ingest.ingest.config import IngestConfig
from pipelines.phase1_ingest.ingest.pipeline import run_ingest
from pipelines.phase1_ingest.ingest.validate import validate_normalized_file


class Phase1IngestTests(unittest.TestCase):
    def test_ingest_and_validate_fixture_corpus(self) -> None:
        raw = REPO / "data" / "raw"
        if not (raw / "app_store.csv").is_file():
            self.skipTest("Run generate_sample_exports.py first")

        config = IngestConfig.load()
        stats = run_ingest(config=config, weeks=12)
        self.assertGreater(stats.rows_written, 0)
        self.assertEqual(stats.files_read, 2)

        errors, summary = validate_normalized_file(config.output, min_rows=1)
        self.assertEqual(errors, [], errors)
        self.assertIn("app_store", summary["stores"])
        self.assertIn("play_store", summary["stores"])

    def test_dedup_same_review_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw = tmp_path / "raw"
            raw.mkdir()
            out = tmp_path / "out.jsonl"

            csv_content = (
                "App Store Review ID,Rating,Title,Review,Date\n"
                "DUP-1,5,Title,Same review text repeated here for dedup testing today,2026-05-01\n"
                "DUP-1,5,Title,Same review text repeated here for dedup testing today,2026-05-01\n"
            )
            (raw / "app_store.csv").write_text(csv_content, encoding="utf-8")
            (raw / "play_store.csv").write_text(
                "Review ID,Star Rating,Review Title,Review Text,Review Submit Date and Time\n"
                "P-1,4,Title here,Play review text with enough english words for filters,2026-05-02 12:00:00\n",
                encoding="utf-8",
            )

            config = IngestConfig.load()
            config.raw_dir = raw
            config.output = out
            stats = run_ingest(config=config, weeks=12)
            self.assertEqual(stats.rows_deduped, 1)
            lines = out.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(lines), 2)


if __name__ == "__main__":
    unittest.main()
