"""Theme rankings and share of voice."""

import pandas as pd
import streamlit as st

from streamlit_lib import api
from streamlit_lib.ui import ensure_api_connected, inject_styles, sidebar_header

inject_styles()
sidebar_header()

if not ensure_api_connected():
    st.stop()

st.title("Review themes")
st.caption("Ranked themes from sampled App Store & Play reviews")

try:
    data = api.themes_ranked()
except Exception as e:
    st.error(str(e))
    st.stop()

ranked = data.get("ranked", [])
meta = data.get("metadata", {})
if not ranked:
    st.warning("No themes returned from API.")
    st.stop()

sample = meta.get("sample_count", "—")
st.metric("Sample size", f"{sample} reviews")

chart_col, table_col = st.columns([1, 1.2])

with chart_col:
    st.subheader("Share of voice")
    df_chart = pd.DataFrame(
        {"Theme": [t["label"] for t in ranked], "Share %": [t["pct_of_sample"] for t in ranked]}
    )
    st.bar_chart(df_chart.set_index("Theme"), color="#00D09C")

with table_col:
    st.subheader("Ranked themes")
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
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
