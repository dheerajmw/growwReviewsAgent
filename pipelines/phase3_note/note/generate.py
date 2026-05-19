from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pipelines.phase2_themes.themes.groq_client import chat_completion, load_dotenv

from .config import Phase3Config
from .loaders import load_clusters, load_jsonl, load_ranked
from .render import count_words, render_note_md
from .validate import validate_note_structure

REPO_ROOT = Path(__file__).resolve().parents[3]


def _parse_note_json(raw: str) -> dict[str, Any]:
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object for weekly note")
    return data


def _week_ending_date(ranked_meta: dict[str, Any]) -> str:
    gen = ranked_meta.get("generated_at") or ""
    if gen:
        try:
            dt = datetime.fromisoformat(gen.replace("Z", "+00:00"))
            return dt.date().isoformat()
        except ValueError:
            pass
    return datetime.now(timezone.utc).date().isoformat()


def _theme_review_map(clusters: dict[str, Any]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for theme in clusters.get("themes") or []:
        tid = theme.get("id")
        if tid:
            out[str(tid)] = list(theme.get("review_ids") or [])
    return out


def _pick_candidates(
    theme_id: str,
    review_ids: list[str],
    by_id: dict[str, dict[str, Any]],
    *,
    limit: int,
    prefer_low: bool,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rid in review_ids:
        row = by_id.get(rid)
        if row and (row.get("text") or "").strip():
            rows.append(row)
    if prefer_low:
        rows.sort(key=lambda r: (int(r.get("rating") or 5), len(r.get("text") or "")))
    else:
        rows.sort(key=lambda r: int(r.get("rating") or 5), reverse=True)

    seen_text: set[str] = set()
    picked: list[dict[str, Any]] = []
    for row in rows:
        key = (row.get("text") or "")[:80].lower()
        if key in seen_text:
            continue
        seen_text.add(key)
        picked.append(
            {
                "review_id": row["review_id"],
                "rating": row.get("rating"),
                "text": (row.get("text") or "")[:400],
            }
        )
        if len(picked) >= limit:
            break
    return picked


def _build_user_payload(
    *,
    week_ending: str,
    top3: list[dict[str, Any]],
    candidates: dict[str, list[dict[str, Any]]],
) -> str:
    payload = {
        "week_ending": week_ending,
        "top3_themes": top3,
        "review_excerpts_by_theme": candidates,
    }
    return json.dumps(payload, indent=2)


def _dry_run_note(
    week_ending: str,
    top3: list[dict[str, Any]],
    candidates: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    themes_out: list[dict[str, Any]] = []
    quotes_out: list[dict[str, Any]] = []
    actions_out: list[dict[str, Any]] = []

    action_templates = {
        "payments": "Audit UPI and bank-link failure logs; fix top error codes and surface clearer retry copy.",
        "onboarding": "Shorten first-session KYC and funding checklist; add progress indicator for stalled signups.",
        "statements": "Improve statement PDF export reliability and in-app download status messaging.",
        "withdrawals": "Publish clearer withdrawal ETA and status timeline in the cash-out flow.",
        "kyc": "Reduce document re-upload loops with inline validation before submit.",
    }

    for row in top3[:3]:
        tid = row["id"]
        label = row.get("label", tid.title())
        pct = row.get("pct_of_sample", 0)
        themes_out.append(
            {
                "id": tid,
                "headline": f"{label} — {pct:.0f}% of sampled reviews; recurring friction in app feedback.",
            }
        )
        cands = candidates.get(tid) or []
        excerpt = cands[0]["text"] if cands else f"Users mention issues with {label.lower()}."
        short = excerpt.split(".")[0][:120] + ("." if "." in excerpt else "")
        quotes_out.append(
            {
                "theme_id": tid,
                "paraphrased": f"Users report that {short.lower().strip()}",
                "source_rating": cands[0].get("rating", 3) if cands else 3,
            }
        )
        actions_out.append(
            {
                "theme_id": tid,
                "text": action_templates.get(tid, f"Prioritize fixes for {label.lower()} pain points from this week's reviews."),
            }
        )

    return {
        "title": f"Groww — Weekly Review Pulse ({week_ending})",
        "themes": themes_out,
        "quotes": quotes_out,
        "actions": actions_out,
    }


def generate_weekly_note(
    config: Phase3Config | None = None,
    *,
    dry_run: bool = False,
) -> dict[str, Any]:
    cfg = config or Phase3Config.load()
    ranked_data = load_ranked(cfg.ranked_path)
    clusters_data = load_clusters(cfg.clusters_path)
    sample = load_jsonl(cfg.sample_path)
    by_id = {r["review_id"]: r for r in sample}

    ranked_list = ranked_data.get("ranked") or []
    top3_rows = ranked_list[:3]
    if len(top3_rows) < 3:
        raise RuntimeError("ranked.json must contain at least 3 themes")

    top3_ids = [r["id"] for r in top3_rows]
    week_ending = _week_ending_date(ranked_data.get("metadata") or {})
    theme_ids = _theme_review_map(clusters_data)

    candidates: dict[str, list[dict[str, Any]]] = {}
    for tid in top3_ids:
        rids = theme_ids.get(tid, [])
        candidates[tid] = _pick_candidates(
            tid,
            rids,
            by_id,
            limit=cfg.candidates_per_theme,
            prefer_low=cfg.prefer_low_ratings,
        )

    if dry_run:
        note = _dry_run_note(week_ending, top3_rows, candidates)
        note["metadata"] = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "dry_run": True,
            "groq_tokens_used": 0,
            "top3": top3_ids,
        }
        return note

    load_dotenv(REPO_ROOT)
    system = cfg.system_prompt_path.read_text(encoding="utf-8")
    weekly_tpl = cfg.weekly_prompt_path.read_text(encoding="utf-8")
    user = weekly_tpl + "\n\n## Input\n\n" + _build_user_payload(
        week_ending=week_ending,
        top3=top3_rows,
        candidates=candidates,
    )

    raw, tokens = chat_completion(
        system=system,
        user=user,
        model=cfg.model,
        temperature=cfg.temperature,
        max_tokens=cfg.max_tokens,
    )
    note = _parse_note_json(raw)
    struct_errors = validate_note_structure(note, top3_ids)
    if struct_errors:
        raise RuntimeError("LLM note failed structure validation: " + "; ".join(struct_errors))

    note["metadata"] = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "dry_run": False,
        "groq_tokens_used": tokens,
        "top3": top3_ids,
        "model": cfg.model,
    }
    return note


def _shorten_note_via_groq(note: dict[str, Any], cfg: Phase3Config, max_words: int) -> dict[str, Any]:
    load_dotenv(REPO_ROOT)
    system = "You shorten weekly executive notes. Output JSON only with same keys: title, themes, quotes, actions."
    user = (
        f"The rendered note exceeds {max_words} words. Shorten all text fields while keeping exactly "
        f"3 themes, 3 quotes, 3 actions. Return JSON only:\n\n{json.dumps(note, indent=2)}"
    )
    raw, extra = chat_completion(
        system=system,
        user=user,
        model=cfg.model,
        temperature=0.2,
        max_tokens=cfg.max_tokens,
    )
    shortened = _parse_note_json(raw)
    meta = note.get("metadata") or {}
    meta["groq_tokens_used"] = int(meta.get("groq_tokens_used", 0)) + extra
    shortened["metadata"] = meta
    return shortened


def run_generate(
    config: Phase3Config | None = None,
    *,
    dry_run: bool = False,
) -> Path:
    cfg = config or Phase3Config.load()
    note = generate_weekly_note(cfg, dry_run=dry_run)

    md = render_note_md(note)
    wc = count_words(md)
    if wc > cfg.max_words and not dry_run:
        note = _shorten_note_via_groq(note, cfg, cfg.max_words)
        md = render_note_md(note)

    cfg.note_json_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.note_md_path.parent.mkdir(parents=True, exist_ok=True)
    cfg.note_json_path.write_text(json.dumps(note, indent=2) + "\n", encoding="utf-8")
    cfg.note_md_path.write_text(md, encoding="utf-8")
    return cfg.note_md_path
