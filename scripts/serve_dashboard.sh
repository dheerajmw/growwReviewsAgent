#!/usr/bin/env bash
# Start Phase 8 BFF + Vite dev server from repo root.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi

if [[ ! -d frontend/node_modules ]]; then
  (cd frontend && npm install)
fi

trap 'kill 0' EXIT
.venv/bin/python -m uvicorn pipelines.phase8_frontend.api.main:app --reload --port 8080 &
(cd frontend && npm run dev) &
wait
