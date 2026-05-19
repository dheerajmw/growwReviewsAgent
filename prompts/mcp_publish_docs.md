# Phase 5 — Publish weekly note to Google Doc (MCP HTTP server)

## Prerequisites

1. Phase 4 passed: `python scripts/check_pii.py data/weekly/note.md`
2. MCP server running: [MCP-server](https://github.com/dheerajmw/MCP-server) at `MCP_SERVER_URL` (default Render deploy)
3. `GROWW_PULSE_DOC_ID` set — create a Google Doc once, copy ID from the URL

## Publish (local script calls MCP server only)

```bash
export GROWW_PULSE_DOC_ID="your-doc-id"
python scripts/publish_doc.py -v
```

The script POSTs to `/append_to_doc` on the MCP server. **No** `googleapis` in this repository.

## Agent rule

> For Google Docs, call the deployed MCP server (`append_to_doc`) or run `scripts/publish_doc.py`. Never add Google Docs API client code to Milestone3.

## Idempotency

Same `week_ending` as last successful publish → skipped unless `--force`. Same `doc_id` is reused (append-only server).
