from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

from .config import Phase2Config
from .sample import load_jsonl

logger = logging.getLogger(__name__)


def build_ranked(
    clusters: dict[str, Any],
    reviews: list[dict[str, Any]],
    config: Phase2Config,
) -> list[dict[str, Any]]:
    rating_by_id = {r["review_id"]: int(r.get("rating", 3)) for r in reviews}
    ranked: list[dict[str, Any]] = []

    for theme in clusters.get("themes", []):
        tid = theme["id"]
        ids = theme.get("review_ids") or []
        score = 0.0
        low_count = 0
        for rid in ids:
            rating = rating_by_id.get(rid, 3)
            weight = config.low_rating_weight if rating <= 2 else 1.0
            score += weight
            if rating <= 2:
                low_count += 1
        ranked.append(
            {
                "id": tid,
                "label": theme.get("label", tid),
                "review_count": len(ids),
                "low_rating_count": low_count,
                "score": round(score, 2),
            }
        )

    ranked.sort(key=lambda x: (-x["score"], -x["review_count"]))
    total = sum(t["review_count"] for t in ranked) or 1
    for t in ranked:
        t["pct_of_sample"] = round(100.0 * t["review_count"] / total, 1)

    return ranked


def write_ranked(
    clusters: dict[str, Any],
    config: Phase2Config,
) -> list[dict[str, Any]]:
    reviews = load_jsonl(config.sample_path)
    ranked = build_ranked(clusters, reviews, config)
    payload = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sample_count": len(reviews),
            "top3": [r["id"] for r in ranked[:3]],
        },
        "ranked": ranked,
    }
    config.ranked_path.parent.mkdir(parents=True, exist_ok=True)
    with config.ranked_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    logger.info("Wrote %s (top theme: %s)", config.ranked_path, ranked[0]["id"] if ranked else "n/a")
    return ranked
