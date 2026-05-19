#!/usr/bin/env python3
"""
Generate Google OAuth token.json for Docs + Gmail (Phase 0 / MCP).

Requires credentials.json (OAuth Desktop client) in repo root.
Opens a browser for consent; writes token.json (gitignored).

Usage:
  python3 auth.py
  python3 auth.py --credentials path/to/credentials.json --token path/to/token.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_CREDENTIALS = REPO_ROOT / "credentials.json"
DEFAULT_TOKEN = REPO_ROOT / "token.json"

# Milestone 3: weekly Doc + Gmail draft (no send required)
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/drive.file",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Google OAuth token generator")
    parser.add_argument(
        "--credentials",
        type=Path,
        default=DEFAULT_CREDENTIALS,
        help="OAuth client secrets JSON (Desktop app)",
    )
    parser.add_argument(
        "--token",
        type=Path,
        default=DEFAULT_TOKEN,
        help="Output token path",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=0,
        help="Local server port (0 = random)",
    )
    args = parser.parse_args()

    if not args.credentials.is_file():
        print(f"Missing credentials file: {args.credentials}", file=sys.stderr)
        print("Download OAuth Desktop client JSON from Google Cloud Console.", file=sys.stderr)
        return 1

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Install: pip install google-auth-oauthlib", file=sys.stderr)
        return 1

    print(f"Using credentials: {args.credentials}", flush=True)
    print(f"Scopes: {', '.join(SCOPES)}", flush=True)
    print("Opening browser for Google sign-in…", flush=True)
    print("(Complete sign-in in the browser; this script waits until you approve.)", flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(str(args.credentials), SCOPES)
    creds = flow.run_local_server(
        port=args.port,
        open_browser=True,
        authorization_prompt_message="Open this URL in your browser to authorize:\n{url}",
        success_message="Authorization complete. You can close this browser tab.",
    )

    args.token.parent.mkdir(parents=True, exist_ok=True)
    args.token.write_text(creds.to_json(), encoding="utf-8")
    print(f"Wrote token: {args.token}")
    print("Keep token.json private (already in .gitignore).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
