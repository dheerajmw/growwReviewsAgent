#!/usr/bin/env python3
"""Phase 4 CLI — PII gate on weekly note."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pipelines.phase4_pii.pii.config import Phase4Config
from pipelines.phase4_pii.pii.gate import run_pii_gate, run_pii_gate_on_text
from pipelines.phase4_pii.pii.redact import redact_and_validate
from pipelines.phase4_pii.pii.scan import scan_text


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 4: PII sanitization gate")
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Path to note.md (default: data/weekly/note.md from config)",
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument(
        "--no-blockers",
        action="store_true",
        help="Do not write or clear data/weekly/blockers.json",
    )
    parser.add_argument(
        "--redact",
        action="store_true",
        help="Run Groq redaction on failure, then re-check",
    )
    parser.add_argument("--json", action="store_true", dest="json_out")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s %(message)s",
    )

    config = Phase4Config.load(args.config)
    write_blockers = not args.no_blockers
    target = args.path or str(config.note_md_path)

    if target == "-":
        text = sys.stdin.read()
        result = run_pii_gate_on_text(
            text,
            config,
            source_label="<stdin>",
            write_blockers_file=write_blockers,
        )
    else:
        path = Path(target)
        if not path.is_file():
            logging.error("File not found: %s", path)
            return 1
        result = run_pii_gate(path, config, write_blockers_file=write_blockers)

    if args.json_out:
        print(
            json.dumps(
                {
                    "passed": result.passed,
                    "source": result.source,
                    "findings": [f.to_dict() for f in result.findings],
                },
                indent=2,
            )
        )

    if result.passed:
        logging.info("PII gate passed (%s)", result.source)
        return 0

    for f in result.findings:
        logging.error("PII %s line %s: %r — %s", f.pii_type, f.line, f.match, f.context)

    if args.redact and target != "-":
        logging.info("Running Groq redaction on %s", config.note_md_path)
        if redact_and_validate(config):
            logging.info("PII gate passed after redaction")
            return 0
        result = run_pii_gate(config.note_md_path, config, write_blockers_file=write_blockers)
        for f in result.findings:
            logging.error("PII %s line %s: %r", f.pii_type, f.line, f.match)

    logging.error("PII gate FAILED — publish blocked (see %s)", config.blockers_path)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
