# Normalized reviews (Phase 1 output)

This folder holds the **canonical review dataset** for Milestone 3. Phase 2 (theme clustering) reads from here; do not start Phase 2 until `normalized.jsonl` exists and passes validation.

**Primary artifact:** `normalized.jsonl` — one JSON object per line (UTF-8).

---

## Prerequisites

1. **Repo root** as working directory: `/Users/dheerajj/Desktop/Milestone3` (or your clone path).
2. **Python 3.9+** and a virtualenv (recommended).
3. **Raw exports** in [`../raw/`](../raw/README.md):
   - `data/raw/app_store*.csv` (or `.json`)
   - `data/raw/play_store*.csv` (or `.json`)

If you do not have console exports, download public Groww reviews first (see step 1 below).

---

## Execution guide (end-to-end)

### 1. One-time setup

```bash
cd /Users/dheerajj/Desktop/Milestone3
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 2. Get raw reviews (8–12 weeks)

**Option A — Download public reviews (recommended for this repo)**

```bash
.venv/bin/python scripts/download_reviews.py --weeks 12
```

| Store | Source | Typical rows |
|-------|--------|-------------|
| Play | `google-play-scraper`, `com.nextbillion.groww`, country `in` | up to 3,000 |
| App Store | iTunes RSS, app id `1404871703` | up to ~500 |

Writes `data/raw/play_store.csv` and `data/raw/app_store.csv`.

**Option B — Your own exports**

Copy App Store Connect / Play Console CSV or JSON into `data/raw/` using names that match `app_store*` and `play_store*` (see [`configs/phase1_ingest.yaml`](../../configs/phase1_ingest.yaml)).

**Option C — Offline sample fixtures**

```bash
.venv/bin/python pipelines/phase1_ingest/generate_sample_exports.py
```

### 3. Ingest and normalize

```bash
.venv/bin/python scripts/ingest_reviews.py -v
```

What this does:

- Reads all matching files in `data/raw/`
- Keeps reviews in the **12-week** window (override with `--weeks 8` … `12`)
- Applies **content normalization** (see below)
- Deduplicates by `review_id`
- Writes **`data/reviews/normalized.jsonl`**

Verbose log ends with a summary, for example:

```text
In window: …
Filtered (normalization): {'too_few_words': …, 'non_english': …, 'contains_emoji': …}
Written: …
```

### 4. Validate output

```bash
.venv/bin/python scripts/validate_reviews.py
```

Pass criteria:

- Exit code `0`
- Both `app_store` and `play_store` present
- Every row: `rating` 1–5, non-empty `text`, ISO `date`, required fields

### 5. Optional checks

```bash
# Line count
wc -l data/reviews/normalized.jsonl

# Store mix
.venv/bin/python -c "
import json
from collections import Counter
c = Counter()
for line in open('data/reviews/normalized.jsonl'):
    c[json.loads(line)['store']] += 1
print(dict(c))
"

