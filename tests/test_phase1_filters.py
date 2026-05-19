#!/usr/bin/env python3
"""Tests for Phase 1 content filters."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pipelines.phase1_ingest.ingest.filters import (
    combined_review_text,
    content_filter_reason,
    contains_emoji,
    is_english,
    word_count,
)


class Phase1FilterTests(unittest.TestCase):
    def test_word_count(self) -> None:
        self.assertEqual(word_count("one two three four five six"), 6)
        self.assertEqual(word_count("one two three four five"), 5)

    def test_emoji_rejected(self) -> None:
        self.assertTrue(contains_emoji("Great app 😀"))
        reason = content_filter_reason(
            {"title": "", "text": "Love it 😀 thanks"},
            min_words=1,
            english_only=False,
            reject_emoji=True,
        )
        self.assertEqual(reason, "contains_emoji")

    def test_too_few_words(self) -> None:
        reason = content_filter_reason(
            {"title": "Good", "text": "Nice app"},
            min_words=6,
            english_only=False,
            reject_emoji=False,
        )
        self.assertEqual(reason, "too_few_words")

    def test_english_passes(self) -> None:
        text = (
            "The onboarding flow was smooth and KYC completed within one day. "
            "Payments and withdrawals work reliably for mutual fund SIP."
        )
        self.assertTrue(is_english(text))
        reason = content_filter_reason(
            {"title": "Works well", "text": text},
            min_words=6,
            english_only=True,
            reject_emoji=True,
        )
        self.assertIsNone(reason)

    def test_non_english_rejected(self) -> None:
        hindi = (
            "यह ऐप बहुत अच्छा है मुझे म्यूचुअल फंड में निवेश करना बहुत पसंद है "
            "और सभी सुविधाएं आसानी से उपलब्ध हैं कृपया इसे जरूर आजमाएं धन्यवाद बहुत बढ़िया"
        )
        self.assertFalse(is_english(hindi))
        reason = content_filter_reason(
            {"title": "", "text": hindi},
            min_words=6,
            english_only=True,
            reject_emoji=False,
        )
        self.assertEqual(reason, "non_english")

    def test_combined_title_body(self) -> None:
        rec = {"title": "one two three", "text": "four five six seven"}
        self.assertEqual(word_count(combined_review_text(rec)), 7)


if __name__ == "__main__":
    unittest.main()
