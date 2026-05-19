# Phase Evaluation Index

Each implementation phase has an **`eval.md`** with automated checks, manual steps, exit criteria, and sign-off.

**Usage:** Complete phases in order per [phasewiseImplementationPlan.md](../phasewiseImplementationPlan.md). Do not start phase *N+1* until phase *N* eval is signed off. Major scope or integration choices belong in [decision.md](../decision.md).

| Phase | Name | Evaluation |
|-------|------|------------|
| 0 | MCP & scaffold | [phase-00/eval.md](./phase-00/eval.md) |
| 1 | Review ingest | [phase-01/eval.md](./phase-01/eval.md) |
| 2 | Theme clustering | [phase-02/eval.md](./phase-02/eval.md) |
| 3 | Weekly note | [phase-03/eval.md](./phase-03/eval.md) |
| 4 | PII gate | [phase-04/eval.md](./phase-04/eval.md) |
| 5 | Google Docs (MCP) | [phase-05/eval.md](./phase-05/eval.md) |
| 6 | Gmail draft (MCP) | [phase-06/eval.md](./phase-06/eval.md) |
| 7 | E2E + GHA scheduler | [phase-07/eval.md](./phase-07/eval.md) |
| 8 | Web dashboard | [phase-08/eval.md](./phase-08/eval.md) |

## Quick validation bundle

```bash
python3 scripts/run_weekly_pulse.py -v --skip-download --stop-after pii
python3 scripts/run_weekly_pulse.py -v --publish-only   # after note exists
```

See [doc/runbook.md](../runbook.md) and [.github/workflows/weekly_pulse.yml](../../.github/workflows/weekly_pulse.yml).

Phases 5–6 require MCP tools in Cursor (see phase-05 and phase-06 evals).
