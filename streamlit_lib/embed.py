"""Embed the same React Pulse 6 app as localhost (npm run dev / groww-pulse-ui)."""

from __future__ import annotations

import os

import requests
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


def react_ui_url() -> str | None:
    """Hosted React URL (secrets → env → Streamlit Cloud default)."""
    url = _from_secrets("PULSE_UI_URL") or os.environ.get("PULSE_UI_URL", "").strip().rstrip("/")
    if url and not is_placeholder(url):
        return url
    if is_streamlit_cloud():
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


def react_ui_reachable(url: str) -> bool:
    try:
        r = requests.get(url, timeout=10)
        body = r.text[:2000] if r.text else ""
        return (
            r.status_code < 400
            and ("html" in (r.headers.get("content-type") or "").lower() or "<html" in body.lower())
            and ("/assets/" in body or "root" in body)
        )
    except Exception:
        return False


def use_react_embed() -> bool:
    """Same UI as localhost:5173 when React host is configured and healthy."""
    if force_native_streamlit():
        return False
    url = react_ui_url()
    if not url:
        return False
    return react_ui_reachable(url)


def render_react_dashboard(*, height: int = 1200) -> None:
    url = react_ui_url()
    if not url:
        st.error("Set `PULSE_UI_URL` in Streamlit secrets (e.g. https://groww-pulse-ui.onrender.com).")
        st.stop()
    if not react_ui_reachable(url):
        st.warning(f"React UI at `{url}` is not reachable. Deploy **groww-pulse-ui** on Render, then reboot.")
        st.link_button("Open React UI", url)
        st.stop()

    st.markdown(f"<style>{_EMBED_CSS}</style>", unsafe_allow_html=True)
    components.iframe(
        f"{url}/",
        height=height,
        scrolling=True,
    )
