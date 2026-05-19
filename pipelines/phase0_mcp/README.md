# Phase 0 — MCP & Project Scaffold

**Status:** Configure in Cursor (no Python package in this folder).

**Objective:** Google Workspace MCP connected; **Docs** + **Gmail draft** tools available for Phases 5–6.

**Evaluation:** [doc/eval/phase-00/eval.md](../../doc/eval/phase-00/eval.md)

---

## Procedure

### 1. Google Cloud

1. Create or select a project.
2. Enable **Gmail API** and **Google Docs API** (enable **Google Drive API** if your MCP server README requires it).
3. **APIs & Services → Credentials → Create OAuth client ID → Desktop app**.
4. Note **Client ID** and **Client secret** (or download JSON per MCP server instructions).

### 2. Install MCP server

Recommended: [Google Workspace MCP](https://github.com/Dave-Nguyen-PM/google-workplace-mcp)

Follow that repo’s README for `npx` / Node requirements.

### 3. Cursor configuration

Add the server in **Cursor Settings → MCP** or edit `~/.cursor/mcp.json`. Example structure (replace with values from the MCP README):

```json
{
  "mcpServers": {
    "google-workspace": {
      "command": "npx",
      "args": ["-y", "<mcp-package-name>"],
      "env": {
        "GOOGLE_OAUTH_CLIENT_ID": "xxxx.apps.googleusercontent.com",
        "GOOGLE_OAUTH_CLIENT_SECRET": "xxxx"
      }
    }
  }
}
```

Restart Cursor after saving.

### 4. Authorize

**Option A — project `auth.py` (token for local scripts / reference):**

```bash
pip install google-auth-oauthlib
python3 auth.py
```

Requires `credentials.json` in repo root. Writes **`token.json`** (gitignored) after browser consent.

**Option B — MCP server (typical for Cursor):**

1. Open MCP panel — server should show **connected**.
2. On first tool use, complete **browser OAuth** for the Google account that will own Docs and drafts (tokens cached by the MCP server, often `~/.google-workspace-mcp/tokens.json`).
3. Confirm tools include at least:
   - Google **Docs** (create / read / update)
   - **Gmail** create **draft** (not send-only unless you add send later)

### 5. Smoke test (Cursor chat)

```
Using only Google Workspace MCP tools (no googleapis code):
1) Create a Google Doc titled "MCP Smoke Test — Milestone3" with body "Phase 0 OK".
2) Create a Gmail draft to myself with subject "MCP Smoke Test" and the same body.
```

Delete the test Doc and draft when done.

### 6. Agent rule (recommended)

Save to `prompts/mcp_publish.md` or `.cursor/rules/`:

> For Google Docs and Gmail, always use MCP tools in Cursor. Never add Gmail or Docs REST/SDK clients to this repository.

---

## What not to do

- Do **not** add `googleapis`, `google-auth`, or hand-rolled OAuth refresh logic in `scripts/` for Docs/Gmail ([decision D-007](../../doc/decision.md)).
- Do **not** publish (Phases 5–6) before Phase 4 PII check passes.

---

## Next phases

| After Phase 0 | Uses MCP? |
|---------------|-----------|
| [Phase 1 — Ingest](../phase1_ingest/README.md) | No — local Python |
| [Phase 2–3 — Groq LLM](../phase2_themes/README.md) | No — `GROQ_API_KEY` |
| [Phase 5 — Docs](../phase5_docs_mcp/README.md) | **Yes** |
| [Phase 6 — Gmail](../phase6_gmail_mcp/README.md) | **Yes** |

**Full MCP + LLM runbook:** [data/reviews/README.md](../../data/reviews/README.md)
