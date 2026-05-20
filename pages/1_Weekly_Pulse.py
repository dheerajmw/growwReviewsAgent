"""Weekly pulse note — Stitch layout (matches React PulsePage)."""

import streamlit as st

from streamlit_lib import api
from streamlit_lib import components as stitch
from streamlit_lib.ui import (
    ensure_api_connected,
    format_week,
    init_page,
    pii_badge,
    render_page_footer,
    render_top_bar,
)

init_page()

if not ensure_api_connected():
    st.stop()

try:
    pulse = api.pulse_latest()
    pipeline = api.pipeline_status()
except Exception as e:
    st.error(str(e))
    st.stop()

publish = pipeline.get("publish_state") or {}
render_top_bar(format_week(publish.get("week_ending")), pipeline.get("pii_passed", False))

note = pulse.get("note")
if not note:
    st.warning("No weekly note on the API. Run Phase 3 locally or sync data to Render.")
    if pulse.get("markdown"):
        st.markdown(pulse["markdown"])
    st.stop()

wc, mx = pulse.get("word_count", 0), pulse.get("max_words", 250)
col_title, col_meta = st.columns([3, 1])
with col_title:
    st.markdown(f"## {note.get('title', 'Weekly Review Pulse')}")
with col_meta:
    st.caption(f"{'✓' if wc <= mx else '⚠'} {wc} / {mx} words")
    pii_badge(pipeline.get("pii_passed", False))

main, side = st.columns([2.2, 1])

with main:
    parts = [stitch.card_open()]
    parts.append(stitch.section_label("Top themes"))
    for i, t in enumerate(note.get("themes", []), 1):
        parts.append(stitch.numbered_theme(t.get("headline", t.get("id", "")), i))
    parts.append(stitch.section_label("What users are saying"))
    for q in note.get("quotes", []):
        parts.append(stitch.quote_block(q.get("paraphrased", "")))
    parts.append(stitch.section_label("Suggested actions"))
    for i, a in enumerate(note.get("actions", []), 1):
        parts.append(stitch.numbered_theme(a.get("text", ""), i))
    parts.append(stitch.card_close())
    st.markdown("\n".join(parts), unsafe_allow_html=True)
    if pulse.get("markdown"):
        with st.expander("Full markdown"):
            st.markdown(pulse["markdown"])

with side:
    st.markdown("### Quick links")
    st.markdown(stitch.doc_link_card(publish.get("doc_url")), unsafe_allow_html=True)
    draft_url = publish.get("draft_url") or "https://mail.google.com/mail/u/0/#drafts"
    st.markdown(
        stitch.draft_link_card(draft_url, bool(publish.get("draft_id"))),
        unsafe_allow_html=True,
    )

render_page_footer()
