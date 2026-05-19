from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import Phase2Config, THEME_IDS
from .groq_client import chat_completion, load_dotenv, parse_assignments_json
from .rate_limit import GroqRateLimiter
from .sample import load_jsonl

logger = logging.getLogger(__name__)


def _load_system_prompt(config: Phase2Config) -> str:
    if config.prompts_path.is_file():
        return config.prompts_path.read_text(encoding="utf-8")
    theme_list = ", ".join(config.theme_ids)
    return (
        f"Classify each review into exactly one theme: {theme_list}. "
        "Respond with JSON only: [{\"review_id\":\"...\",\"theme\":\"...\"}, ...]"
    )


def _compact_review(review: dict[str, Any], text_max_chars: int) -> dict[str, Any]:
    text = str(review.get("text") or "")[:text_max_chars]
    return {
        "review_id": review["review_id"],
        "rating": review["rating"],
        "text": text,
    }


def _build_user_payload(batch: list[dict[str, Any]], text_max_chars: int) -> str:
    compact = [_compact_review(r, text_max_chars) for r in batch]
    return json.dumps(compact, ensure_ascii=False)


def _assign_batch(
    config: Phase2Config,
    batch: list[dict[str, Any]],
    system: str,
    limiter: GroqRateLimiter,
) -> list[dict[str, str]]:
    limiter.wait_for_tpm()
    limiter.assert_daily_budget(estimated_next=6000)

    user = _build_user_payload(batch, config.text_max_chars)
    raw, tokens = chat_completion(
        system=system,
        user=user,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens_per_response,
    )
    limiter.record(tokens)
    logger.info("Groq batch (%s reviews): %s tokens", len(batch), tokens)

    assignments = parse_assignments_json(raw)
    expected = {r["review_id"] for r in batch}
    got = {a["review_id"] for a in assignments}
    missing = expected - got
    if missing:
        logger.warning("Batch missing %s review_ids; will retry or heuristic-fill", len(missing))
    return assignments


def _heuristic_theme(review: dict[str, Any]) -> str:
    text = f"{review.get('title', '')} {review.get('text', '')}".lower()
    rules = [
        ("kyc", ("kyc", "pan", "aadhaar", "verification", "verify")),
        ("payments", ("payment", "upi", "sip", "pay", "autopay", "failed")),
        ("withdrawals", ("withdraw", "payout", "bank transfer")),
        ("statements", ("statement", "report", "tax", "capital gain", "download")),
        ("onboarding", ("onboard", "signup", "sign up", "otp", "login", "register")),
    ]
    for theme_id, keywords in rules:
        if any(k in text for k in keywords):
            return theme_id
    return "onboarding"


def cluster_reviews(
    reviews: list[dict[str, Any]],
    config: Phase2Config,
    *,
    dry_run: bool = False,
) -> tuple[dict[str, Any], GroqRateLimiter]:
    load_dotenv()
    limiter = GroqRateLimiter(
        daily_token_budget=config.daily_token_budget,
        tpm_soft_limit=config.tpm_soft_limit,
        inter_request_delay_sec=config.inter_request_delay_sec,
    )
    system = _load_system_prompt(config)
    assignments_map: dict[str, str] = {}

    if dry_run:
        for r in reviews:
            assignments_map[r["review_id"]] = _heuristic_theme(r)
        return _build_clusters(reviews, assignments_map, config, limiter, dry_run=True), limiter

    batches = [
        reviews[i : i + config.batch_size]
        for i in range(0, len(reviews), config.batch_size)
    ]
    logger.info("Clustering %s reviews in %s Groq batches", len(reviews), len(batches))

    for idx, batch in enumerate(batches, start=1):
        logger.info("Batch %s/%s (%s reviews)", idx, len(batches), len(batch))
        try:
            assignments = _assign_batch(config, batch, system, limiter)
            for a in assignments:
                theme = a["theme"]
                if theme not in THEME_IDS:
                    theme = _heuristic_theme(next(r for r in batch if r["review_id"] == a["review_id"]))
                assignments_map[a["review_id"]] = theme
        except (json.JSONDecodeError, ValueError) as exc:
            logger.error("Parse error batch %s: %s — using heuristics", idx, exc)
            for r in batch:
                assignments_map[r["review_id"]] = _heuristic_theme(r)

        for r in batch:
            if r["review_id"] not in assignments_map:
                assignments_map[r["review_id"]] = _heuristic_theme(r)

        if idx < len(batches):
            limiter.pause_between_requests()

    return _build_clusters(reviews, assignments_map, config, limiter), limiter


def _build_clusters(
    reviews: list[dict[str, Any]],
    assignments_map: dict[str, str],
    config: Phase2Config,
    limiter: GroqRateLimiter,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    buckets: dict[str, list[str]] = {t.id: [] for t in config.themes}
    for r in reviews:
        rid = r["review_id"]
        theme = assignments_map.get(rid, _heuristic_theme(r))
        if theme not in buckets:
            theme = "onboarding"
        buckets[theme].append(rid)

    themes_out = []
    for t in config.themes:
        ids = buckets.get(t.id, [])
        themes_out.append(
            {
                "id": t.id,
                "label": t.label,
                "review_count": len(ids),
                "review_ids": ids,
            }
        )

    return {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sample_count": len(reviews),
            "groq_model": config.model,
            "dry_run": dry_run,
            "groq_tokens_used": limiter.daily_tokens_used,
            "theme_ids": config.theme_ids,
        },
        "themes": themes_out,
    }


def run_clustering(
    config: Phase2Config | None = None,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    cfg = config or Phase2Config.load()
    if not cfg.sample_path.is_file():
        raise FileNotFoundError(
            f"Missing {cfg.sample_path}. Run sample_for_phase2.py first."
        )
    reviews = load_jsonl(cfg.sample_path)
    clusters, limiter = cluster_reviews(reviews, cfg, dry_run=dry_run)

    cfg.clusters_path.parent.mkdir(parents=True, exist_ok=True)
    with cfg.clusters_path.open("w", encoding="utf-8") as f:
        json.dump(clusters, f, indent=2, ensure_ascii=False)

    logger.info(
        "Wrote %s (%s themes, %s Groq tokens)",
        cfg.clusters_path,
        len(clusters["themes"]),
        limiter.daily_tokens_used,
    )
    return clusters
