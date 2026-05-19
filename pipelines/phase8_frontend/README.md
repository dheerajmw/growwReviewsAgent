# Phase 8 — Web dashboard (BFF + React)

Read-only dashboard for the weekly review pulse. Serves pipeline artifacts from `data/` — no Groq or Google APIs in this layer.

## Stack

| Layer | Path | Role |
|-------|------|------|
| BFF | `api/` | FastAPI — `/api/v1/*` from disk |
| UI | `../../frontend/` | Vite + React + Tailwind |

## Run locally

From repo root:

```bash
# API (port 8080 — avoids MCP server on :8000)
python -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m uvicorn pipelines.phase8_frontend.api.main:app --reload --port 8080

# UI (port 5173, proxies /api → 8080)
cd frontend && npm install && npm run dev
```

Or use the helper script:

```bash
./scripts/serve_dashboard.sh
```

Open http://localhost:5173

## API routes

| Method | Path | Source |
|--------|------|--------|
| GET | `/api/v1/health` | Liveness |
| GET | `/api/v1/pulse/latest` | `data/weekly/note.json`, `note.md` |
| GET | `/api/v1/pulse/weeks` | History + publish state |
| GET | `/api/v1/themes/ranked` | `data/themes/ranked.json` |
| GET | `/api/v1/themes/clusters` | `data/themes/clusters.json` (summary) |
| GET | `/api/v1/pipeline/status` | Artifact presence + PII gate |
| GET | `/api/v1/publish/state` | `data/weekly/publish_state.json` |

## Eval

See [doc/eval/phase-08/eval.md](../../doc/eval/phase-08/eval.md).

```bash
cd frontend && npm run build
curl -s http://127.0.0.1:8080/api/v1/health
curl -s http://127.0.0.1:8080/api/v1/pulse/latest | head
```

## Constraints

- No `googleapis` in frontend or Phase 8 API.
- Doc/Gmail links only — publish stays in MCP scripts / CI.
- No PII fields in API responses or UI.
