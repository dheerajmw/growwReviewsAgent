"""Groww-style Streamlit chrome."""

from __future__ import annotations

import streamlit as st

from . import api
from .config import LOCAL_BFF, default_api_url, env_api_url


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background-color: #F6F7F9; }
        [data-testid="stSidebar"] { background-color: #ffffff; }
        h1, h2, h3 { color: #1D1D1F !important; letter-spacing: -0.02em; }
        div[data-testid="stMetricValue"] { color: #171a2c; font-weight: 600; }
        .stButton > button[kind="primary"] {
            background-color: #00D09C; border: none; color: white;
        }
        .stButton > button[kind="primary"]:hover { background-color: #00B88A; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def api_connection_sidebar(expanded: bool = False) -> None:
    """Configure BFF URL in the sidebar."""
    with st.sidebar.expander("API connection", expanded=expanded):
        suggested = env_api_url() or st.session_state.get("pulse_api_url") or default_api_url() or ""
        url = st.text_input(
            "BFF base URL",
            value=suggested,
            placeholder="https://groww-pulse-api.onrender.com",
            help="Render Phase 8 API URL (no trailing slash). Not the MCP server.",
        )
        if st.button("Connect & refresh", type="primary", use_container_width=True):
            st.session_state["pulse_api_url"] = url.strip().rstrip("/")
            api.clear_cache()
            st.rerun()


def sidebar_header() -> None:
    st.sidebar.markdown("### Groww")
    st.sidebar.caption("Weekly Review Pulse · App reviews")
    ok, msg = api.test_connection()
    if ok:
        st.sidebar.success(msg)
    else:
        st.sidebar.error(msg.split(":")[0] if ":" in msg else msg)
    st.sidebar.divider()


def show_connection_help() -> None:
    """Main-area help when the BFF is unreachable."""
    st.error("Cannot load dashboard — BFF is not reachable.")
    st.markdown(
        f"""
**Choose one:**

1. **Render (production)** — Deploy the BFF from `render.yaml`, then set the URL:
   - Streamlit Cloud → **Secrets** → `PULSE_API_URL = "https://your-service.onrender.com"`
   - Local → add to `.env`: `PULSE_API_URL=https://your-service.onrender.com`

2. **Local dev** — Run both services:
   ```bash
   ./scripts/run_streamlit.sh
   ```
   Or start the API only: `uvicorn pipelines.phase8_frontend.api.main:app --port 8080`  
   Default local URL: `{LOCAL_BFF}`

Use the **API connection** box in the sidebar to enter your URL, then click **Connect & refresh**.
        """
    )
    api_connection_sidebar(expanded=True)


def ensure_api_connected() -> bool:
    """Return True if health check passes; otherwise show help and return False."""
    ok, _ = api.test_connection()
    if ok:
        return True
    show_connection_help()
    return False


def format_week(iso: str | None) -> str:
    if not iso:
        return "—"
    try:
        from datetime import datetime

        d = datetime.strptime(iso[:10], "%Y-%m-%d")
        return d.strftime("%d %b %Y")
    except ValueError:
        return iso


def pii_badge(passed: bool) -> None:
    if passed:
        st.success("PII cleared ✓")
    else:
        st.error("PII blocked")
