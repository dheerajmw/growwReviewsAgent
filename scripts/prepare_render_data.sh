#!/usr/bin/env bash
# Copy pipeline artifacts into deploy/data/ for committing or Render upload.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/deploy/data"
mkdir -p "$DEST/weekly" "$DEST/themes" "$DEST/reviews"

copy_if() {
  if [[ -f "$1" ]]; then
    cp "$1" "$2"
    echo "copied $1"
  fi
}

copy_if "$ROOT/data/weekly/note.json" "$DEST/weekly/note.json"
copy_if "$ROOT/data/weekly/note.md" "$DEST/weekly/note.md"
copy_if "$ROOT/data/weekly/publish_state.json" "$DEST/weekly/publish_state.json"
copy_if "$ROOT/data/weekly/blockers.json" "$DEST/weekly/blockers.json"
copy_if "$ROOT/data/themes/ranked.json" "$DEST/themes/ranked.json"
copy_if "$ROOT/data/themes/clusters.json" "$DEST/themes/clusters.json"
copy_if "$ROOT/data/reviews/normalized.jsonl" "$DEST/reviews/normalized.jsonl"

echo "Done. On Render set PULSE_DATA_ROOT=$ROOT/deploy (or commit deploy/data and use repo root + deploy/data layout)."
echo "Or set PULSE_DATA_ROOT to $DEST if BFF should read only deploy bundle."
