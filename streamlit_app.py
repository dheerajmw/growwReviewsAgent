"""
Groww Weekly Review Pulse — Streamlit dashboard (Pulse 6 design).

Runs the native Stitch-styled Streamlit UI on Streamlit Cloud (recommended).
Optional React embed: set PULSE_USE_REACT_UI=true and PULSE_UI_URL in secrets.
"""

from __future__ import annotations

import streamlit as st

from streamlit_lib import api
from streamlit_lib import components as stitch
from streamlit_lib.embed import render_react_dashboard, use_react_embed
from streamlit_lib.ui import (
    ensure_api_connected,
    format_week,
    init_page,
    render_page_footer,
    render_top_bar,
)

_embed_react = use_react_embed()

st.set_page_config(
    page_title="Groww — Weekly Review Pulse",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed" if _embed_react else "expanded",
)

if _embed_react:
    render_react_dashboard()
    st.stop()

init_page()

if not ensure_api_connected():
    st.stop()

try:
    pipeline = api.pipeline_status()
except Exception as e:
    st.error(str(e))
    st.stop()

publish = pipeline.get("publish_state") or {}
week = format_week(publish.get("week_ending"))
pii_ok = pipeline.get("pii_passed", False)

render_top_bar(week, pii_ok)

st.link_button(
    "Open full React dashboard ↗",
    "https://groww-pulse-ui.onrender.com",
    help="Optional hosted UI (same as npm run dev)",
)

hero_l, hero_r = st.columns([3, 1])
with hero_l:
    st.markdown("## This week's pulse")
    st.caption("Executive summary from mobile app reviews")
with hero_r:
    st.page_link("pages/1_Weekly_Pulse.py", label="Read full pulse →", icon="📈")

try:
    pulse = api.pulse_latest()
    wc, mx = pulse.get("word_count", 0), pulse.get("max_words", 250)
except Exception:
    wc, mx = 0, 250

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(
        stitch.metric_card(
            "Reviews analyzed",
            str(pipeline.get("normalized_count") or pipeline.get("sample_count") or "—"),
        ),
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        stitch.metric_card("Word count", str(wc), f"/ {mx} max", value_class="ok" if wc <= mx else ""),
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        f'{stitch.card_open()}<p class="groww-metric-label">PII gate</p>{stitch.pii_chip(pii_ok)}{stitch.card_close()}',
        unsafe_allow_html=True,
    )

try:
    themes = api.themes_ranked()
    ranked = themes.get("ranked", [])[:3]
except Exception:
    ranked = []

left, right = st.columns([1.15, 1])
with left:
    if ranked:
        st.markdown(stitch.theme_progress_bars(ranked), unsafe_allow_html=True)
    else:
        st.info("No theme data from API.")

with right:
    draft_url = publish.get("draft_url") or "https://mail.google.com/mail/u/0/#drafts"
    st.markdown(stitch.doc_link_card(publish.get("doc_url")), unsafe_allow_html=True)
    st.markdown(
        stitch.draft_link_card(draft_url, bool(publish.get("draft_id"))),
        unsafe_allow_html=True,
    )

st.markdown(
    stitch.pipeline_footer_strip(publish.get("published_at")),
    unsafe_allow_html=True,
)
render_page_footer()
