#!/usr/bin/env python3
"""Phase 2 unit tests (sampling, rank, validate — no Groq required)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pipelines.phase2_themes.themes.cluster import cluster_reviews
from pipelines.phase2_themes.themes.config import Phase2Config
from pipelines.phase2_themes.themes.rank import build_ranked, write_ranked
from pipelines.phase2_themes.themes.sample import sample_reviews, write_jsonl
from pipelines.phase2_themes.themes.validate import validate_all, validate_clusters


class Phase2Tests(unittest.TestCase):
    def test_sample_stratified_cap(self) -> None:
        reviews = []
        for i in range(100):
            reviews.append(
                {
                    "review_id": f"app:{i}",
                    "store": "app_store",
                    "date": f"2026-05-{i % 28 + 1:02d}T00:00:00Z",
                    "rating": 4,
                    "text": "word " * 10,
                    "title": "",
                }
            )
        for i in range(200):
            reviews.append(
                {
                    "review_id": f"play:{i}",
                    "store": "play_store",
                    "date": f"2026-04-{i % 28 + 1:02d}T00:00:00Z",
                    "rating": 3,
                    "text": "word " * 10,
                    "title": "",
                }
            )
        sampled = sample_reviews(reviews, 90)
        self.assertEqual(len(sampled), 90)
        stores = {r["store"] for r in sampled}
        self.assertEqual(stores, {"app_store", "play_store"})

    def test_dry_run_cluster_and_validate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sample = tmp_path / "sample.jsonl"
            clusters_path = tmp_path / "clusters.json"
            ranked_path = tmp_path / "ranked.json"

            rows = []
            for i, theme_word in enumerate(
                ["kyc", "payment", "withdraw", "statement", "onboard", "kyc"], start=1
            ):
                rows.append(
                    {
                        "review_id": f"r{i}",
                        "rating": 2 if i % 2 == 0 else 5,
                        "title": "",
                        "text": f"Issues with {theme_word} flow on the app today",
                        "date": "2026-05-10T00:00:00Z",
                        "store": "play_store",
                    }
                )
            write_jsonl(sample, rows)

            config = Phase2Config.load()
            config.sample_path = sample
            config.clusters_path = clusters_path
            config.ranked_path = ranked_path

            clusters, _ = cluster_reviews(rows, config, dry_run=True)
            with clusters_path.open("w", encoding="utf-8") as f:
                json.dump(clusters, f)

            write_ranked(clusters, config)
            errors, _ = validate_all(config)
            self.assertEqual(errors, [], errors)


if __name__ == "__main__":
    unittest.main()
