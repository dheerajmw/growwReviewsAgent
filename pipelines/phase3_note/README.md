# Phase 3 — Weekly note generation

**Plan:** [Phase 3](../../doc/phasewiseImplementationPlan.md#phase-3--weekly-note-generation-250-words) · **Eval:** [phase-03 eval](../../doc/eval/phase-03/eval.md)

Produces `data/weekly/note.md` and `note.json` from Phase 2 `ranked.json` + review excerpts.

## Inputs

| Path | Source |
|------|--------|
| `data/themes/ranked.json` | Phase 2 |
| `data/themes/clusters.json` | Phase 2 |
| `data/reviews/phase2_sample.jsonl` | Phase 2 |
| `prompts/system.md`, `prompts/weekly_note.md` | Prompts |

## Outputs

| Path | Description |
|------|-------------|
| `data/weekly/note.json` | Structured note for MCP publish |
| `data/weekly/note.md` | Human-readable pulse (≤250 words) |

## Run

```bash
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)   # GROQ_API_KEY

python pipelines/phase3_note/run.py -v
python scripts/validate_note.py
```

`--dry-run` builds a heuristic note without calling Groq (for CI / offline).

**Depends on:** [Phase 2](../phase2_themes/README.md)
