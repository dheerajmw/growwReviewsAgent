# Phase 4 Evaluation — PII Sanitization Gate

**Plan:** [Phase 4](../../phasewiseImplementationPlan.md#phase-4--pii-sanitization-gate) · **Depends on:** [Phase 3](../phase-03/eval.md) complete

---

## Prerequisites

- `data/weekly/note.md` from Phase 3
- `scripts/check_pii.py` implemented with documented patterns
- Agent/workflow blocks MCP publish on failure

---

## Automated checks

| # | Check | Command | Pass condition |
|---|--------|---------|----------------|
| A1 | PII scan clean | `python3 scripts/check_pii.py data/weekly/note.md` | Exit code `0` |
| A2 | Negative test — email | `echo 'Contact user@example.com' \| python3 scripts/check_pii.py -` | Exit code non-zero |
| A3 | Negative test — phone | Sample string with phone pattern | Detected |
| A4 | Negative test — @handle | `@groww_user_123` | Detected |
| A5 | No `review_id` in note | `rg "review_id" data/weekly/note.md` | No matches |
| A6 | Blockers file on failure | Deliberately dirty note → run gate | `data/weekly/blockers.json` written; publish aborted |

---

## Manual verification

| # | Step | Expected result |
|---|------|-----------------|
| M1 | Read all 3 quotes in `note.md` | No usernames, emails, phone numbers, order/ account IDs |
| M2 | Read action ideas and theme lines | No PII |
| M3 | Review `check_pii.py` pattern list | Covers: email, phone, @handle, long numeric IDs (≥10 digits) |
| M4 | Redaction path | If A1 failed once, redaction re-run passes A1 |

---

## Exit criteria (sign-off checklist)

- [ ] **E1** `check_pii.py` passes on final `note.md`
- [ ] **E2** PII patterns documented in script header or `doc/`
- [ ] **E3** Manual review of 3 quotes: no identifiable users
- [ ] **E4** Publish blocked when PII check fails (`blockers.json` + no MCP calls)
- [ ] **E5** Aligns with [problem statement — no PII](../../problemStatement.md#key-constraints)

**Phase 4 complete when:** E1–E5 checked and A1–A6 pass.

---

## PII test corpus (use in CI or local)

Create `tests/fixtures/pii_samples.txt` with lines that **must fail** scan:

```
user@domain.com
+91 98765 43210
@ReviewerName
Account ID: 1234567890123
```

Create `tests/fixtures/clean_note_snippet.txt` that **must pass**.

---

## Failure modes

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| False negative on names | Names only in free text | Add optional reviewer name column blocklist from export |
| False positive on “KYC” | Over-aggressive regex | Tune patterns; allowlist product terms |
| Publish despite failure | Missing gate in agent flow | Enforce: Phase 4 before any Phase 5 MCP call |

**Phase 4 is a hard gate for Phases 5–6.**

**Evaluator:** _______________ **Date:** _______________
