#!/usr/bin/env bash
# Build React UI for production (Render static site or local preview).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/frontend"

API_URL="${VITE_API_BASE_URL:-https://groww-pulse-api.onrender.com}"
echo "Building frontend with VITE_API_BASE_URL=$API_URL"
export VITE_API_BASE_URL="$API_URL"

npm install
npm run build

echo "Done. Output: frontend/dist"
echo "Deploy on Render as groww-pulse-ui (see render.yaml) or set Streamlit secret:"
echo '  PULSE_UI_URL = "https://groww-pulse-ui.onrender.com"'
