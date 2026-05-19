"""
PII detection patterns for Phase 4 (documented per eval phase-04).

| Type            | Pattern summary                          |
|-----------------|------------------------------------------|
| email           | RFC5322-lite local@domain                |
| phone           | E.164-ish, US, spaced Indian (+91)       |
| at_handle       | @word (not part of email)                |
| long_numeric_id | >= min_digits consecutive digits         |
| review_id       | literal review_id or store:id prefixes   |
| blocklist_name  | optional names from export column        |
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Email (avoid matching "user@domain" inside longer tokens)
EMAIL = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    re.IGNORECASE,
)

# Phones: +91 98765 43210, +1-555-123-4567, (555) 123-4567, 10-digit US
PHONE = re.compile(
    r"(?:"
    r"\+?\d{1,3}[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}(?:[\s.-]?\d{2,4})?"
    r"|\(\d{3}\)\s*\d{3}[\s.-]?\d{4}"
    r"|\b\d{10}\b"
    r")",
)

# @handle — require letter after @ (skip lone @)
AT_HANDLE = re.compile(r"(?<![\w.@])[@]([A-Za-z][\w]{1,})\b")

# Store / internal review identifiers
REVIEW_ID_LITERAL = re.compile(r"\breview_id\b", re.IGNORECASE)
STORE_REVIEW_PREFIX = re.compile(
    r"\b(?:app_store|play_store):[\w-]+\b",
    re.IGNORECASE,
)


def long_numeric_pattern(min_digits: int) -> re.Pattern[str]:
    return re.compile(rf"\b\d{{{min_digits},}}\b")


@dataclass(frozen=True)
class PatternSpec:
    pii_type: str
    pattern: re.Pattern[str]
    description: str
