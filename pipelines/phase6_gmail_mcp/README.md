# Phase 6 — Gmail draft (HTTP MCP)

**Plan:** [Phase 6](../../doc/phasewiseImplementationPlan.md#phase-6--gmail-draft-via-mcp) · **Eval:** [phase-06 eval](../../doc/eval/phase-06/eval.md)

Creates a **draft only** (never sends) via [MCP-server](https://github.com/dheerajmw/MCP-server) `POST /create_email_draft`.

## Setup

```bash
# .env
MCP_SERVER_URL=https://mcp-server-p01x.onrender.com
PULSE_DRAFT_TO=your-email@example.com
```

Gmail API must be enabled and OAuth on the MCP server (Render env vars).

## Run

```bash
python scripts/check_pii.py data/weekly/note.md
python scripts/publish_draft.py -v
```

Appends `draft_id`, `draft_to`, `draft_created_at` to `data/weekly/publish_state.json`.

Open Gmail → **Drafts** to review. Do not use a send endpoint.

**Depends on:** [Phase 4](../phase4_pii/README.md) · [Phase 5](../phase5_docs_mcp/README.md) (optional Doc link in body)
