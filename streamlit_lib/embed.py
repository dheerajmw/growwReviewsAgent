"""Embed the React (Vite) dashboard inside Streamlit Cloud."""

from __future__ import annotations

import os

import streamlit as st
import streamlit.components.v1 as components

_EMBED_CSS = """
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"], header[data-testid="stHeader"],
#groww-sidebar-open-btn {
  display: none !important;
}
section.main {
  padding: 0 !important;
  overflow: hidden !important;
}
section.main .block-container {
  padding: 0 !important;
  max-width: 100% !important;
}
.stApp { background: #F6F7F9 !important; }
"""


def react_ui_url() -> str | None:
    """Resolve hosted React app URL (Streamlit secret or env)."""
    try:
        if "PULSE_UI_URL" in st.secrets:
            raw = str(st.secrets["PULSE_UI_URL"]).strip().rstrip("/")
            if raw and not raw.startswith("YOUR"):
                return raw
    except Exception:
        pass
    raw = os.environ.get("PULSE_UI_URL", "").strip().rstrip("/")
    if raw:
        return raw
    # Default after Render static site deploy (see render.yaml groww-pulse-ui)
    return "https://groww-pulse-ui.onrender.com"


def render_react_dashboard(*, height: int = 920) -> None:
    """Full-page iframe to the Pulse 6 React app (same UI as npm run dev)."""
    url = react_ui_url()
    if not url:
        st.error(
            "React UI URL not configured. Set Streamlit secret `PULSE_UI_URL` "
            "to your deployed frontend (e.g. Render static site)."
        )
        st.stop()

    st.markdown(f"<style>{_EMBED_CSS}</style>", unsafe_allow_html=True)
    components.iframe(f"{url}/", height=height, scrolling=False)


def use_react_embed() -> bool:
    """True unless native Streamlit UI is explicitly requested."""
    flag = os.environ.get("PULSE_STREAMLIT_NATIVE", "").strip().lower()
    if flag in ("1", "true", "yes"):
        return False
    try:
        if "PULSE_STREAMLIT_NATIVE" in st.secrets:
            return str(st.secrets["PULSE_STREAMLIT_NATIVE"]).strip().lower() not in (
                "1",
                "true",
                "yes",
            )
    except Exception:
        pass
    return True
