"""Weekly pulse note (paraphrased themes, quotes, actions)."""

import streamlit as st

from streamlit_lib import api
from streamlit_lib.ui import ensure_api_connected, inject_styles, pii_badge, sidebar_header

inject_styles()
sidebar_header()

st.title("Weekly Pulse")

if not ensure_api_connected():
    st.stop()

try:
    pulse = api.pulse_latest()
    pipeline = api.pipeline_status()
except Exception as e:
    st.error(str(e))
    st.stop()

note = pulse.get("note")
if not note:
    st.warning("No weekly note on the API. Run Phase 3 locally or sync data to Render.")
    if pulse.get("markdown"):
        st.markdown(pulse["markdown"])
    st.stop()

st.header(note.get("title", "Weekly Review Pulse"))
wc, mx = pulse.get("word_count", 0), pulse.get("max_words", 250)
ok = wc <= mx
st.caption(f"{'✓' if ok else '⚠'} {wc} / {mx} words")
pii_badge(pipeline.get("pii_passed", False))

col_main, col_side = st.columns([2, 1])

with col_main:
    st.subheader("Top themes")
    for i, t in enumerate(note.get("themes", []), 1):
        st.markdown(f"**{i}.** {t.get('headline', t.get('id', ''))}")

    st.subheader("What users are saying")
    for q in note.get("quotes", []):
        st.markdown(f"> {q.get('paraphrased', '')}")

    st.subheader("Suggested actions")
    for i, a in enumerate(note.get("actions", []), 1):
        st.markdown(f"{i}. {a.get('text', '')}")

    if pulse.get("markdown"):
        with st.expander("Full markdown"):
            st.markdown(pulse["markdown"])

with col_side:
    publish = pipeline.get("publish_state") or {}
    st.subheader("Quick links")
    if publish.get("doc_url"):
        st.link_button("Google Doc", publish["doc_url"], use_container_width=True)
    if publish.get("draft_id"):
        url = publish.get("draft_url") or "https://mail.google.com/mail/u/0/#drafts"
        st.link_button("Gmail Drafts", url, use_container_width=True)
