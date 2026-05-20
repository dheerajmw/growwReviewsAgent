"""Optional: embed hosted React app inside Streamlit (off by default on Streamlit Cloud)."""

from __future__ import annotations

import os

import requests
import streamlit as st
import streamlit.components.v1 as components

_EMBED_CSS = """
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"], header[data-testid="stHeader"],
#groww-sidebar-open-btn { display: none !important; }
section.main { padding: 0 !important; overflow: hidden !important; }
section.main .block-container { padding: 0 !important; max-width: 100% !important; }
.stApp { background: #F6F7F9 !important; }
.groww-iframe-wrap { width: 100%; height: calc(100vh - 1rem); min-height: 800px; border: none; }
"""


def react_ui_url() -> str | None:
    """React app URL — only when explicitly configured (not auto-default)."""
    try:
        if "PULSE_UI_URL" in st.secrets:
            raw = str(st.secrets["PULSE_UI_URL"]).strip().rstrip("/")
            if raw and not raw.upper().startswith("YOUR"):
                return raw
    except Exception:
        pass
    raw = os.environ.get("PULSE_UI_URL", "").strip().rstrip("/")
    return raw or None


def react_ui_reachable(url: str) -> bool:
    try:
        r = requests.get(url, timeout=8)
        return r.status_code < 400 and "html" in (r.headers.get("content-type") or "").lower()
    except Exception:
        return False


def use_react_embed() -> bool:
    """Only when PULSE_USE_REACT_UI=true and PULSE_UI_URL is set and reachable."""
    enabled = False
    try:
        if "PULSE_USE_REACT_UI" in st.secrets:
            enabled = str(st.secrets["PULSE_USE_REACT_UI"]).strip().lower() in ("1", "true", "yes")
    except Exception:
        pass
    if not enabled:
        enabled = os.environ.get("PULSE_USE_REACT_UI", "").strip().lower() in ("1", "true", "yes")
    if not enabled:
        return False
    url = react_ui_url()
    return bool(url and react_ui_reachable(url))


def render_react_dashboard(*, height: int = 900) -> None:
    url = react_ui_url()
    if not url:
        st.error("Set Streamlit secret `PULSE_UI_URL` to your Render static site (groww-pulse-ui).")
        st.stop()
    if not react_ui_reachable(url):
        st.error(f"Cannot reach React UI at `{url}`. Deploy groww-pulse-ui on Render first.")
        st.link_button("Open React UI in new tab", url)
        st.stop()

    st.markdown(f"<style>{_EMBED_CSS}</style>", unsafe_allow_html=True)
    safe = url.replace('"', "%22")
    components.html(
        f'<iframe class="groww-iframe-wrap" src="{safe}/" title="Groww Review Pulse" '
        f'allow="fullscreen" loading="eager" referrerpolicy="no-referrer-when-downgrade"></iframe>',
        height=height,
        scrolling=False,
    )
