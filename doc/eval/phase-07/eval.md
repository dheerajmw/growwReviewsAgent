# Phase 7 Evaluation — End-to-End Agent Workflow

**Plan:** [Phase 7](../../phasewiseImplementationPlan.md#phase-7--end-to-end-agent-workflow-and-hardening) · **Depends on:** Phases [0](../phase-00/eval.md)–[6](../phase-06/eval.md) complete

---

## Prerequisites

- All phase evals 0–6 signed off
- [doc/runbook.md](../../runbook.md) and `scripts/run_weekly_pulse.py`
- `.github/workflows/weekly_pulse.yml` configured with `GROQ_API_KEY` secret
- Optional: `.cursor/rules/google-mcp-only.mdc`

---

## End-to-end test procedure

Run **one full weekly pulse** from clean exports (or fixed fixture set):

| Step | Action | Phase eval |
|------|--------|------------|
| 1 | Place fresh exports in `data/raw/` | [Phase 1](../phase-01/eval.md) |
| 2 | `python3 scripts/ingest_reviews.py` | Phase 1 |
| 3 | Generate themes → `clusters.json`, `ranked.json` | [Phase 2](../phase-02/eval.md) |
| 4 | Generate `note.md` / `note.json` | [Phase 3](../phase-03/eval.md) |
| 5 | `python3 scripts/validate_note.py` | Phase 3 |
| 6 | `python3 scripts/check_pii.py` | [Phase 4](../phase-04/eval.md) |
| 7 | Agent: MCP publish Doc | [Phase 5](../phase-05/eval.md) |
| 8 | Agent: MCP create Gmail draft | [Phase 6](../phase-06/eval.md) |

Or one command: `python scripts/run_weekly_pulse.py -v --publish`

**Timebox:** Excluding export download, complete steps 2–8 in **≤30 minutes**.

---

## Automated checks (regression bundle)

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | Full script chain | `python3 scripts/ingest_reviews.py && python3 scripts/validate_note.py && python3 scripts/check_pii.py data/weekly/note.md` | All exit `0` (after theme/note generation) |
| A2 | Theme cap | Phase 2 validator | Still ≤5 themes |
| A3 | No Google SDKs | `rg -i "googleapis|google-auth" --glob '!doc/**'` | Zero in app code |
| A4 | Publish state complete | JSON has `doc_id`, `doc_url`, `draft_id`, `published_at` | All keys present after E2E |
| A5 | Second run idempotency | Re-run same week | Same `doc_id`; new `draft_id` acceptable |
| A6 | Orchestration script | `python3 scripts/run_weekly_pulse.py --help` | Exits 0 |
| A7 | GHA workflow file | `test -f .github/workflows/weekly_pulse.yml` | Present |
| A8 | Scheduler refresh | Actions → Weekly pulse → Run workflow (refresh-data) | Job succeeds; artifacts uploaded |
| A9 | GHA validate job | Push/PR to `main` | `validate` job passes (no Groq) |

---

## Problem statement deliverables matrix

| Deliverable | Verified | Reference |
|-------------|----------|-----------|
| Import 8–12 weeks of reviews | ☐ | [problemStatement](../../problemStatement.md) |
| ≤5 themes | ☐ | Phase 2 eval |
| Weekly note: top 3 themes, 3 quotes, 3 actions | ☐ | Phase 3 eval |
| ≤250 words | ☐ | Phase 3 eval |
| Google Doc via MCP | ☐ | Phase 5 eval |
| Gmail draft via MCP | ☐ | Phase 6 eval |
| No PII in artifacts | ☐ | Phase 4 eval |
| Public exports only (no scrape) | ☐ | Phase 1 eval + runbook |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | Single agent prompt | “Run weekly pulse for Groww” completes pipeline with minimal extra instruction |
| M2 | Doc + Draft | Both artifacts reachable in browser/Gmail |
| M3 | Leadership read-through | Non-engineer can understand note in <2 min |
| M4 | Second weekly run | New note date; Doc update policy respected; new draft |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** Full E2E run completed once with evidence (links/ids in `publish_state.json`)
- [ ] **E2** All [problem statement](../../problemStatement.md#deliverables-checklist) items checked
- [ ] **E3** E2E time ≤30 min (excluding export download)
- [ ] **E4** Second run proves Doc idempotency + new draft
- [ ] **E5** Runbook documents order: ingest → themes → note → PII → MCP Doc → MCP Gmail
- [ ] **E6** Phases 0–6 eval files signed off
- [ ] **E7** GitHub Actions `refresh-data` job runs on `workflow_dispatch` and uploads artifacts
- [ ] **E8** `publish` job optional on dispatch with `run_publish: true` (secrets set)

**Phase 7 / Milestone complete when:** E1–E6 checked and deliverables matrix fully ticked.

---

## Optional enhancements (not required for pass)

- [ ] Week-over-week trend arrows in note
- [ ] Auto-commit bot PR from `refresh-data` artifacts
- [ ] Cron publish (default: publish is manual dispatch only)

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| E2E breaks at MCP | Phase 0 regression | Re-auth MCP; re-run Phase 0 eval |
| Inconsistent Doc vs email | Separate manual edits | Single `note.md` source for both MCP calls |
| Slow runs | Large export | Batch theme labeling; cache normalized JSONL |

**Evaluator:** _______________ **Date:** _______________

**Milestone 3 status:** ☐ PASS ☐ FAIL — Notes: _______________
