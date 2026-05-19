# Phase 2 — Theme Clustering (≤5 Themes)

**Status:** Implemented.

**LLM:** Groq `llama-3.3-70b-versatile` — `GROQ_API_KEY` in `.env`

**Rate limits:** Sample **450** reviews; batches of **40**; **25s** between Groq calls; **90k** token daily cap.

## Outputs

| File | Description |
|------|-------------|
| `data/reviews/phase2_sample.jsonl` | Stratified subset for Groq |
| `data/themes/clusters.json` | Themes + `review_ids` |
| `data/themes/ranked.json` | Ordered themes for Phase 3 top-3 |

## Run (full pipeline)

```bash
cd /Users/dheerajj/Desktop/Milestone3
.venv/bin/pip install -r requirements.txt

# .env must contain GROQ_API_KEY=gsk_...
.venv/bin/python scripts/sample_for_phase2.py
.venv/bin/python scripts/cluster_themes.py -v

# Or one command:
.venv/bin/python pipelines/phase2_themes/run.py -v

.venv/bin/python scripts/validate_themes.py
```

**Dry run** (no Groq, heuristic themes only):

```bash
.venv/bin/python pipelines/phase2_themes/run.py --dry-run -v
```

## Options

| Flag | Description |
|------|-------------|
| `--resample` | Regenerate `phase2_sample.jsonl` |
| `--sample-only` | Only sample, no Groq |
| `--cluster-only` | Skip sample step (use existing sample) |
| `--dry-run` | Skip Groq API calls |

Config: [`configs/phase2_themes.yaml`](../../configs/phase2_themes.yaml)

**Evaluation:** [doc/eval/phase-02/eval.md](../../doc/eval/phase-02/eval.md)

**Depends on:** [Phase 1](../phase1_ingest/README.md) → `normalized.jsonl`

**Next:** [Phase 3 — Weekly note](../phase3_note/README.md)
