# Phase 2 Evaluation — Theme Clustering (≤5 Themes)

**Plan:** [Phase 2](../../phasewiseImplementationPlan.md#phase-2--theme-clustering-max-5-themes) · **Depends on:** [Phase 1](../phase-01/eval.md) complete

---

## Prerequisites

- `data/reviews/normalized.jsonl` from Phase 1
- `prompts/themes.md` authored
- Clustering script or documented agent workflow producing `data/themes/clusters.json` and `data/themes/ranked.json`

---

## Automated checks

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | Artifacts exist | `test -f data/themes/clusters.json && test -f data/themes/ranked.json` | Both files present |
| A2 | Theme count cap | `python3 scripts/validate_themes.py` or `python3 -c "import json; t=json.load(open('data/themes/clusters.json'))['themes']; assert len(t)<=5"` | `len(themes) <= 5` |
| A3 | Theme schema | Validator | Each theme has `id`, `label`, `review_ids` (array) |
| A4 | Coverage | Validator | Union of `review_ids` covers all normalized ids (or ≥95% with documented orphans) |
| A5 | No duplicate assignment | Validator | No `review_id` in more than one theme |
| A6 | Ranked top 3 | `python3 -c "import json; r=json.load(open('data/themes/ranked.json')); assert len(r)>=3"` | At least 3 ranked entries |
| A7 | Labels from vocabulary | Manual script check | Labels align with locked set (onboarding, KYC, payments, statements, withdrawals) unless change documented |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | Read `ranked.json` top 3 | Sensible for Groww (e.g. KYC/payments common in fintech) |
| M2 | Sample 10 reviews per top theme | Text broadly matches theme label |
| M3 | Orphan / “other” bucket | None, or merged; count noted in README |
| M4 | Re-run clustering on same input | Same theme count; ranks may shift slightly if LLM — document non-determinism |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** `clusters.json` and `ranked.json` generated
- [ ] **E2** At most **5** themes
- [ ] **E3** Every in-scope review assigned exactly one theme
- [ ] **E4** Top 3 themes identifiable from `ranked.json` for Phase 3
- [ ] **E5** Theme vocabulary documented in `prompts/themes.md`

**Phase 2 complete when:** E1–E5 checked and A1–A6 pass.

---

## Quality rubric (manual, 1–5 each)

| Criterion | 5 = Excellent |
|-----------|----------------|
| Theme coherence | Reviews in a theme clearly share a problem area |
| Distinctness | Minimal overlap between theme labels |
| Actionability | Labels map to product areas (not vague “bugs”) |

**Minimum to pass manual rubric:** Average ≥3 across three criteria.

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| 6+ themes in JSON | Missing post-process cap | Merge smallest themes or re-prompt with hard limit |
| Empty `review_ids` | LLM JSON parse error | Add validation + retry with smaller batches |
| One giant “other” theme | Weak prompt | Refine enum; batch by rating |

**Evaluator:** _______________ **Date:** _______________
