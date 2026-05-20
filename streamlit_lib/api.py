"""HTTP client for the Phase 8 BFF (Render or local)."""

from __future__ import annotations

from typing import Any

import requests
import streamlit as st

from .config import default_api_url, env_api_url, is_placeholder

REQUEST_TIMEOUT = 15


def api_base() -> str:
    """Resolve API URL: session override → secrets → .env → local default."""
    if url := st.session_state.get("pulse_api_url"):
        u = str(url).strip().rstrip("/")
        if u and not is_placeholder(u):
            return u

    try:
        if "PULSE_API_URL" in st.secrets:
            u = str(st.secrets["PULSE_API_URL"]).strip().rstrip("/")
            if u and not is_placeholder(u):
                return u
    except Exception:
        pass

    if url := env_api_url():
        return url

    if url := default_api_url():
        return url

    return ""


def _get(path: str) -> Any:
    base = api_base()
    if not base:
        raise ConnectionError(
            "PULSE_API_URL is not set. Add it to Streamlit secrets, .env, or the sidebar."
        )
    url = f"{base}{path}"
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError as e:
        raise ConnectionError(
            f"Cannot reach BFF at {base}. "
            "Start locally: `.venv/bin/python -m uvicorn pipelines.phase8_frontend.api.main:app --port 8080` "
            "or set PULSE_API_URL to your Render URL."
        ) from e


def test_connection() -> tuple[bool, str]:
    """Return (ok, message) for the configured base URL."""
    base = api_base()
    if not base:
        return False, "No API URL configured."
    try:
        r = requests.get(f"{base}/api/v1/health", timeout=REQUEST_TIMEOUT)
        if r.ok and r.json().get("status") == "ok":
            return True, f"Connected to {base}"
        return False, f"Unexpected response from {base}: {r.status_code}"
    except requests.RequestException as e:
        return False, f"Cannot reach {base}: {e}"


@st.cache_data(ttl=60, show_spinner=False)
def health() -> dict[str, Any]:
    return _get("/api/v1/health")


@st.cache_data(ttl=60)
def pulse_latest() -> dict[str, Any]:
    return _get("/api/v1/pulse/latest")


@st.cache_data(ttl=60)
def pulse_weeks() -> dict[str, Any]:
    return _get("/api/v1/pulse/weeks")


@st.cache_data(ttl=60)
def themes_ranked() -> dict[str, Any]:
    return _get("/api/v1/themes/ranked")


@st.cache_data(ttl=60)
def pipeline_status() -> dict[str, Any]:
    return _get("/api/v1/pipeline/status")


@st.cache_data(ttl=60)
def publish_state() -> dict[str, Any]:
    return _get("/api/v1/publish/state")


def clear_cache() -> None:
    health.clear()
    pulse_latest.clear()
    pulse_weeks.clear()
    themes_ranked.clear()
    pipeline_status.clear()
    publish_state.clear()
