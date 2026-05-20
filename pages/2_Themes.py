"""Theme rankings — Stitch layout (matches React ThemesPage)."""

import pandas as pd
import streamlit as st

from streamlit_lib import api
from streamlit_lib import components as stitch
from streamlit_lib.ui import ensure_api_connected, init_page, render_page_footer, render_top_bar

init_page()

if not ensure_api_connected():
    st.stop()

try:
    pipeline = api.pipeline_status()
    data = api.themes_ranked()
except Exception as e:
    st.error(str(e))
    st.stop()

publish = pipeline.get("publish_state") or {}
from streamlit_lib.ui import format_week

render_top_bar(format_week(publish.get("week_ending")), pipeline.get("pii_passed", False))

st.markdown("## Review themes")
st.caption("Up to 5 themes from sampled App Store & Play reviews")

ranked = data.get("ranked", [])
meta = data.get("metadata", {})
if not ranked:
    st.warning("No themes returned from API.")
    st.stop()

sample = meta.get("sample_count", "—")

chart_col, side_col = st.columns([1.4, 1])

with chart_col:
    st.markdown(
        f'{stitch.card_open()}<h3 class="groww-card-title" style="font-size:14px;color:#7C7E8C;font-weight:500;">Share of voice</h3>',
        unsafe_allow_html=True,
    )
    df_chart = pd.DataFrame(
        {"Share %": [t["pct_of_sample"] for t in ranked]},
        index=[t["label"] for t in ranked],
    )
    st.bar_chart(df_chart, color="#00D09C", height=280)
    st.markdown(stitch.card_close(), unsafe_allow_html=True)

with side_col:
    st.markdown(
        stitch.metric_card("Sample size", str(sample), "reviews", value_class="ok"),
        unsafe_allow_html=True,
    )
    st.markdown(
        f'{stitch.card_open()}<p class="groww-metric-label">Stores</p>'
        f'<p style="font-size:14px;color:#44475B;margin:8px 0;">App Store &amp; Play Store exports</p>'
        f"{stitch.card_close()}",
        unsafe_allow_html=True,
    )

st.markdown("### Ranked themes")
rows = []
for i, t in enumerate(ranked, 1):
    low_pct = round(100 * t["low_rating_count"] / t["review_count"]) if t["review_count"] else 0
    rows.append(
        {
            "Rank": f"#{i}",
            "Theme": t["label"],
            "Reviews": t["review_count"],
            "% sample": t["pct_of_sample"],
            "Low ratings %": low_pct,
        }
    )
st.dataframe(
    pd.DataFrame(rows),
    use_container_width=True,
    hide_index=True,
    column_config={
        "% sample": st.column_config.NumberColumn(format="%.1f"),
        "Low ratings %": st.column_config.NumberColumn(format="%d"),
    },
)

render_page_footer()
