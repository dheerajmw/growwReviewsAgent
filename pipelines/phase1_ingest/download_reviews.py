#!/usr/bin/env python3
"""
Download publicly visible Groww reviews (App Store + Play Store).

Uses third-party libraries that read public store pages — no App Store Connect /
Play Console login. Prefer official CSV exports when you have developer access.

Output: data/raw/app_store.csv, data/raw/play_store.csv
"""

from __future__ import annotations

import argparse
import csv
import logging
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
RAW_DIR = REPO / "data" / "raw"

GROWW_PLAY_PACKAGE = "com.nextbillion.groww"
GROWW_APP_STORE_ID = "1404871703"
GROWW_APP_NAME = "groww-stocks-mutual-fund-ipo"
DEFAULT_COUNTRY = "in"
DEFAULT_WEEKS = 12


def _cutoff(weeks: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(weeks=weeks)


def _in_window(dt: datetime, cutoff: datetime) -> bool:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc) >= cutoff


def download_play_reviews(
    weeks: int,
    max_fetch: int,
    country: str,
) -> list[dict]:
    from google_play_scraper import Sort, reviews

    cutoff = _cutoff(weeks)
    collected: list[dict] = []
    token = None

    logging.info("Play Store: fetching up to %s reviews (country=%s)", max_fetch, country)

    while len(collected) < max_fetch:
        batch_size = min(200, max_fetch - len(collected))
        batch, token = reviews(
            GROWW_PLAY_PACKAGE,
            lang="en",
            country=country,
            sort=Sort.NEWEST,
            count=batch_size,
            continuation_token=token,
        )
        if not batch:
            break

        oldest_in_batch = None
        for r in batch:
            at = r.get("at")
            if at is None:
                continue
            if isinstance(at, datetime) and at.tzinfo is None:
                at = at.replace(tzinfo=timezone.utc)
            oldest_in_batch = at
            if _in_window(at, cutoff):
                collected.append(r)

        if oldest_in_batch and oldest_in_batch < cutoff:
            logging.info("Play Store: reached reviews older than %s-week window", weeks)
            break
        if token is None:
            break

    logging.info("Play Store: %s reviews in %s-week window", len(collected), weeks)
    return collected


def write_play_csv(rows: list[dict], path: Path) -> None:
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
        for r in rows:
            at = r.get("at")
            if isinstance(at, datetime):
                date_str = at.strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = str(at)
            w.writerow(
                [
                    r.get("reviewId", ""),
                    r.get("score", ""),
                    "",  # Play reviews often have no title
                    (r.get("content") or "").replace("\n", " ").strip(),
                    date_str,
                ]
            )


def _parse_rss_updated(label: str) -> datetime | None:
    if not label:
        return None
    try:
        # iTunes RSS uses ISO-8601, e.g. 2026-05-16T00:08:15-07:00
        cleaned = label.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        pass
    try:
        from email.utils import parsedate_to_datetime

        return parsedate_to_datetime(label).astimezone(timezone.utc)
    except (TypeError, ValueError):
        return None


