from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .config import Phase4Config
from .scan import ScanFinding, scan_file, scan_text


@dataclass
class GateResult:
    passed: bool
    findings: list[ScanFinding]
    source: str

    @property
    def blocked(self) -> bool:
        return not self.passed


def write_blockers(
    path: Path,
    *,
    source: str,
    findings: list[ScanFinding],
    passed: bool,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": source,
        "passed": passed,
        "publish_blocked": not passed,
        "findings": [f.to_dict() for f in findings],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def clear_blockers(path: Path) -> None:
    if path.is_file():
        path.unlink()


def run_pii_gate(
    source: Path | str,
    config: Phase4Config | None = None,
    *,
    write_blockers_file: bool = True,
) -> GateResult:
    cfg = config or Phase4Config.load()
    src = Path(source) if isinstance(source, str) else source
    src_label = str(src) if src != Path("-") else "<stdin>"

    if src == Path("-") or str(source) == "-":
        raise ValueError("use scan_text for stdin; gate expects a file path")

    findings = scan_file(
        src,
        min_numeric_id_length=cfg.min_numeric_id_length,
        name_blocklist_path=cfg.name_blocklist_path,
    )
    passed = len(findings) == 0

    if write_blockers_file:
        if passed:
            clear_blockers(cfg.blockers_path)
        else:
            write_blockers(
                cfg.blockers_path,
                source=src_label,
                findings=findings,
                passed=False,
            )

    return GateResult(passed=passed, findings=findings, source=src_label)


def run_pii_gate_on_text(
    text: str,
    config: Phase4Config | None = None,
    *,
    source_label: str = "<text>",
    write_blockers_file: bool = True,
) -> GateResult:
    cfg = config or Phase4Config.load()
    findings = scan_text(
        text,
        min_numeric_id_length=cfg.min_numeric_id_length,
        name_blocklist_path=cfg.name_blocklist_path,
    )
    passed = len(findings) == 0

    if write_blockers_file:
        if passed:
            clear_blockers(cfg.blockers_path)
        else:
            write_blockers(
                cfg.blockers_path,
                source=source_label,
                findings=findings,
                passed=False,
            )

    return GateResult(passed=passed, findings=findings, source=source_label)
