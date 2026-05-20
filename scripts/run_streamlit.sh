#!/usr/bin/env bash
# Start local BFF + Streamlit UI (fixes connection refused on :8080)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt -r requirements-streamlit.txt
fi

export PULSE_API_URL="${PULSE_API_URL:-http://127.0.0.1:8080}"

trap 'kill 0' EXIT
.venv/bin/python -m uvicorn pipelines.phase8_frontend.api.main:app --host 127.0.0.1 --port 8080 &
sleep 2
.venv/bin/streamlit run streamlit_app.py --server.port 8501
