"""
Groww Weekly Review Pulse — Streamlit dashboard.

Calls the Phase 8 BFF on Render (or local). Set PULSE_API_URL in Streamlit secrets.
"""

from __future__ import annotations

import streamlit as st

from streamlit_lib import api
from streamlit_lib.ui import format_week, inject_styles, pii_badge, sidebar_header

st.set_page_config(
    page_title="Groww — Weekly Review Pulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()
sidebar_header()

# Optional API override (Settings page also sets this)
with st.sidebar.expander("API connection", expanded=False):
    default = api.api_base()
    url = st.text_input("BFF base URL", value=default, help="Render service URL, no trailing slash")
    if st.button("Apply & refresh"):
        st.session_state["pulse_api_url"] = url.rstrip("/")
        api.clear_cache()
        st.rerun()

try:
    pipeline = api.pipeline_status()
except Exception as e:
    st.error(f"Cannot load dashboard: {e}")
    st.info("Deploy the BFF on Render and set `PULSE_API_URL` in Streamlit secrets.")
    st.stop()

publish = pipeline.get("publish_state") or {}
week = format_week(publish.get("week_ending"))
st.caption(f"Week ending **{week}**")
pii_badge(pipeline.get("pii_passed", False))

st.title("This week's pulse")
st.markdown("Executive summary from mobile app reviews")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Reviews analyzed", pipeline.get("normalized_count") or pipeline.get("sample_count") or "—")
with col2:
    try:
        pulse = api.pulse_latest()
        wc, mx = pulse.get("word_count", 0), pulse.get("max_words", 250)
        st.metric("Word count", f"{wc} / {mx}")
    except Exception:
        st.metric("Word count", "—")
with col3:
    st.metric("PII gate", "Passed" if pipeline.get("pii_passed") else "Blocked")

try:
    themes = api.themes_ranked()
    ranked = themes.get("ranked", [])[:3]
except Exception:
    ranked = []

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Top 3 themes")
    if ranked:
        import pandas as pd

        df = pd.DataFrame(
            [{"Theme": t["label"], "Share %": t["pct_of_sample"]} for t in ranked]
        )
        for _, row in df.iterrows():
            st.write(f"**{row['Theme']}** — {row['Share %']}%")
            st.progress(min(float(row["Share %"]) / 100.0, 1.0))
    else:
        st.info("No theme data from API.")

with right:
    st.subheader("Publish")
    if publish.get("doc_url"):
        st.link_button("Open Google Doc", publish["doc_url"], use_container_width=True)
    else:
        st.caption("Google Doc not published yet.")
    draft_url = publish.get("draft_url") or "https://mail.google.com/mail/u/0/#drafts"
    if publish.get("draft_id"):
        st.link_button("Open Gmail Drafts", draft_url, use_container_width=True)
    else:
        st.caption("Gmail draft not created yet.")

st.divider()
st.caption("Data from public App Store & Play exports · BFF on Render · UI on Streamlit")
