"""HTTP client for the Phase 8 BFF (Render or local)."""

from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

DEFAULT_API = "http://127.0.0.1:8080"


def api_base() -> str:
    """Resolve API URL: secrets → env → sidebar session → default."""
    try:
        if "PULSE_API_URL" in st.secrets:
            return str(st.secrets["PULSE_API_URL"]).rstrip("/")
    except Exception:
        pass
    if url := os.environ.get("PULSE_API_URL"):
        return url.rstrip("/")
    if url := st.session_state.get("pulse_api_url"):
        return str(url).rstrip("/")
    return DEFAULT_API


def _get(path: str, timeout: int = 30) -> Any:
    base = api_base()
    url = f"{base}{path}"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


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
