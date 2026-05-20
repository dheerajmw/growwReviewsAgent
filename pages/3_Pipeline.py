"""Pipeline phase status — Stitch layout (matches React PipelinePage)."""

import streamlit as st

from streamlit_lib import api
from streamlit_lib import components as stitch
from streamlit_lib.ui import (
    ensure_api_connected,
    format_week,
    init_page,
    render_page_footer,
    render_top_bar,
)

init_page()

if not ensure_api_connected():
    st.stop()

try:
    data = api.pipeline_status()
except Exception as e:
    st.error(str(e))
    st.stop()

publish = data.get("publish_state") or {}
render_top_bar(format_week(publish.get("week_ending")), data.get("pii_passed", False))

st.markdown("## Pipeline status")
st.caption("Phases 1–7 · automated refresh via GitHub Actions")

left, right = st.columns([1.6, 1])

with left:
    st.markdown(stitch.card_open(), unsafe_allow_html=True)
    for phase in data.get("phases", []):
        extra = ""
        if phase.get("id") == 5 and publish.get("doc_url"):
            extra = publish["doc_url"]
        st.markdown(
            stitch.phase_row(phase.get("name", ""), bool(phase.get("complete")), extra),
            unsafe_allow_html=True,
        )
    st.markdown(stitch.card_close(), unsafe_allow_html=True)

with right:
    st.markdown(
        f"""{stitch.card_open()}
        <div style="display:flex;gap:16px;align-items:flex-start;">
          <div class="groww-link-icon">📅</div>
          <div>
            <h3 style="margin:0;font-size:16px;">Scheduler</h3>
            <p style="color:#7C7E8C;font-size:14px;">{data.get("scheduler", {}).get("description", "Monday 06:00 UTC")}</p>
          </div>
        </div>
        {stitch.card_close()}""",
        unsafe_allow_html=True,
    )
    st.link_button(
        "View GitHub Actions",
        "https://github.com/dheerajmw/growwReviewsAgent/actions",
        use_container_width=True,
    )

    st.markdown(stitch.card_open() + '<p class="groww-section-label">Counts</p>', unsafe_allow_html=True)
    st.write(f"**Normalized reviews:** {data.get('normalized_count', '—')}")
    st.write(f"**Sample size:** {data.get('sample_count', '—')}")
    st.markdown(stitch.card_close(), unsafe_allow_html=True)

    if st.button("Refresh data", type="primary", use_container_width=True):
        api.clear_cache()
        st.rerun()

    blocked = (data.get("blockers") or {}).get("publish_blocked")
    if blocked:
        st.error("PII blockers detected — publish is blocked.")

render_page_footer()
