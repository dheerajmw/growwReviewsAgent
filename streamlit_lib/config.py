"""Load PULSE_API_URL from .env and detect runtime."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_ENV_LOADED = False
LOCAL_BFF = "http://127.0.0.1:8080"
PLACEHOLDER_PREFIXES = ("https://YOUR", "http://YOUR", "YOUR-")


def load_env() -> None:
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(REPO_ROOT / ".env")
    except ImportError:
        pass
    _ENV_LOADED = True


def is_placeholder(url: str) -> bool:
    u = url.strip()
    return not u or any(u.startswith(p) for p in PLACEHOLDER_PREFIXES)


def is_streamlit_cloud() -> bool:
    return os.environ.get("STREAMLIT_RUNTIME_ENV") == "cloud"


def env_api_url() -> str | None:
    load_env()
    raw = os.environ.get("PULSE_API_URL", "").strip()
    if is_placeholder(raw):
        return None
    return raw.rstrip("/") if raw else None


def default_api_url() -> str | None:
    """Local BFF default only when not on Streamlit Cloud."""
    if is_streamlit_cloud():
        return None
    return LOCAL_BFF
