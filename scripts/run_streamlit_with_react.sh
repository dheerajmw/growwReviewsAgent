#!/usr/bin/env bash
# BFF + Vite dev server + Streamlit embedding React (matches Streamlit Cloud)
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

export PULSE_API_URL="${PULSE_API_URL:-http://127.0.0.1:8080}"
export PULSE_UI_URL="${PULSE_UI_URL:-http://localhost:5173}"

trap 'kill 0' EXIT
.venv/bin/python -m uvicorn pipelines.phase8_frontend.api.main:app --host 127.0.0.1 --port 8080 &
(cd frontend && npm run dev -- --host 127.0.0.1 --port 5173) &
sleep 4
.venv/bin/streamlit run streamlit_app.py --server.port 8501
