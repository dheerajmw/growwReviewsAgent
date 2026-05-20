"""Embed the same React Pulse 6 app as localhost (npm run dev / groww-pulse-ui)."""

from __future__ import annotations

import os

import streamlit as st
import streamlit.components.v1 as components

from .config import is_placeholder, is_streamlit_cloud

DEFAULT_UI_URL = "https://groww-pulse-ui.onrender.com"


_EMBED_CSS = """
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"], header[data-testid="stHeader"],
#groww-sidebar-open-btn, [data-testid="stToolbar"], footer { display: none !important; }
section.main { padding: 0 !important; overflow: hidden !important; }
section.main .block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #F6F7F9 !important; }
section.main iframe {
  width: 100% !important;
  min-height: calc(100vh - 0.5rem) !important;
  border: none !important;
}
"""


def _from_secrets(key: str) -> str | None:
    try:
        if key in st.secrets:
            raw = str(st.secrets[key]).strip().rstrip("/")
            if raw and not is_placeholder(raw):
                return raw
    except Exception:
        pass
    return None


def _api_url_configured() -> str | None:
    """Remote BFF in secrets/env → treat as production (use default React host)."""
    url = _from_secrets("PULSE_API_URL") or os.environ.get("PULSE_API_URL", "").strip().rstrip("/")
    if url and not is_placeholder(url) and not url.startswith("http://127.0.0.1"):
        return url
    return None


def react_ui_url() -> str | None:
    """Hosted React URL (secrets → env → production default)."""
    url = _from_secrets("PULSE_UI_URL") or os.environ.get("PULSE_UI_URL", "").strip().rstrip("/")
    if url and not is_placeholder(url):
        return url
    if force_native_streamlit():
        return None
    if is_streamlit_cloud() or _api_url_configured():
        return DEFAULT_UI_URL
    return None


def force_native_streamlit() -> bool:
    try:
        if "PULSE_STREAMLIT_NATIVE" in st.secrets:
            v = str(st.secrets["PULSE_STREAMLIT_NATIVE"]).strip().lower()
            return v in ("1", "true", "yes")
    except Exception:
        pass
    return os.environ.get("PULSE_STREAMLIT_NATIVE", "").strip().lower() in ("1", "true", "yes")


def use_react_embed() -> bool:
    """Embed React whenever we have a UI URL (no server-side health check)."""
    if force_native_streamlit():
        return False
    return bool(react_ui_url())


def render_react_dashboard(*, height: int = 1200) -> None:
    url = react_ui_url()
    if not url:
        st.error(
            "Set Streamlit secret `PULSE_UI_URL` (e.g. https://groww-pulse-ui.onrender.com) "
            "or deploy groww-pulse-ui on Render."
        )
        st.stop()

    st.markdown(f"<style>{_EMBED_CSS}</style>", unsafe_allow_html=True)
    # Always embed — Streamlit Cloud cannot reliably preflight Render free-tier (cold start).
    components.iframe(f"{url}/", height=height, scrolling=True)

    with st.expander("Dashboard not loading?", expanded=False):
        st.markdown(
            f"If the iframe is blank, wait ~30s for Render cold start, then refresh. "
            f"Or open the React app directly: [{url}]({url}/)"
        )
        st.caption("Ensure **groww-pulse-ui** is deployed and Live on Render.")
