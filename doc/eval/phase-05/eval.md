# Phase 5 Evaluation — Google Docs Publish (MCP)

**Plan:** [Phase 5](../../phasewiseImplementationPlan.md#phase-5--publish-weekly-note-to-google-docs-mcp) · **Depends on:** [Phase 0](../phase-00/eval.md), [Phase 4](../phase-04/eval.md) complete

---

## Prerequisites

- Phase 4 PII gate passed on `data/weekly/note.md`
- Google Workspace MCP connected (Phase 0)
- Sanitized note ready for publish

---

## Automated checks

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | No Docs API in repo | `rg -i "google.docs|docs\.googleapis|googleapis.*docs" --glob '!doc/**'` | Zero app-code matches |
| A2 | Publish state written | `test -f data/weekly/publish_state.json` | File exists after publish run |
| A3 | State schema | `python3 -c "import json; s=json.load(open('data/weekly/publish_state.json')); assert all(k in s for k in ['doc_id','doc_url','published_at'])"` | Required keys present |
| A4 | PII gate before publish | Workflow order in runbook/agent | `check_pii.py` run logged immediately before MCP Doc call |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | MCP tool invocation | Cursor log / transcript shows **MCP** Docs tool (not HTTP curl to Google) |
| M2 | Open `doc_url` in browser | Doc title: `Weekly Review Pulse — Groww — YYYY-MM-DD` (or agreed convention) |
| M3 | Body match | Doc body matches `note.md` (formatting may differ; content equivalent) |
| M4 | Idempotency | Re-run same calendar week | Same `doc_id` updated, not duplicate Docs (unless policy says new Doc per run) |
| M5 | Word limit in Doc | Still ≤250 words of substance |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** Google Doc created/updated via **MCP only**
- [ ] **E2** `publish_state.json` has `doc_id`, `doc_url`, `published_at`
- [ ] **E3** Doc content matches sanitized `note.md`
- [ ] **E4** No `googleapis` / Google Docs SDK code in repository
- [ ] **E5** Phase 4 PII check passed before this publish

**Phase 5 complete when:** E1–E5 checked and A1–A4 pass.

---

## MCP publish smoke script (agent prompt)

Use in Cursor once:

> Read `data/weekly/note.md`. Using **only** Google Workspace MCP Docs tools, create or update the weekly pulse document. Save returned document id and URL to `data/weekly/publish_state.json`.

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| 403 from MCP | Token expired | Re-run OAuth for MCP server |
| Empty Doc | Wrong tool (create vs append) | Read MCP tool schema; use append/update after create |
| Duplicate Docs | No idempotency | Persist `doc_id`; update instead of create |

**Evaluator:** _______________ **Date:** _______________
