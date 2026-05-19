# Phase 1 Evaluation — Review Ingest & Validation

**Plan:** [Phase 1](../../phasewiseImplementationPlan.md#phase-1--review-ingest-and-validation) · **Depends on:** [Phase 0](../phase-00/eval.md) complete

---

## Prerequisites

- [Phase 0 exit criteria](../phase-00/eval.md#exit-criteria-sign-off-checklist) met
- App Store and Play Store review export files in `data/raw/`
- `scripts/ingest_reviews.py` implemented

---

## Automated checks

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | Ingest runs cleanly | `python3 scripts/ingest_reviews.py` | Exit code `0`; writes `data/reviews/normalized.jsonl` |
| A2 | Output non-empty | `wc -l < data/reviews/normalized.jsonl` | Line count > 0 |
| A3 | Schema validation | `python3 scripts/validate_reviews.py` (or ingest `--validate`) | Exit code `0`; no schema errors |
| A4 | Both stores present | `python3 -c "import json; s=set(json.loads(l)['store'] for l in open('data/reviews/normalized.jsonl')); assert 'app_store' in s and 'play_store' in s"` | Both stores in output |
| A5 | Date window | Ingest config: `--weeks 12` (or 8–12) | All `date` values within window; log shows dropped-out-of-window count |
| A6 | Rating range | Validator | Every `rating` in 1–5 |
| A7 | Required fields | Validator | Every row has `rating`, `title`, `text`, `date`, `store`, `review_id` |
| A8 | Dedup | Run ingest twice | Second run: duplicate count in log; line count stable |
| A9 | Normalization | Ingest log includes `Filtered (normalization)` | Counts for `too_few_words`, `non_english`, `contains_emoji` |
| A10 | Min words | Spot-check JSONL | All rows have ≥6 English words in title+body |
| A11 | No emoji | `python3 -c "..."` or manual | No emoji in random sample of `text` fields |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | Inspect ingest log | Counts for: read, in-window, deduped, invalid, written |
| M2 | Spot-check 5 random lines in `normalized.jsonl` | Dates plausible; `text` non-empty; no obvious corrupt encoding |
| M3 | Compare raw vs normalized row count | Normalized ≤ raw; difference explained by window/dedup/invalid |
| M4 | Confirm `review_id` not in publish docs | Grep `doc/` and `prompts/` for guidance that `review_id` is internal-only |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** ≥1 App Store and ≥1 Play Store source file ingested
- [ ] **E2** `data/reviews/normalized.jsonl` exists with reviews from **8–12 week** window
- [ ] **E3** Invalid rows logged (not silently dropped)
- [ ] **E4** Canonical schema documented (see [architecture](../../architecture.md#31-ingest-pipeline-local))
- [ ] **E5** `review_id` used only for dedup — excluded from downstream publish artifacts

**Phase 1 complete when:** E1–E5 checked and A1–A8 pass.

---

## Sample acceptance thresholds

| Metric | Minimum (adjust per corpus) |
|--------|-----------------------------|
| Reviews in window | ≥50 combined (or all available if smaller export) |
| Invalid row rate | <10% unless explained in notes |

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Zero Play Store rows | Column mapping wrong | Update ingest column map for Play CSV |
| All dates filtered out | Wrong date format / timezone | Normalize to ISO 8601 UTC or local with documented rule |
| Duplicate explosion | Weak dedup key | Dedup on `review_id` or hash `(store, date, text)` |

---

## Evidence to retain

- Ingest log snippet (counts)
- `head -n 2 data/reviews/normalized.jsonl` (redact if needed for submission)

**Evaluator:** _______________ **Date:** _______________
