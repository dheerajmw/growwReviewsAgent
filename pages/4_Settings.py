"""Dashboard settings and API configuration."""

import os

import streamlit as st

from streamlit_lib import api
from streamlit_lib.ui import inject_styles, sidebar_header

inject_styles()
sidebar_header()

st.title("Settings")
st.caption("Read-only dashboard — publish stays on Render MCP / CI")

st.subheader("API connection")
env_url = os.environ.get("PULSE_API_URL", "")
secrets_url = ""
if "PULSE_API_URL" in st.secrets:
    secrets_url = st.secrets["PULSE_API_URL"]

current = api.api_base()
url = st.text_input(
    "BFF base URL (Render)",
    value=st.session_state.get("pulse_api_url", current),
    placeholder="https://groww-pulse-api.onrender.com",
    help="Phase 8 FastAPI service. No trailing slash.",
)
col_a, col_b = st.columns(2)
with col_a:
    if st.button("Save & test", type="primary"):
        st.session_state["pulse_api_url"] = url.rstrip("/")
        api.clear_cache()
        try:
            h = api.health()
            st.success(f"Connected: {h}")
        except Exception as e:
            st.error(str(e))
with col_b:
    if st.button("Clear cache"):
        api.clear_cache()
        st.rerun()

st.divider()
st.subheader("Configuration status")
try:
    pub = api.publish_state()
    h = api.health()
except Exception as e:
    st.error(str(e))
    pub, h = {}, {}

st.write(f"**BFF health:** {h.get('status', 'unknown')}")
st.write(f"**Google Doc:** {'Configured' if pub.get('doc_id') else 'Not set'}")
st.write(f"**Gmail draft:** {'Created' if pub.get('draft_id') else 'Not set'}")
st.write(f"**Week ending:** {pub.get('week_ending', '—')}")

if secrets_url:
    st.caption("Using `PULSE_API_URL` from Streamlit secrets.")
elif env_url:
    st.caption("Using `PULSE_API_URL` from environment.")
else:
    st.caption("Override URL above, or set Streamlit secret `PULSE_API_URL`.")

st.divider()
st.markdown(
    """
- [Runbook](https://github.com/dheerajmw/growwReviewsAgent/blob/main/doc/runbook.md)
- [GitHub repository](https://github.com/dheerajmw/growwReviewsAgent)
"""
)

try:
    weeks = api.pulse_weeks().get("weeks", [])
    if weeks:
        st.selectbox("Historical weeks (read-only)", weeks)
except Exception:
    pass
