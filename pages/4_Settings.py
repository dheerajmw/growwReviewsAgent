"""Settings — Stitch layout (matches React SettingsPage)."""

import os

import streamlit as st

from streamlit_lib import api
from streamlit_lib import components as stitch
from streamlit_lib.ui import ensure_api_connected, init_page, render_page_footer

init_page(show_connection=True, connection_expanded=True)

st.markdown("## Settings")
st.caption("Manage dashboard preferences and data pipeline configuration")

if not ensure_api_connected():
    st.stop()

st.markdown(stitch.card_open(), unsafe_allow_html=True)
st.markdown("#### API connection")
env_url = os.environ.get("PULSE_API_URL", "")
secrets_url = str(st.secrets.get("PULSE_API_URL", "")) if "PULSE_API_URL" in st.secrets else ""

current = api.api_base()
url = st.text_input(
    "BFF base URL (Render)",
    value=st.session_state.get("pulse_api_url", current),
    placeholder="https://groww-pulse-api.onrender.com",
    help="Phase 8 FastAPI service. No trailing slash.",
)
col_a, col_b = st.columns(2)
with col_a:
    if st.button("Save & test", type="primary", use_container_width=True):
        st.session_state["pulse_api_url"] = url.rstrip("/")
        api.clear_cache()
        try:
            h = api.health()
            st.success(f"Connected: {h}")
        except Exception as e:
            st.error(str(e))
with col_b:
    if st.button("Clear cache", use_container_width=True):
        api.clear_cache()
        st.rerun()
st.markdown(stitch.card_close(), unsafe_allow_html=True)

try:
    pub = api.publish_state()
    h = api.health()
    weeks = api.pulse_weeks().get("weeks", [])
except Exception as e:
    st.error(str(e))
    pub, h, weeks = {}, {}, []

st.markdown(stitch.card_open(), unsafe_allow_html=True)
st.markdown("#### Week selection")
if weeks:
    st.selectbox("Historical weekly pulses (read-only)", weeks)
else:
    st.caption("No historical weeks on API yet.")
st.markdown(stitch.card_close(), unsafe_allow_html=True)

st.markdown(stitch.card_open(), unsafe_allow_html=True)
st.markdown("#### Configuration status")

def _row(label: str, ok: bool, status: str) -> None:
    chip = "groww-chip-ok" if ok else "groww-chip-err"
    st.markdown(
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #E9E9EB;">'
        f"<span style='font-size:14px;'>{label}</span>"
        f'<span class="groww-chip {chip}">{status}</span></div>',
        unsafe_allow_html=True,
    )


_row("BFF health", h.get("status") == "ok", h.get("status", "unknown"))
_row("Google Doc", bool(pub.get("doc_id")), "Configured ✓" if pub.get("doc_id") else "Not set")
_row("Gmail draft", bool(pub.get("draft_id")), "Created" if pub.get("draft_id") else "Not set")
st.caption(f"Week ending: {pub.get('week_ending', '—')}")

if secrets_url:
    st.caption("Using `PULSE_API_URL` from Streamlit secrets.")
elif env_url:
    st.caption("Using `PULSE_API_URL` from environment.")
else:
    st.caption("Set Streamlit secret `PULSE_API_URL` or save URL above.")

st.markdown(stitch.card_close(), unsafe_allow_html=True)

st.markdown(
    """
- [Runbook](https://github.com/dheerajmw/growwReviewsAgent/blob/main/doc/runbook.md)
- [GitHub repository](https://github.com/dheerajmw/growwReviewsAgent)
- **Local React UI (Stitch):** run `cd frontend && npm run dev` for the full Vite dashboard
"""
)

render_page_footer()
