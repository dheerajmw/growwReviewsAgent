# Phase 6 — Gmail draft (MCP HTTP server)

## Prerequisites

1. Phase 4: `python scripts/check_pii.py data/weekly/note.md`
2. `PULSE_DRAFT_TO` in `.env` (recipient for the draft)
3. MCP server: `MCP_SERVER_URL` (default Render deploy)

## Create draft (draft only — never send)

```bash
python scripts/publish_draft.py -v
```

Updates `data/weekly/publish_state.json` with `draft_id`, `draft_to`, `draft_created_at`.
