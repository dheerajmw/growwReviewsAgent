# Phase 7 — E2E workflow + GitHub Actions scheduler

**Plan:** [Phase 7](../../doc/phasewiseImplementationPlan.md#phase-7--end-to-end-workflow-github-actions-scheduler-and-hardening) · **Runbook:** [doc/runbook.md](../../doc/runbook.md)

## Local orchestration

```bash
python scripts/run_weekly_pulse.py -v
python scripts/run_weekly_pulse.py -v --publish --force
```

## CI scheduler

[`.github/workflows/weekly_pulse.yml`](../../.github/workflows/weekly_pulse.yml)

- **validate** — every push/PR (no Groq)
- **refresh-data** — weekly cron + manual dispatch
- **publish** — manual dispatch with `run_publish: true`

**Depends on:** Phases [0–6](../phase0_mcp/README.md)
