# Phase 6 Evaluation — Gmail Draft (MCP)

**Plan:** [Phase 6](../../phasewiseImplementationPlan.md#phase-6--gmail-draft-via-mcp) · **Depends on:** [Phase 5](../phase-05/eval.md) complete

---

## Prerequisites

- `data/weekly/note.md` PII-clean (Phase 4)
- Google Doc published (Phase 5) — optional cross-check
- `PULSE_DRAFT_TO` env var or documented recipient
- Gmail MCP tools available (Phase 0)

---

## Automated checks

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | No Gmail API in repo | `rg -i "gmail\.googleapis|googleapis.*gmail|GmailService" --glob '!doc/**'` | Zero app-code matches |
| A2 | Draft state in publish file | `python3 -c "import json; s=json.load(open('data/weekly/publish_state.json')); assert 'draft_id' in s"` | `draft_id` recorded |
| A3 | Recipient configured | `test -n \"$PULSE_DRAFT_TO\"` or documented in `.env.example` | Target email defined |
| A4 | Email not auto-sent | Workflow review | Only `create_draft` used; no `send` unless out-of-scope and explicit |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | MCP tool invocation | Transcript shows Gmail MCP **create draft** tool |
| M2 | Gmail → Drafts | Draft exists for `PULSE_DRAFT_TO` |
| M3 | Subject | `Groww Weekly Review Pulse — YYYY-MM-DD` (or documented pattern) |
| M4 | Body | Matches `note.md` (plain or HTML) |
| M5 | Not in Sent | Mail remains in Drafts only |
| M6 | Consistency with Doc | Theme/quote/action content aligns with Phase 5 Doc |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** Gmail draft created via **MCP only**
- [ ] **E2** `publish_state.json` includes `draft_id` (and optionally `draft_url`)
- [ ] **E3** Recipient is self or team alias (not arbitrary external list)
- [ ] **E4** No Gmail API client code in repository
- [ ] **E5** Draft not sent automatically

**Phase 6 complete when:** E1–E5 checked and A1–A4 pass.

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Draft to wrong address | Env not loaded | Set `PULSE_DRAFT_TO` in MCP env or agent context |
| Empty body | Wrong MCP parameter names | Read tool schema for `body` / `message` field |
| Send instead of draft | Wrong tool | Use draft-specific MCP tool only |

**Evaluator:** _______________ **Date:** _______________
