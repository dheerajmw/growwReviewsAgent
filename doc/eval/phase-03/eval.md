# Phase 3 Evaluation — Weekly Note Generation (≤250 Words)

**Plan:** [Phase 3](../../phasewiseImplementationPlan.md#phase-3--weekly-note-generation-250-words) · **Depends on:** [Phase 2](../phase-02/eval.md) complete

---

## Prerequisites

- `data/themes/ranked.json` from Phase 2
- `prompts/system.md`, `prompts/weekly_note.md`
- `scripts/validate_note.py` (or equivalent)
- `data/weekly/note.md` and `data/weekly/note.json`

---

## Automated checks

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | Artifacts exist | `test -f data/weekly/note.md && test -f data/weekly/note.json` | Both present |
| A2 | Word count | `python3 scripts/validate_note.py` | Body ≤ **250** words |
| A3 | Required sections | Validator | Sections present: Top 3 themes, 3 quotes, 3 action ideas |
| A4 | JSON structure | `python3 -c "import json; n=json.load(open('data/weekly/note.json')); assert all(k in n for k in ['themes','quotes','actions'])"` | Keys: `themes` (len 3), `quotes` (len 3), `actions` (len 3) |
| A5 | Top themes match rank | Script or manual diff | `note.json` themes ⊆ top 3 from `ranked.json` |
| A6 | No investment advice | `rg -i "should invest|buy this|sell|recommend" data/weekly/note.md` | No advisory language |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | Read `note.md` end-to-end | Scannable in <2 minutes; executive tone |
| M2 | Three quotes | Paraphrased; no `@user`, emails, or full names |
| M3 | Three actions | Specific to product/support (fix flow, clarify copy), not stock tips |
| M4 | Groww context | Title or intro references weekly mobile review pulse for Groww |
| M5 | Compare to problem statement | Matches [deliverables](../../problemStatement.md#what-you-must-build) |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** `note.md` passes `validate_note.py`
- [ ] **E2** Word count ≤250
- [ ] **E3** Exactly 3 themes, 3 quotes, 3 action ideas
- [ ] **E4** `note.json` mirrors `note.md` for MCP publish
- [ ] **E5** Quotes paraphrased (not raw export copy-paste)

**Phase 3 complete when:** E1–E5 checked and A1–A6 pass.

---

## Content checklist (quick)

| Item | Present? |
|------|----------|
| Document title with date | ☐ |
| Top 3 themes (one line each) | ☐ |
| 3 user quotes (anonymized) | ☐ |
| 3 action ideas | ☐ |
| No PII in draft note (Phase 4 will gate formally) | ☐ |

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| >250 words | Verbose LLM output | Tighten prompt; add truncate step with validator retry |
| Missing section | JSON/markdown drift | Single source: generate JSON then render `note.md` |
| Raw quotes with names | Copy from export | Enforce paraphrase in `weekly_note.md` prompt |

**Evaluator:** _______________ **Date:** _______________
