"""Groww-style Streamlit chrome."""

from __future__ import annotations

import streamlit as st

from . import api


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp { background-color: #F6F7F9; }
        [data-testid="stSidebar"] { background-color: #ffffff; }
        h1, h2, h3 { color: #1D1D1F !important; letter-spacing: -0.02em; }
        div[data-testid="stMetricValue"] { color: #171a2c; font-weight: 600; }
        .stButton > button[kind="primary"] {
            background-color: #00D09C; border: none; color: white;
        }
        .stButton > button[kind="primary"]:hover { background-color: #00B88A; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_header() -> None:
    st.sidebar.markdown("### Groww")
    st.sidebar.caption("Weekly Review Pulse · App reviews")
    try:
        h = api.health()
        st.sidebar.success("API connected") if h.get("status") == "ok" else st.sidebar.warning("API unknown")
    except Exception as e:
        st.sidebar.error(f"API unreachable: {e}")
    st.sidebar.divider()


def format_week(iso: str | None) -> str:
    if not iso:
        return "—"
    try:
        from datetime import datetime

        d = datetime.strptime(iso[:10], "%Y-%m-%d")
        return d.strftime("%d %b %Y")
    except ValueError:
        return iso


def pii_badge(passed: bool) -> None:
    if passed:
        st.success("PII cleared ✓")
    else:
        st.error("PII blocked")
