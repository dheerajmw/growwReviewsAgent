from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PYTHON = sys.executable


@dataclass
class WeeklyPulseOptions:
    skip_download: bool = False
    skip_publish: bool = False
    publish_only: bool = False
    publish_doc: bool = False
    publish_draft: bool = False
    force_publish: bool = False
    phase2_dry_run: bool = False
    verbose: bool = False
    stop_after: str | None = None  # e.g. "ingest", "themes", "note", "pii"


def _run(cmd: list[str], *, step: str, verbose: bool) -> None:
    logging.info("=== %s ===", step)
    logging.info("Command: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Step failed ({step}): exit {result.returncode}")


def _should_stop(stop_after: str | None, completed: str) -> bool:
    order = ["download", "ingest", "validate_reviews", "themes", "note", "validate_note", "pii", "publish_doc", "publish_draft"]
    if not stop_after:
        return False
    if stop_after not in order:
        raise ValueError(f"Unknown --stop-after value: {stop_after!r}; choose from {order}")
    return order.index(completed) >= order.index(stop_after)


def run_weekly_pulse(opts: WeeklyPulseOptions) -> int:
    v = ["-v"] if opts.verbose else []
    extra_pub = ["--force"] if opts.force_publish else []

    data_steps: list[tuple[str, list[str]]] = [
        ("download", [PYTHON, "scripts/download_reviews.py", *v]),
        ("ingest", [PYTHON, "scripts/ingest_reviews.py", *v]),
        ("validate_reviews", [PYTHON, "scripts/validate_reviews.py"]),
        (
            "themes",
            [PYTHON, "pipelines/phase2_themes/run.py", *v]
            + (["--dry-run"] if opts.phase2_dry_run else []),
        ),
        ("note", [PYTHON, "pipelines/phase3_note/run.py", *v]),
        ("validate_note", [PYTHON, "scripts/validate_note.py"]),
        ("pii", [PYTHON, "scripts/check_pii.py", "data/weekly/note.md"]),
    ]

    publish_steps: list[tuple[str, list[str]]] = [
        ("publish_doc", [PYTHON, "scripts/publish_doc.py", *v, *extra_pub]),
        ("publish_draft", [PYTHON, "scripts/publish_draft.py", *v, *extra_pub]),
    ]

    if opts.publish_only:
        if opts.skip_publish:
            raise ValueError("--publish-only conflicts with --skip-publish")
        if not opts.publish_doc and not opts.publish_draft:
            opts.publish_doc = True
            opts.publish_draft = True
        steps = [("pii", [PYTHON, "scripts/check_pii.py", "data/weekly/note.md"])]
        if opts.publish_doc:
            steps.append(publish_steps[0])
        if opts.publish_draft:
            steps.append(publish_steps[1])
    else:
        steps = []
        if not opts.skip_download:
            steps.extend(data_steps)
        else:
            steps.extend(data_steps[1:])  # skip download
        if not opts.skip_publish:
            if opts.publish_doc or opts.publish_draft:
                if opts.publish_doc:
                    steps.append(publish_steps[0])
                if opts.publish_draft:
                    steps.append(publish_steps[1])
            # default: do not publish unless flags set

    for step_name, cmd in steps:
        _run(cmd, step=step_name, verbose=opts.verbose)
        if _should_stop(opts.stop_after, step_name):
            logging.info("Stopped after %s (--stop-after)", step_name)
            break

    logging.info("Weekly pulse completed successfully.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Phase 7: run weekly Groww review pulse (phases 1–6)",
    )
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--skip-publish", action="store_true", help="Do not publish Doc/draft")
    parser.add_argument("--publish-only", action="store_true", help="Only publish Doc + draft (after PII)")
    parser.add_argument("--publish-doc", action="store_true", help="Include Phase 5 Doc publish")
    parser.add_argument("--publish-draft", action="store_true", help="Include Phase 6 Gmail draft")
    parser.add_argument("--publish", action="store_true", help="Shorthand: --publish-doc --publish-draft")
    parser.add_argument("--force", action="store_true", help="Force Doc/draft publish same week")
    parser.add_argument("--phase2-dry-run", action="store_true", help="Heuristic themes only (no Groq)")
    parser.add_argument(
        "--stop-after",
        choices=["download", "ingest", "validate_reviews", "themes", "note", "validate_note", "pii", "publish_doc", "publish_draft"],
        default=None,
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    publish_doc = args.publish_doc or args.publish
    publish_draft = args.publish_draft or args.publish

    opts = WeeklyPulseOptions(
        skip_download=args.skip_download,
        skip_publish=args.skip_publish,
        publish_only=args.publish_only,
        publish_doc=publish_doc,
        publish_draft=publish_draft,
        force_publish=args.force,
        phase2_dry_run=args.phase2_dry_run,
        verbose=args.verbose,
        stop_after=args.stop_after,
    )

    try:
        return run_weekly_pulse(opts)
    except Exception as exc:
        logging.error("%s", exc)
        return 1
