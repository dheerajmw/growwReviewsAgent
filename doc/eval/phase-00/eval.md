# Phase 0 Evaluation — MCP Setup & Project Scaffold

**Plan:** [Phase 0](../../phasewiseImplementationPlan.md#phase-0--mcp-setup-and-project-scaffold) · **Architecture:** [MCP publish layer](../../architecture.md#35-mcp-publish-layer-google-only-via-mcp)

---

## Prerequisites

- Google Cloud project with OAuth 2.0 Desktop client
- Gmail API and Google Docs API enabled
- [Google Workspace MCP](https://github.com/Dave-Nguyen-PM/google-workplace-mcp) (or approved equivalent) installed per server README
- Cursor with MCP configuration access

---

## Automated checks

| # | Check | Command / action | Pass condition |
|---|--------|------------------|----------------|
| A1 | No Google API clients in repo | `rg -i "googleapis|google-auth|@google-cloud" --glob '!doc/**'` from repo root | Zero matches in application code (doc references OK) |
| A2 | Folder scaffold | `test -d data/raw && test -d data/reviews && test -d prompts && test -d scripts` | All directories exist |
| A3 | Secrets gitignored | `rg "data/raw|\.env|token|credentials" .gitignore` | Patterns present in `.gitignore` |
| A4 | MCP config file exists | `test -f ~/.cursor/mcp.json` or MCP entry visible in Cursor Settings | Server block configured |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | Open Cursor → MCP / Tools panel | Server listed (e.g. `google-workspace`); status connected |
| M2 | List available tools | At least one **Google Docs** tool (create/read/write) and one **Gmail** tool (create draft) |
| M3 | Agent smoke test — Docs | Create Doc titled `MCP Smoke Test — <date>` with body `Phase 0 OK` | Doc opens in browser with correct title/body |
| M4 | Agent smoke test — Gmail | Create draft to yourself; subject `MCP Smoke Test` | Draft appears in Gmail → Drafts |
| M5 | Cleanup | Delete smoke Doc and draft | No leftover test artifacts required for Phase 1 |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** MCP server connected; Docs + Gmail tools visible
- [ ] **E2** Smoke Doc and draft created via MCP only (no `googleapis` in repo)
- [ ] **E3** `data/`, `prompts/`, `scripts/` scaffold present
- [ ] **E4** `.gitignore` excludes raw exports, tokens, `.env`
- [ ] **E5** OAuth completed once; reconnection works after Cursor restart

**Phase 0 complete when:** E1–E5 checked and A1–A4 pass.

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| MCP tools empty | Server not started / wrong `mcp.json` | Re-read server README; fix command/args/env |
| OAuth loop | Redirect URI mismatch | Use Desktop OAuth client; check redirect in Cloud Console |
| Docs tool works, Gmail fails | Gmail API not enabled or scope missing | Enable Gmail API; re-authorize with draft scope |
| `googleapis` found in repo | Scaffold added API client | Remove; use MCP only per architecture |

---

## Evidence to retain

- Screenshot or link of smoke-test Google Doc (optional)
- Copy of MCP server name and tool list (paste into PR or notes)

**Evaluator:** _______________ **Date:** _______________
