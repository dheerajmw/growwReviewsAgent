# Phase 5 — Google Docs publish (HTTP MCP)

**Plan:** [Phase 5](../../doc/phasewiseImplementationPlan.md#phase-5--publish-weekly-note-to-google-docs-mcp) · **Eval:** [phase-05 eval](../../doc/eval/phase-05/eval.md)

Publishes `data/weekly/note.md` by calling your deployed [MCP-server](https://github.com/dheerajmw/MCP-server) (`POST /append_to_doc`). **No** `googleapis` in this repository.

## One-time setup

1. **Google Cloud** — Enable Docs API; OAuth on the MCP server (Render: `GOOGLE_CREDENTIALS_JSON`, `GOOGLE_TOKEN_JSON`).
2. **Create a Google Doc** — e.g. title `Weekly Review Pulse — Groww`. Share edit access with the OAuth account.
3. **Copy Doc ID** from URL: `https://docs.google.com/document/d/DOC_ID/edit`
4. **`.env`:**

```bash
MCP_SERVER_URL=https://mcp-server-p01x.onrender.com
GROWW_PULSE_DOC_ID=your-doc-id-here
```

## Publish

```bash
python scripts/check_pii.py data/weekly/note.md
python scripts/publish_doc.py -v
```

| Flag | Effect |
|------|--------|
| `--dry-run` | Writes `publish_state.json` without HTTP call |
| `--force` | Append again even if same week already published |
| `--health` | Ping MCP server only |

## Outputs

`data/weekly/publish_state.json` — `doc_id`, `doc_url`, `published_at`, `week_ending`

**Depends on:** [Phase 4](../phase4_pii/README.md) PII gate · [Phase 3](../phase3_note/README.md) note

**Note:** The MCP server **appends** content; it does not create new Docs. Use one Doc per pulse log or create new Docs manually if needed.
