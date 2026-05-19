from __future__ import annotations

import re
from typing import Any

# Broad emoji / pictograph ranges (no extra dependency)
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002700-\U000027BF"
    "\U0001F600-\U0001F64F"
    "\U00002600-\U000026FF"
    "\U00002300-\U000023FF"
    "\U0000FE00-\U0000FE0F"
    "\U0001F1E0-\U0001F1FF"
    "]+",
    flags=re.UNICODE,
)

# Mostly-ASCII emoticons often used instead of unicode emoji
_ASCII_EMOTICON_RE = re.compile(
    r"(?:^|[\s.,!?])(?:"
    r":-?\)|:-?\(|:-?D|:-?P|:-?/|:-?\\|"
    r";-?\)|<3|xD|XD"
    r")(?:$|[\s.,!?])",
    flags=re.IGNORECASE,
)

_WORD_RE = re.compile(r"[a-zA-Z]+(?:'[a-zA-Z]+)?")


def combined_review_text(record: dict[str, Any]) -> str:
    title = str(record.get("title") or "").strip()
    body = str(record.get("text") or "").strip()
    if title and body:
        return f"{title}. {body}"
    return title or body


def word_count(text: str) -> int:
    return len(_WORD_RE.findall(text))


def contains_emoji(text: str) -> bool:
    if _EMOJI_RE.search(text):
        return True
    return bool(_ASCII_EMOTICON_RE.search(text))


def is_english(text: str, min_chars: int = 15) -> bool:
    """
    Detect English using langdetect on review text.
    Short strings skip detection only if entirely ASCII letters/spaces.
    """
    cleaned = text.strip()
    if not cleaned:
        return False

    if len(cleaned) < min_chars and cleaned.isascii():
        # Very short ASCII reviews (e.g. "Good app works fine")
        return True

    try:
        from langdetect import LangDetectException, detect

        lang = detect(cleaned)
        return lang == "en"
    except Exception:
        # langdetect missing or failed — fall back to ASCII heuristic
        letters = sum(1 for c in cleaned if c.isalpha())
        if letters == 0:
            return False
        ascii_letters = sum(1 for c in cleaned if c.isascii() and c.isalpha())
        return ascii_letters / letters >= 0.95


def content_filter_reason(
    record: dict[str, Any],
    *,
    min_words: int = 6,
    english_only: bool = True,
    reject_emoji: bool = True,
) -> str | None:
    """
    Return a skip reason if the record should be dropped, else None.
    """
    text = combined_review_text(record)

    if reject_emoji and contains_emoji(text):
        return "contains_emoji"

    if english_only and not is_english(text):
        return "non_english"

    if word_count(text) < min_words:
        return "too_few_words"

    return None
