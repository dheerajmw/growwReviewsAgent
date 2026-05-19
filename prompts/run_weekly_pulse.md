# Agent prompt — Run weekly pulse for Groww

Run the full weekly review pulse for **Groww** using repo scripts only (no `googleapis` in this repo).

## Command (local)

```bash
source .venv/bin/activate
set -a && source .env && set +a

# Data refresh + note (no publish)
python scripts/run_weekly_pulse.py -v

# Include Google Doc + Gmail draft via HTTP MCP
python scripts/run_weekly_pulse.py -v --publish --force
```

## Order

1. Download public reviews → `data/raw/`
2. Ingest → `data/reviews/normalized.jsonl`
3. Validate reviews
4. Groq themes → `data/themes/clusters.json`, `ranked.json`
5. Groq note → `data/weekly/note.md`, `note.json`
6. Validate note
7. PII gate (`check_pii.py`)
8. Publish Doc (MCP HTTP) — if `--publish-doc`
9. Publish Gmail draft (MCP HTTP) — if `--publish-draft`

## Rules

- Never add Google Docs/Gmail SDK code to this repository.
- Do not publish if Phase 4 PII check fails.
- Gmail: **draft only**, never send automatically.

See [doc/runbook.md](../doc/runbook.md).