# Unit tests (Phase 1)
.venv/bin/python -m unittest tests.test_phase1_filters tests.test_phase1_ingest -v
```

**Phase 1 sign-off:** [doc/eval/phase-01/eval.md](../../doc/eval/phase-01/eval.md)

---

## Canonical schema (each JSON line)

| Field | Type | Notes |
|-------|------|--------|
| `rating` | int | 1–5 |
| `title` | string | May be `""` on Play Store |
| `text` | string | Non-empty review body |
| `date` | string | ISO 8601 UTC, e.g. `2026-05-10T00:00:00Z` |
| `store` | string | `app_store` or `play_store` |
| `review_id` | string | **Internal only** — dedup/QA; never put in Doc, email, or weekly note |

Example:

```json
{"rating": 4, "title": "Smooth SIP setup", "text": "Setting up monthly SIP was quick and the UI is clean.", "date": "2026-05-10T00:00:00Z", "store": "play_store", "review_id": "play_store:abc123"}
```

---

## Content normalization (applied at ingest)

Configured in [`configs/phase1_ingest.yaml`](../../configs/phase1_ingest.yaml) → `normalization`:

| Rule | Default | Logged skip reason |
|------|---------|-------------------|
| ≥ **6** English words (title + body) | on | `too_few_words` |
| **English only** (`langdetect`) | on | `non_english` |
| **No emoji** / emoticons | on | `contains_emoji` |

To change rules, edit the YAML and re-run ingest.

---

## CLI reference

| Command | Purpose |
|---------|---------|
| `scripts/ingest_reviews.py -v` | Ingest + validate (default) |
| `scripts/ingest_reviews.py --weeks 10` | 8–12 week window |
| `scripts/ingest_reviews.py --no-validate` | Ingest only |
| `scripts/validate_reviews.py` | Validate existing JSONL |
| `pipelines/phase1_ingest/run.py` | Same as ingest (alternate entry) |

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `No App Store export found` | Add `data/raw/app_store.csv` or run `scripts/download_reviews.py` |
| `No Play Store export found` | Add `data/raw/play_store.csv` or run download script |
| `Written: 0` | Check date window; raw dates may be outside `--weeks` |
| Very few rows after ingest | Expected if many reviews fail normalization; inspect `Filtered (normalization)` in log |
| Validation: missing store | Ensure both `app_store` and `play_store` files exist and have in-window rows |

---

## Full pipeline: local scripts vs LLM vs MCP

After `normalized.jsonl` exists, the milestone uses **three integration modes**:

| Mode | Phases | Technology | Secrets |
|------|--------|------------|---------|
| **Local Python** | 1, 4 (validators) | `scripts/*.py`, pipelines | None |
| **LLM (Groq)** | 2, 3 (optional 4 redaction) | Groq Chat Completions API | `GROQ_API_KEY` |
| **MCP (Google)** | 5, 6 | Google Workspace MCP in **Cursor** | OAuth via MCP server |

**Rule:** Do **not** add `googleapis` / Gmail / Docs SDK code in this repo for publish. Google surfaces are **MCP-only** ([decision D-007](../../doc/decision.md)).

---

## LLM procedure (Groq) — Phases 2–3+

Theme clustering and weekly note generation use **[Groq](https://groq.com/)**, not OpenAI/Anthropic clients in application code.

### One-time Groq setup

1. Create an API key at [console.groq.com](https://console.groq.com/).
2. Add to repo root `.env` (never commit):

```bash
# .env (gitignored)
GROQ_API_KEY=gsk_xxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile   # optional; this is the default
```

3. Load before running Phase 2+ scripts or tell Cursor the variable is set in your environment.

### Phase 2 — Theme clustering (Groq)

**Input:** `data/reviews/normalized.jsonl`  
**Outputs:** `data/themes/clusters.json`, `data/themes/ranked.json`

**Procedure (when implemented):**

```bash
# Ensure Groq key is set
export $(grep -v '^#' .env | xargs)   # or: set -a && source .env && set +a

.venv/bin/python scripts/cluster_themes.py -v   # planned entry point
# OR run from Cursor agent with prompts/themes.md
```

**Agent prompt (Cursor):**

> Read `data/reviews/normalized.jsonl`. Using Groq (`GROQ_API_KEY`), assign each review to one of ≤5 themes (onboarding, KYC, payments, statements, withdrawals). Return JSON only per `prompts/themes.md`. Write `data/themes/clusters.json` and `data/themes/ranked.json`.

| Setting | Value |
|---------|--------|
| Provider | Groq |
| Default model | `llama-3.3-70b-versatile` |
| Override | `GROQ_MODEL` env var |
| Prompt | `prompts/themes.md` |

**Eval:** [doc/eval/phase-02/eval.md](../../doc/eval/phase-02/eval.md)

### Phase 3 — Weekly note (Groq)

**Input:** `data/themes/ranked.json` (+ clusters)  
**Outputs:** `data/weekly/note.md`, `data/weekly/note.json` (≤250 words)

```bash
.venv/bin/python pipelines/phase3_note/run.py -v
.venv/bin/python scripts/validate_note.py
```

`--dry-run` skips Groq (heuristic note for CI). Config: `configs/phase3_note.yaml`. See [pipelines/phase3_note/README.md](../../pipelines/phase3_note/README.md).

### Phase 4 — PII gate (before any Google publish)

```bash
.venv/bin/python scripts/check_pii.py data/weekly/note.md
# optional: .venv/bin/python pipelines/phase4_pii/run.py --redact -v
```

See [pipelines/phase4_pii/README.md](../../pipelines/phase4_pii/README.md).

If PII check fails, stop — do **not** call MCP. Optional: Groq redaction pass, then re-run `check_pii.py`.

---

## MCP procedure (Google Workspace) — Phases 0, 5, 6

Google **Docs** and **Gmail** are reached only through the **Google Workspace MCP server** inside Cursor ([problem statement](../../doc/problemStatement.md#integration-approach--mcp-not-direct-apis)).

### Phase 0 — One-time MCP setup (do this before Phase 5)

1. **Google Cloud**
   - Create a project → enable **Gmail API** and **Google Docs API** (and **Drive** if your MCP server requires it).
   - Create **OAuth 2.0 Desktop** credentials; download client JSON if the MCP server asks for it.

2. **Install MCP server** — default: [Google Workspace MCP](https://github.com/Dave-Nguyen-PM/google-workplace-mcp) (or course-approved equivalent with Docs + Gmail **draft** tools).

3. **Configure Cursor** — add to `~/.cursor/mcp.json` (example shape; follow the server README for exact `command` / `args` / `env`):

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "npx",
      "args": ["-y", "<package-from-mcp-readme>"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "your-client-id",
        "GOOGLE_OAUTH_CLIENT_SECRET": "your-client-secret"
      }
    }
  }
}
```

4. **Restart Cursor** → open **Settings → MCP** (or MCP tools panel).
5. **Authorize** — complete browser OAuth once when prompted.
6. **Smoke test** — in Cursor chat:

> Using **only** Google Workspace MCP tools: create a Doc titled `MCP Smoke Test`, then create a Gmail draft to me with subject `MCP Smoke Test` and body `OK`. Do not use googleapis in code.

7. Confirm **Docs** and **Gmail** tools appear and smoke test succeeds.

**Eval:** [doc/eval/phase-00/eval.md](../../doc/eval/phase-00/eval.md) · [pipelines/phase0_mcp/README.md](../../pipelines/phase0_mcp/README.md)

### Phase 5 — Publish Google Doc (HTTP MCP server)

**Server:** [dheerajmw/MCP-server](https://github.com/dheerajmw/MCP-server) · `MCP_SERVER_URL=https://mcp-server-p01x.onrender.com`

**Prerequisites:** Phase 4 passed; create a Google Doc once and set `GROWW_PULSE_DOC_ID` in `.env`.

```bash
.venv/bin/python scripts/check_pii.py data/weekly/note.md
.venv/bin/python scripts/publish_doc.py -v
```

Open `doc_url` from `data/weekly/publish_state.json`. Same week re-run is skipped unless `--force` (append-only server).

**Eval:** [doc/eval/phase-05/eval.md](../../doc/eval/phase-05/eval.md) · [pipelines/phase5_docs_mcp/README.md](../../pipelines/phase5_docs_mcp/README.md)

### Phase 6 — Gmail draft (HTTP MCP server)

**Prerequisites:** Phase 4 passed; set `PULSE_DRAFT_TO` in `.env`.

```bash
.venv/bin/python scripts/check_pii.py data/weekly/note.md
.venv/bin/python scripts/publish_draft.py -v
```

Draft only — never auto-sent. Check Gmail → **Drafts**. Updates `publish_state.json` with `draft_id`.

**Eval:** [doc/eval/phase-06/eval.md](../../doc/eval/phase-06/eval.md) · [pipelines/phase6_gmail_mcp/README.md](../../pipelines/phase6_gmail_mcp/README.md)

### MCP troubleshooting

| Issue | Fix |
|-------|-----|
| No MCP tools in Cursor | Check `mcp.json`, restart Cursor, verify server starts in MCP logs |
| OAuth / 403 | Re-authorize; confirm APIs enabled in Google Cloud |
| Agent writes `googleapis` code | Reject; use MCP tools only ([D-007](../../doc/decision.md)) |
| PII in Doc/draft | Run Phase 4 `check_pii.py` **before** Phase 5/6 |

---

## Downstream checklist (from this folder)

| Step | Phase | Tool | Artifact |
|------|-------|------|----------|
| ✅ Done | 1 | Local ingest | `normalized.jsonl` (here) |
| ☐ | 2 | **Groq** | `data/themes/clusters.json`, `ranked.json` |
| ☐ | 3 | **Groq** | `data/weekly/note.md`, `note.json` |
| ☐ | 4 | Local + optional Groq | PII-clean note |
| ☐ | 0/5 | **MCP** Docs | Google Doc + `publish_state.json` |
| ☐ | 6 | **MCP** Gmail | Draft in mailbox |
| ☐ | 7 | E2E + GHA scheduler | `run_weekly_pulse.py` + [weekly_pulse.yml](../../.github/workflows/weekly_pulse.yml) |

**Runbook:** [doc/runbook.md](../../doc/runbook.md) · **Next:** `python scripts/run_weekly_pulse.py -v --publish`

---

## Related docs

- [Phase 1 pipeline](../../pipelines/phase1_ingest/README.md)
- [Phase 0 MCP](../../pipelines/phase0_mcp/README.md)
- [Architecture — ingest](../../doc/architecture.md#31-ingest-pipeline-local)
- [Architecture — Groq theme engine](../../doc/architecture.md#32-theme-engine-local--groq-llm)
- [Architecture — MCP publish](../../doc/architecture.md#35-mcp-publish-layer-google-only-via-mcp)
- [Phasewise plan](../../doc/phasewiseImplementationPlan.md)
- [Runbook](../../doc/runbook.md)
- [Eval index](../../doc/eval/README.md)
