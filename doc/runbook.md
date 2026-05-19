# Weekly pulse runbook — Groww (Milestone 3)

**Plan:** [Phase 7](./phasewiseImplementationPlan.md#phase-7--end-to-end-workflow-github-actions-scheduler-and-hardening)

End-to-end flow: public App Store / Play reviews → themes → weekly note → PII gate → Google Doc + Gmail draft (via [HTTP MCP server](https://github.com/dheerajmw/MCP-server)).

---

## Prerequisites

| Item | Where |
|------|--------|
| Python 3.9+ venv | `python3 -m venv .venv && pip install -r requirements.txt` |
| `GROQ_API_KEY` | `.env` — Phases 2–3 |
| `GROWW_PULSE_DOC_ID` | `.env` — Phase 5 |
| `PULSE_DRAFT_TO` | `.env` — Phase 6 |
| `MCP_SERVER_URL` | `.env` — default `https://mcp-server-p01x.onrender.com` |
| Render MCP OAuth | `GOOGLE_CREDENTIALS_JSON`, `GOOGLE_TOKEN_JSON` on MCP server |

---

## One-command local run

```bash
source .venv/bin/activate
set -a && source .env && set +a

# Refresh data + generate note (no Google publish)
python scripts/run_weekly_pulse.py -v

# Full run including Doc append + Gmail draft
python scripts/run_weekly_pulse.py -v --publish --force
```

### Useful flags

| Flag | Effect |
|------|--------|
| `--skip-download` | Use existing `data/raw/` CSVs |
| `--publish-only` | PII check + publish only (note must exist) |
| `--publish-doc` / `--publish-draft` | Select publish steps |
| `--stop-after themes` | Stop after Phase 2 |
| `--phase2-dry-run` | No Groq for themes (CI smoke) |

---

## Manual step-by-step

| # | Command | Output |
|---|---------|--------|
| 1 | `python scripts/download_reviews.py` | `data/raw/*.csv` |
| 2 | `python scripts/ingest_reviews.py` | `data/reviews/normalized.jsonl` |
| 3 | `python scripts/validate_reviews.py` | exit 0 |
| 4 | `python pipelines/phase2_themes/run.py -v` | `data/themes/clusters.json`, `ranked.json` |
| 5 | `python pipelines/phase3_note/run.py -v` | `data/weekly/note.md`, `note.json` |
| 6 | `python scripts/validate_note.py` | exit 0 |
| 7 | `python scripts/check_pii.py data/weekly/note.md` | exit 0 |
| 8 | `python scripts/publish_doc.py -v` | Doc updated; `publish_state.json` |
| 9 | `python scripts/publish_draft.py -v` | Gmail draft; `draft_id` in state |

**Timebox:** Steps 2–9 in ≤30 minutes (excluding step 1 download).

---

## GitHub Actions scheduler

Workflow: [`.github/workflows/weekly_pulse.yml`](../.github/workflows/weekly_pulse.yml)

| Job | When | What |
|-----|------|------|
| **validate** | Push / PR to `main` | Ingest (if raw present) + validators; **no Groq** |
| **refresh-data** | Cron Mon 06:00 UTC + manual dispatch | Download → ingest → Groq themes → note → PII |
| **publish** | Manual dispatch only | Doc + draft via MCP (needs secrets) |

### Repository secrets

| Secret | Required for |
|--------|----------------|
| `GROQ_API_KEY` | `refresh-data` job |
| `GROWW_PULSE_DOC_ID` | `publish` job |
| `PULSE_DRAFT_TO` | `publish` job |
| `MCP_SERVER_URL` | Optional override for publish |

### Trigger refresh manually

GitHub → **Actions** → **Weekly pulse** → **Run workflow** → choose job inputs.

Artifacts: `weekly-pulse-YYYY-MM-DD` contains `data/themes/` and `data/weekly/`.

---

## Verification checklist

- [ ] `normalized.jsonl` row count > 0
- [ ] ≤5 themes in `clusters.json`
- [ ] `note.md` ≤250 words (`validate_note.py`)
- [ ] `check_pii.py` passes
- [ ] Google Doc shows new appended section
- [ ] Gmail draft exists (not sent)
- [ ] `publish_state.json` has `doc_id`, `doc_url`, `draft_id`, `published_at`

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Groq 429 | Reduce sample in `configs/phase2_themes.yaml`; re-run `--cluster-only` |
| Doc 404 | Check full Doc ID in `GROWW_PULSE_DOC_ID` (includes leading characters) |
| Empty draft | Confirm Gmail API on MCP server; re-OAuth Render token |
| PII fail | Fix `note.md`; optional `pipelines/phase4_pii/run.py --redact` |

**Eval:** [doc/eval/phase-07/eval.md](./eval/phase-07/eval.md)