def download_app_store_reviews_rss(
    weeks: int,
    max_pages: int,
    country: str,
) -> list[dict]:
    """Fetch reviews via Apple's public iTunes RSS (no login). ~50 reviews/page, max 10 pages."""
    import json
    import time
    import urllib.error
    import urllib.request

    cutoff = _cutoff(weeks)
    collected: list[dict] = []
    logging.info("App Store RSS: country=%s, up to %s pages", country, max_pages)

    for page in range(1, max_pages + 1):
        url = (
            f"https://itunes.apple.com/{country}/rss/customerreviews/"
            f"page={page}/id={GROWW_APP_STORE_ID}/sortby=mostrecent/json"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Milestone3-ReviewPulse/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            if exc.code == 400:
                logging.info("App Store RSS: no more pages at page %s", page)
                break
            raise

        entries = payload.get("feed", {}).get("entry") or []
        if isinstance(entries, dict):
            entries = [entries]

        page_count = 0
        stop = False
        for entry in entries:
            rating_label = (entry.get("im:rating") or {}).get("label")
            if not rating_label:
                continue  # skip app metadata row
            updated_label = (entry.get("updated") or {}).get("label")
            dt = _parse_rss_updated(updated_label) if updated_label else None
            if dt is None:
                continue
            if not _in_window(dt, cutoff):
                stop = True
                continue
            content = entry.get("content") or {}
            text = content.get("label") if isinstance(content, dict) else str(content)
            title = (entry.get("title") or {}).get("label", "")
            review_id = (entry.get("id") or {}).get("label", "")
            collected.append(
                {
                    "reviewId": review_id,
                    "rating": int(rating_label),
                    "title": title,
                    "review": text or "",
                    "date": dt,
                }
            )
            page_count += 1

        logging.info("App Store RSS page %s: %s in-window reviews", page, page_count)
        if stop or page_count == 0:
            break
        time.sleep(0.3)

    logging.info("App Store: %s reviews in %s-week window", len(collected), weeks)
    return collected


def download_app_store_reviews(
    weeks: int,
    max_fetch: int,
    country: str,
) -> list[dict]:
    """Prefer iTunes RSS; fall back to app-store-scraper if RSS returns nothing."""
    rows = download_app_store_reviews_rss(weeks=weeks, max_pages=10, country=country)
    if rows:
        return rows[:max_fetch]

    logging.info("App Store RSS empty; trying app-store-scraper fallback")
    try:
        from app_store_scraper import AppStore
    except ImportError:
        return rows

    cutoff = _cutoff(weeks)
    app = AppStore(country=country, app_name=GROWW_APP_NAME, app_id=GROWW_APP_STORE_ID)
    app.review(how_many=min(max_fetch, 500))
    collected: list[dict] = []
    for r in app.reviews:
        dt = r.get("date")
        if not isinstance(dt, datetime):
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        if _in_window(dt, cutoff):
            collected.append(r)
    logging.info("App Store scraper: %s reviews in window", len(collected))
    return collected


def write_app_store_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["App Store Review ID", "Rating", "Title", "Review", "Date"])
        for i, r in enumerate(rows, start=1):
            dt = r.get("date")
            if isinstance(dt, datetime):
                date_str = dt.strftime("%Y-%m-%d")
            else:
                date_str = str(dt)
            review_id = r.get("reviewId") or f"AS-FETCH-{i}"
            w.writerow(
                [
                    review_id,
                    r.get("rating", ""),
                    (r.get("title") or "").replace("\n", " ").strip(),
                    (r.get("review") or "").replace("\n", " ").strip(),
                    date_str,
                ]
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="Download public Groww store reviews")
    parser.add_argument("--weeks", type=int, default=DEFAULT_WEEKS, help="Window 8–12 weeks")
    parser.add_argument("--max-fetch", type=int, default=3000, help="Max reviews to fetch per store")
    parser.add_argument("--country", type=str, default=DEFAULT_COUNTRY, help="Store country code")
    parser.add_argument("--play-only", action="store_true")
    parser.add_argument("--app-store-only", action="store_true")
    args = parser.parse_args()

    if args.weeks < 8 or args.weeks > 12:
        logging.error("--weeks must be between 8 and 12")
        return 1

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    play_path = RAW_DIR / "play_store.csv"
    app_path = RAW_DIR / "app_store.csv"

    try:
        if not args.app_store_only:
            play_rows = download_play_reviews(args.weeks, args.max_fetch, args.country)
            if not play_rows:
                logging.warning("No Play Store reviews in window — check network or package id")
            write_play_csv(play_rows, play_path)
            logging.info("Wrote %s (%s rows)", play_path, len(play_rows))

        if not args.play_only:
            app_rows = download_app_store_reviews(args.weeks, args.max_fetch, args.country)
            if not app_rows:
                logging.warning("No App Store reviews in window — check network or app id")
            write_app_store_csv(app_rows, app_path)
            logging.info("Wrote %s (%s rows)", app_path, len(app_rows))
    except Exception as exc:
        logging.error("Download failed: %s", exc)
        logging.error("Install deps: pip install -r requirements.txt")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
