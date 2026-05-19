from __future__ import annotations

from unittest.mock import patch

from pipelines.phase7_e2e.e2e.run_weekly import WeeklyPulseOptions, run_weekly_pulse


def test_stop_after_ingest_skips_themes():
    calls: list[str] = []

    def fake_run(cmd, *, step, verbose):
        calls.append(step)

    opts = WeeklyPulseOptions(skip_download=True, stop_after="ingest", verbose=False)

    with patch("pipelines.phase7_e2e.e2e.run_weekly._run", side_effect=fake_run):
        run_weekly_pulse(opts)

    assert calls == ["ingest"]


def test_publish_only_includes_pii_and_publish():
    calls: list[str] = []

    def fake_run(cmd, *, step, verbose):
        calls.append(step)

    opts = WeeklyPulseOptions(publish_only=True, publish_doc=True, publish_draft=False)

    with patch("pipelines.phase7_e2e.e2e.run_weekly._run", side_effect=fake_run):
        run_weekly_pulse(opts)

    assert calls == ["pii", "publish_doc"]
