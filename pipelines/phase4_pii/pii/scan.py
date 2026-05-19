from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .patterns import (
    AT_HANDLE,
    EMAIL,
    PHONE,
    REVIEW_ID_LITERAL,
    STORE_REVIEW_PREFIX,
    long_numeric_pattern,
)


@dataclass
class ScanFinding:
    pii_type: str
    match: str
    line: int
    context: str

    def to_dict(self) -> dict[str, str | int]:
        return {
            "pii_type": self.pii_type,
            "match": self.match,
            "line": self.line,
            "context": self.context,
        }


def _line_context(lines: list[str], line_idx: int, match: str) -> str:
    text = lines[line_idx].strip()
    if len(text) <= 120:
        return text
    pos = text.find(match)
    if pos < 0:
        return text[:120] + "..."
    start = max(0, pos - 40)
    end = min(len(text), pos + len(match) + 40)
    snippet = text[start:end]
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def _add_findings(
    findings: list[ScanFinding],
    lines: list[str],
    pii_type: str,
    pattern: re.Pattern[str],
) -> None:
    for i, line in enumerate(lines):
        for m in pattern.finditer(line):
            matched = m.group(0)
            findings.append(
                ScanFinding(
                    pii_type=pii_type,
                    match=matched,
                    line=i + 1,
                    context=_line_context(lines, i, matched),
                )
            )


def _phone_is_likely_date_or_percent(line: str, matched: str) -> bool:
    """Reduce false positives on dates embedded in long digit runs."""
    digits_only = re.sub(r"\D", "", matched)
    if len(digits_only) < 10:
        return True
    if "%" in line and matched in line:
        return True
    return False


def _load_name_blocklist(path: Path | None) -> list[str]:
    if not path or not path.is_file():
        return []
    names: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        name = line.strip()
        if name and not name.startswith("#"):
            names.append(name)
    return names


def scan_text(
    text: str,
    *,
    min_numeric_id_length: int = 10,
    name_blocklist_path: Path | None = None,
) -> list[ScanFinding]:
    lines = text.splitlines()
    findings: list[ScanFinding] = []

    _add_findings(findings, lines, "email", EMAIL)
    _add_findings(findings, lines, "review_id", REVIEW_ID_LITERAL)
    _add_findings(findings, lines, "store_review_id", STORE_REVIEW_PREFIX)

    numeric_pat = long_numeric_pattern(min_numeric_id_length)
    for i, line in enumerate(lines):
        for m in numeric_pat.finditer(line):
            matched = m.group(0)
            findings.append(
                ScanFinding(
                    pii_type="long_numeric_id",
                    match=matched,
                    line=i + 1,
                    context=_line_context(lines, i, matched),
                )
            )

    for i, line in enumerate(lines):
        for m in PHONE.finditer(line):
            matched = m.group(0)
            if _phone_is_likely_date_or_percent(line, matched):
                continue
            if EMAIL.search(matched):
                continue
            findings.append(
                ScanFinding(
                    pii_type="phone",
                    match=matched,
                    line=i + 1,
                    context=_line_context(lines, i, matched),
                )
            )

    for i, line in enumerate(lines):
        if EMAIL.search(line):
            continue
        for m in AT_HANDLE.finditer(line):
            matched = m.group(0)
            findings.append(
                ScanFinding(
                    pii_type="at_handle",
                    match=matched,
                    line=i + 1,
                    context=_line_context(lines, i, matched),
                )
            )

    for name in _load_name_blocklist(name_blocklist_path):
        if len(name) < 3:
            continue
        pat = re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE)
        for i, line in enumerate(lines):
            for m in pat.finditer(line):
                findings.append(
                    ScanFinding(
                        pii_type="blocklist_name",
                        match=m.group(0),
                        line=i + 1,
                        context=_line_context(lines, i, m.group(0)),
                    )
                )

    return _dedupe_findings(findings)


def _dedupe_findings(findings: list[ScanFinding]) -> list[ScanFinding]:
    seen: set[tuple[str, str, int]] = set()
    out: list[ScanFinding] = []
    for f in findings:
        key = (f.pii_type, f.match, f.line)
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def scan_file(
    path: Path,
    *,
    min_numeric_id_length: int = 10,
    name_blocklist_path: Path | None = None,
) -> list[ScanFinding]:
    text = path.read_text(encoding="utf-8")
    return scan_text(
        text,
        min_numeric_id_length=min_numeric_id_length,
        name_blocklist_path=name_blocklist_path,
    )
