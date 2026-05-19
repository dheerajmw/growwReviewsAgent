# Phase 4 — PII sanitization gate

**Plan:** [Phase 4](../../doc/phasewiseImplementationPlan.md#phase-4--pii-sanitization-gate) · **Eval:** [phase-04 eval](../../doc/eval/phase-04/eval.md)

Hard gate before Google Docs/Gmail (Phases 5–6). Scans `note.md` for emails, phones, `@handles`, long numeric IDs, and review identifiers.

## Run

```bash
python scripts/check_pii.py data/weekly/note.md
# or
python pipelines/phase4_pii/run.py
```

On **failure:** writes `data/weekly/blockers.json` with `publish_blocked: true` and exits `1`.

On **success:** removes `blockers.json` if present.

## Optional redaction (Groq)

```bash
python pipelines/phase4_pii/run.py --redact -v
```

Requires `GROQ_API_KEY` in `.env`. Rewrites `data/weekly/note.md` then re-runs the gate.

## Patterns

Documented in `pipelines/phase4_pii/pii/patterns.py` module header.

**Depends on:** [Phase 3](../phase3_note/README.md) → `data/weekly/note.md`
