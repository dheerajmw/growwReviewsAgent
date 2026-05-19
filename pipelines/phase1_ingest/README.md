# Phase 1 — Review Ingest & Validation

**Objective:** Normalize 8–12 weeks of App Store and Play Store **public exports** into `data/reviews/normalized.jsonl`.

**Evaluation:** [doc/eval/phase-01/eval.md](../../doc/eval/phase-01/eval.md)

## Canonical schema

| Field | Description |
|-------|-------------|
| `rating` | Integer 1–5 |
| `title` | Review title (may be empty string on Play) |
| `text` | Review body (required, non-empty) |
| `date` | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) |
| `store` | `app_store` or `play_store` |
| `review_id` | **Internal only** — dedup; never publish (see [decision D-013](../../doc/decision.md)) |

## Content normalization (after date filter)

Configured in `configs/phase1_ingest.yaml` → `normalization`:

| Rule | Default | Skip reason logged |
|------|---------|-------------------|
| Min **6** English words (title + body) | on | `too_few_words` |
| English only (`langdetect`) | on | `non_english` |
| No emoji / emoticons | on | `contains_emoji` |

## Inputs

Place exports under `data/raw/`:

- `app_store*.csv` or `.json` — App Store Connect export **or** RSS download
- `play_store*.csv` or `.json` — Play Console export **or** public scraper download

### Download public reviews (Groww)

```bash
python3 scripts/download_reviews.py --weeks 12
```

- **Play:** `com.nextbillion.groww` (country `in`)
- **App Store:** app id `1404871703` via iTunes RSS

Then run ingest (below).

## Run

```bash
# From repo root (install deps once: pip install -r requirements.txt)
python3 scripts/ingest_reviews.py
python3 scripts/validate_reviews.py
```

Or:

```bash
python3 pipelines/phase1_ingest/run.py --weeks 12 -v
```

## Options

| Flag | Description |
|------|-------------|
| `--weeks` | Rolling window (8–12, default 12 from config) |
| `--config` | Custom YAML path |
| `--no-validate` | Skip post-ingest validation |
| `-v` | Verbose logging |

## Outputs

- `data/reviews/normalized.jsonl` — one JSON object per line
- Console log: files read, in-window, out-of-window, invalid, deduped, written

## Next phase

[Phase 2 — Theme clustering](../phase2_themes/README.md)
