"""Pipeline phase status."""

import streamlit as st

from streamlit_lib import api
from streamlit_lib.ui import ensure_api_connected, inject_styles, sidebar_header

inject_styles()
sidebar_header()

if not ensure_api_connected():
    st.stop()

st.title("Pipeline status")
st.caption("Phases 1–7 · automated refresh via GitHub Actions")

try:
    data = api.pipeline_status()
except Exception as e:
    st.error(str(e))
    st.stop()

scheduler = data.get("scheduler", {})
publish = data.get("publish_state") or {}
blocked = (data.get("blockers") or {}).get("publish_blocked")

left, right = st.columns([1.5, 1])

with left:
    for phase in data.get("phases", []):
        icon = "✅" if phase.get("complete") else "⏳"
        st.markdown(f"{icon} **{phase.get('name')}** — {'complete' if phase.get('complete') else 'pending'}")
        if phase.get("id") == 5 and publish.get("doc_url"):
            st.link_button("View document", publish["doc_url"], key=f"doc_{phase['id']}")

with right:
    st.subheader("Scheduler")
    st.write(scheduler.get("description", "Monday 06:00 UTC"))
    st.code(scheduler.get("cron", "0 6 * * 1"))
    st.link_button(
        "View GitHub Actions",
        "https://github.com/dheerajmw/growwReviewsAgent/actions",
        use_container_width=True,
    )

    st.subheader("Counts")
    st.write(f"Normalized reviews: **{data.get('normalized_count', '—')}**")
    st.write(f"Sample size: **{data.get('sample_count', '—')}**")

    if blocked:
        st.error("PII blockers detected — publish is blocked.")

    if st.button("Refresh data"):
        api.clear_cache()
        st.rerun()
