#!/usr/bin/env python3
"""Generate sample App Store / Play Store CSV fixtures for Phase 1 dev & eval."""

from __future__ import annotations

import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RAW = REPO / "data" / "raw"

SAMPLES = [
    (5, "Smooth SIP setup", "Setting up monthly SIP was quick and the UI is clean.", "2026-05-10"),
    (4, "Good overall", "App works well for tracking mutual funds and stocks.", "2026-05-08"),
    (2, "KYC stuck", "KYC verification pending for days with no clear status update.", "2026-05-05"),
    (1, "Cannot complete KYC", "Upload keeps failing at PAN step. Very frustrating.", "2026-05-01"),
    (3, "Payment failed", "UPI payment for lump sum failed twice before it went through.", "2026-04-28"),
    (2, "Withdrawal delay", "Withdrawal to bank shows processing for over 48 hours.", "2026-04-25"),
    (4, "Statement download", "Finally found tax statement download under reports section.", "2026-04-20"),
    (3, "Statement missing", "Capital gains statement for last FY not visible yet.", "2026-04-15"),
    (5, "Easy onboarding", "Onboarding flow was simple and well guided for a new user.", "2026-04-10"),
    (2, "Confusing onboarding", "Too many steps during signup. Lost progress once.", "2026-04-05"),
    (4, "Fast UPI", "UPI payments for stocks are fast and reliable.", "2026-04-01"),
    (1, "App crashes", "App crashes when opening portfolio after latest update.", "2026-03-28"),
    (3, "KYC document", "Need clearer instructions on acceptable address proof.", "2026-03-25"),
    (5, "Great for beginners", "Helpful for someone new to mutual funds.", "2026-03-20"),
    (2, "Bank link issue", "Bank account linking failed with generic error.", "2026-03-15"),
    (4, "Notifications", "Price alerts work well. Would like more customization.", "2026-03-10"),
    (3, "Slow support", "In-app support chat took long to respond on withdrawal query.", "2026-03-05"),
    (5, "Reliable tracker", "Use it daily to track NAV and holdings.", "2026-03-01"),
    (2, "KYC retry", "Had to retry KYC video verification multiple times.", "2026-05-12"),
    (4, "Payments ok", "Autopay for SIP works without issues now.", "2026-05-14"),
    (3, "Withdrawal ok", "Withdrawal completed but status UI was unclear.", "2026-05-11"),
    (1, "Login loop", "Keeps asking to login again after fingerprint unlock.", "2026-05-09"),
    (4, "Reports", "Monthly statement PDF downloaded without hassle.", "2026-05-07"),
    (2, "Payment pending", "Payment stuck on pending screen for 30 minutes.", "2026-05-04"),
    (5, "Clean design", "Love the minimal design and dark mode.", "2026-05-02"),
    (3, "Onboarding OTP", "OTP delayed during onboarding on weekend.", "2026-04-30"),
    (4, "KYC fast", "KYC approved within a day. Smooth experience.", "2026-04-27"),
    (2, "Statement format", "Statement CSV format hard to import into sheets.", "2026-04-22"),
    (5, "SIP reminder", "SIP reminders are timely and accurate.", "2026-04-18"),
    (3, "Withdrawal limit", "Wish withdrawal limits were explained upfront.", "2026-04-12"),
    # Out of window (should be dropped)
    (5, "Old review", "This review is outside the ingest window.", "2025-06-01"),
]


def write_app_store(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["App Store Review ID", "Rating", "Title", "Review", "Date"])
        for i, (rating, title, text, date) in enumerate(SAMPLES, start=1):
            w.writerow([f"AS-{i:04d}", rating, title, text, date])


def write_play_store(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "Review ID",
                "Star Rating",
                "Review Title",
                "Review Text",
                "Review Submit Date and Time",
            ]
        )
        for i, (rating, title, text, date) in enumerate(SAMPLES, start=1):
            w.writerow([f"PS-{i:04d}", rating, title, text, f"{date} 10:00:00"])


def main() -> None:
    write_app_store(RAW / "app_store.csv")
    write_play_store(RAW / "play_store.csv")
    print(f"Wrote {RAW / 'app_store.csv'}")
    print(f"Wrote {RAW / 'play_store.csv'}")


if __name__ == "__main__":
    main()
