# Phase 8 Evaluation — Web Dashboard (Frontend)

**Plan:** [Phase 8](../../phasewiseImplementationPlan.md#phase-8--web-dashboard-proper-frontend) · **Depends on:** [Phase 7](../phase-07/eval.md) (artifacts available)

---

## Prerequisites

- `frontend/` scaffold (Vite + React + TypeScript + Tailwind)
- `pipelines/phase8_frontend/api/` serving read-only endpoints
- Latest `data/weekly/note.json` and `data/themes/ranked.json` from pipeline

---

## Automated checks

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | Frontend builds | `cd frontend && npm run build` | Exit 0 |
| A2 | No Google SDK in UI | `rg -i "googleapis|gapi" frontend/` | Zero matches |
| A3 | API health | `curl localhost:8080/api/v1/health` | `status: ok` |
| A4 | Pulse API | `curl localhost:8080/api/v1/pulse/latest` | Valid JSON with `themes`, `quotes`, `actions` |
| A5 | Lint (optional) | `cd frontend && npm run lint` | No errors |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | Open Dashboard `/` | Week ending, top 3 themes, PII chip visible |
| M2 | Pulse page | Renders note content; word count ≤250 indicated |
| M3 | Themes page | Chart/list matches `ranked.json` |
| M4 | Pipeline page | Phase stepper reflects artifact state |
| M5 | Publish links | Doc + Gmail open in new tab (external) |
| M6 | Mobile 375px | Layout usable; nav accessible |
| M7 | No PII in UI | No emails, handles, or review_ids shown |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** All five routes render without errors
- [ ] **E2** Content matches latest pipeline artifacts
- [ ] **E3** No `googleapis` in frontend or Phase 8 API
- [ ] **E4** Responsive at mobile and desktop widths
- [ ] **E5** README documents `npm run dev` + API start

**Phase 8 complete when:** E1–E5 and A1–A4 pass.

**Evaluator:** _______________ **Date:** _______________
