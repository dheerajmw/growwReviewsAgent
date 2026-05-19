# Milestone 3 — Weekly App Review Pulse (Groww)

Turn App Store and Play Store review exports into a weekly one-page pulse, published via **Google Workspace MCP** (Docs + Gmail draft). Theme and note generation use **Groq** LLM.

## Documentation

| Doc | Purpose |
|-----|---------|
| [doc/problemStatement.md](doc/problemStatement.md) | Requirements |
| [doc/architecture.md](doc/architecture.md) | System design (local / Groq / MCP) |
| [doc/phasewiseImplementationPlan.md](doc/phasewiseImplementationPlan.md) | Build phases |
| [doc/decision.md](doc/decision.md) | Decision log |
| [doc/eval/README.md](doc/eval/README.md) | Per-phase testing |
| [data/reviews/README.md](data/reviews/README.md) | **Phase 1 + full LLM/MCP execution guide** |

## Pipelines (by phase)

| Phase | Folder | Integration | Status |
|-------|--------|-------------|--------|
| 0 | [pipelines/phase0_mcp](pipelines/phase0_mcp) | **MCP** (Cursor) | Setup in Cursor |
| 1 | [pipelines/phase1_ingest](pipelines/phase1_ingest) | Local Python | **Implemented** |
| 2 | [pipelines/phase2_themes](pipelines/phase2_themes) | **Groq** LLM | **Implemented** |
| 3 | [pipelines/phase3_note](pipelines/phase3_note) | **Groq** LLM | **Implemented** |
| 4 | [pipelines/phase4_pii](pipelines/phase4_pii) | Local (+ optional Groq) | **Implemented** |
| 5 | [pipelines/phase5_docs_mcp](pipelines/phase5_docs_mcp) | **MCP** Docs (HTTP) | **Implemented** |
| 6 | [pipelines/phase6_gmail_mcp](pipelines/phase6_gmail_mcp) | **MCP** Gmail (HTTP) | **Implemented** |
| 7 | [pipelines/phase7_e2e](pipelines/phase7_e2e) | E2E + **GitHub Actions** | **Implemented** |
| 8 | [pipelines/phase8_frontend](pipelines/phase8_frontend) | Dashboard BFF + React UI | **Implemented** |

---

## Quick start — Phase 1 (local)

```bash
cd /Users/dheerajj/Desktop/Milestone3
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

.venv/bin/python scripts/download_reviews.py --weeks 12
.venv/bin/python scripts/ingest_reviews.py -v
.venv/bin/python scripts/validate_reviews.py
```

**Output:** `data/reviews/normalized.jsonl` — see [data/reviews/README.md](data/reviews/README.md) for the full runbook.

---

## LLM setup (Groq) — Phases 2–3

| Item | Detail |
|------|--------|
| Provider | [Groq](https://groq.com/) |
| API key | `GROQ_API_KEY` in `.env` (gitignored) |
| Default model | `llama-3.3-70b-versatile` |
| Override | `GROQ_MODEL` |

```bash
# .env example — do not commit
GROQ_API_KEY=gsk_xxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile
```

**Phase 2:** `normalized.jsonl` → `data/themes/clusters.json`, `ranked.json` via `prompts/themes.md`  
**Phase 3:** ranked themes → `data/weekly/note.md`, `note.json` via `prompts/system.md`, `prompts/weekly_note.md`

```bash
# Phase 2
python pipelines/phase2_themes/run.py -v
python scripts/validate_themes.py

# Phase 3
python pipelines/phase3_note/run.py -v
python scripts/validate_note.py

# Phase 4 (gate before MCP publish)
python scripts/check_pii.py data/weekly/note.md

# Phase 5 (requires GROWW_PULSE_DOC_ID in .env)
python scripts/publish_doc.py -v

# Phase 6 (requires PULSE_DRAFT_TO in .env)
python scripts/publish_draft.py -v

# Phase 7 — full weekly run
python scripts/run_weekly_pulse.py -v --publish
```

**Runbook:** [doc/runbook.md](doc/runbook.md) · **CI:** [.github/workflows/weekly_pulse.yml](.github/workflows/weekly_pulse.yml)

**Do not** use Groq for Google Docs or Gmail — those are MCP-only.

### Phase 8 — dashboard

```bash
./scripts/serve_dashboard.sh
# or separately: uvicorn on :8080 + `cd frontend && npm run dev`
```

See [pipelines/phase8_frontend/README.md](pipelines/phase8_frontend/README.md) and [doc/eval/phase-08/eval.md](doc/eval/phase-08/eval.md).

---

## MCP setup (Google Workspace) — Phases 0, 5, 6

| Item | Detail |
|------|--------|
| Server | [dheerajmw/MCP-server](https://github.com/dheerajmw/MCP-server) on Render (`MCP_SERVER_URL`) |
| Config | `~/.cursor/mcp.json` or Cursor **Settings → MCP** |
| Auth | Google Cloud OAuth (Desktop); enable Gmail + Docs APIs |
| Usage | Cursor agent calls MCP tools — **no** `googleapis` in this repo |

### Phase 0 checklist

1. Enable Gmail API + Google Docs API in Google Cloud.
2. Add MCP server block to Cursor MCP config (see [pipelines/phase0_mcp](pipelines/phase0_mcp/README.md)).
3. Restart Cursor → complete OAuth in browser.
4. Confirm **Docs** + **Gmail draft** tools appear.
5. Smoke test: create test Doc + Gmail draft via MCP only.

### Phase 5–6 publish (after PII gate)

```bash
.venv/bin/python scripts/check_pii.py data/weekly/note.md   # must pass first
```

Then in **Cursor** (MCP connected):

1. **Docs** — create/update weekly pulse from `data/weekly/note.md` → save IDs in `data/weekly/publish_state.json`
2. **Gmail** — create **draft** to `PULSE_DRAFT_TO` (do not auto-send)

Optional `.env`:

```bash
PULSE_DRAFT_TO=you@example.com
```

Full prompts and troubleshooting: [data/reviews/README.md — MCP procedure](data/reviews/README.md#mcp-procedure-google-workspace--phases-0-5-6).

---

## End-to-end order

```text
Phase 0  MCP setup (Cursor)
Phase 1  download → ingest → normalized.jsonl     ← local
Phase 2  Groq theme clustering
Phase 3  Groq weekly note
Phase 4  check_pii.py (gate)
Phase 5  MCP → Google Doc
Phase 6  MCP → Gmail draft
Phase 7  Full “weekly pulse” runbook in Cursor
Phase 8  Dashboard (BFF + React) — read artifacts, link to Doc/Draft
```

---

## Secrets summary

| Variable | Used for | Committed? |
|----------|----------|------------|
| `GROQ_API_KEY` | Phases 2–3 LLM | No — `.env` only |
| `GROQ_MODEL` | Optional model override | No |
| `GOOGLE_OAUTH_*` | MCP server env in Cursor | No |
| `PULSE_DRAFT_TO` | Gmail draft recipient | No |

---

## Review data sources

| Source | Method | Typical volume |
|--------|--------|----------------|
| Play Store | `google-play-scraper` (public) | Up to 3,000 recent reviews |
| App Store | Apple iTunes RSS (public) | Up to ~500 reviews |

Official App Store Connect / Play Console CSV exports are preferred when you have developer access.
