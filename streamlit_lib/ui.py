"""Groww Stitch design system for Streamlit (aligned with frontend/)."""

from __future__ import annotations

import streamlit as st

from . import api
from .config import LOCAL_BFF, default_api_url, env_api_url, is_streamlit_cloud

_STITCH_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}

.stApp {
  background-color: #F6F7F9 !important;
}

/* Keep Streamlit header — contains sidebar collapse / expand (>>) control */
[data-testid="stHeader"] {
  display: block !important;
  visibility: visible !important;
  height: auto !important;
  min-height: 3.25rem !important;
  background: rgba(255, 255, 255, 0.92) !important;
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #E9E9EB !important;
}

/* Re-open sidebar when collapsed — do not hide this control */
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {
  display: flex !important;
  visibility: visible !important;
  opacity: 1 !important;
  z-index: 999999 !important;
  position: relative !important;
}

[data-testid="stSidebarCollapsedControl"] button,
[data-testid="stSidebarCollapseButton"] button {
  display: inline-flex !important;
  visibility: visible !important;
  background: #00D09C !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 10px !important;
  padding: 0.4rem 0.65rem !important;
  box-shadow: 0 4px 12px rgba(0, 208, 156, 0.35) !important;
}

[data-testid="stSidebarCollapsedControl"] button:hover,
[data-testid="stSidebarCollapseButton"] button:hover {
  background: #00B88A !important;
}

section.main {
  padding-top: 0 !important;
}

.block-container {
  padding-top: 0.5rem !important;
  max-width: 1200px !important;
}

[data-testid="stSidebar"] {
  background-color: #ffffff !important;
  border-right: 1px solid #E9E9EB !important;
}

[data-testid="stSidebarNav"] a {
  font-size: 14px !important;
  font-weight: 500 !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
  background-color: #f3f2ff !important;
  border-left: 4px solid #00D09C !important;
  color: #006c4f !important;
  font-weight: 700 !important;
}

h1 { font-size: 28px !important; font-weight: 600 !important; color: #1D1D1F !important;
     letter-spacing: -0.02em !important; }
h2 { font-size: 20px !important; font-weight: 600 !important; color: #1D1D1F !important; }
h3 { font-size: 16px !important; font-weight: 600 !important; color: #1D1D1F !important; }

div[data-testid="stMetric"] {
  background: #fff; border: 1px solid #E9E9EB; border-radius: 12px;
  padding: 20px 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
div[data-testid="stMetricLabel"] { color: #7C7E8C !important; font-size: 14px !important; }
div[data-testid="stMetricValue"] { color: #171a2c !important; font-weight: 600 !important; font-size: 28px !important; }

.stButton > button[kind="primary"] {
  background-color: #00D09C !important; border: none !important; color: white !important;
  border-radius: 8px !important; font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover { background-color: #00B88A !important; }
.stButton > button[kind="secondary"] {
  border: 1px solid #00D09C !important; color: #00D09C !important; background: white !important;
  border-radius: 8px !important;
}

.stProgress > div > div { background-color: #00D09C !important; border-radius: 999px !important; }
.stProgress > div { background-color: #E9E9EB !important; border-radius: 999px !important; }

/* Stitch components */
.groww-topbar {
  position: sticky;
  top: 3.25rem;
  z-index: 998;
  display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid #E9E9EB; border-radius: 12px;
  padding: 16px 24px; margin: 0 0 24px 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  min-height: 56px;
}
.groww-topbar-title { font-size: 20px; font-weight: 700; color: #1D1D1F; line-height: 1.3; }
.groww-topbar-meta { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.groww-week { font-size: 12px; font-weight: 700; color: #006c4f; border-bottom: 2px solid #00D09C; padding-bottom: 4px; }
.groww-pii { font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 999px; }
.groww-pii-ok { background: rgba(0,208,156,0.1); color: #00D09C; }
.groww-pii-bad { background: rgba(223,81,76,0.1); color: #DF514C; }

.groww-brand { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.groww-logo {
  width: 32px; height: 32px; border-radius: 8px; background: #00D09C; color: #fff;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 16px;
}
.groww-brand-title { font-size: 16px; font-weight: 600; color: #171a2c; line-height: 1.2; }
.groww-brand-sub { font-size: 12px; color: #7C7E8C; }

.groww-card {
  background: #fff; border: 1px solid #E9E9EB; border-radius: 12px;
  padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); margin-bottom: 16px;
}
.groww-card-title { font-size: 20px; font-weight: 600; color: #1D1D1F; margin: 0 0 20px 0; }
.groww-metric-label { font-size: 14px; color: #7C7E8C; margin: 0 0 8px 0; }
.groww-metric-value { font-size: 28px; font-weight: 600; color: #171a2c; }
.groww-metric-suffix { font-size: 16px; color: #7C7E8C; margin-left: 8px; }
.groww-metric-row { display: flex; align-items: baseline; flex-wrap: wrap; gap: 8px; }
.groww-metric-value.ok { color: #00D09C; }

.groww-chip { display: inline-flex; align-items: center; padding: 6px 16px; border-radius: 999px;
  font-size: 14px; font-weight: 700; }
.groww-chip-ok { background: rgba(0,208,156,0.1); color: #00D09C; }
.groww-chip-err { background: rgba(223,81,76,0.1); color: #DF514C; }

.groww-bar-row { margin-bottom: 24px; }
.groww-bar-labels { display: flex; justify-content: space-between; font-size: 14px; margin-bottom: 8px; }
.groww-bar-name { font-weight: 600; color: #171a2c; }
.groww-bar-pct { color: #7C7E8C; }
.groww-bar-track { height: 12px; background: #E9E9EB; border-radius: 999px; overflow: hidden; }
.groww-bar-fill { height: 100%; border-radius: 999px; transition: width 0.5s ease; }

.groww-link-card { display: flex; gap: 16px; align-items: flex-start; }
.groww-link-card.groww-muted { opacity: 0.65; }
.groww-link-icon { width: 48px; height: 48px; border-radius: 8px; background: #F1F3F4;
  display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
.groww-link-body h3 { margin: 0; font-size: 16px; font-weight: 700; color: #171a2c; }
.groww-link-body p { margin: 4px 0 12px; font-size: 14px; color: #7C7E8C; }
.groww-btn-secondary {
  display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px;
  border: 1px solid #00D09C; border-radius: 8px; color: #00D09C; font-weight: 600;
  font-size: 14px; text-decoration: none; background: #fff;
}
.groww-btn-secondary:hover { background: rgba(0,208,156,0.05); }

.groww-hero-link { color: #00D09C; font-weight: 700; text-decoration: none; font-size: 16px; }
.groww-hero-link:hover { text-decoration: underline; }

.groww-footer-strip {
  display: flex; flex-wrap: wrap; align-items: center; gap: 8px;
  padding: 12px 24px; border-radius: 8px; border: 1px solid #E9E9EB;
  background: rgba(255,255,255,0.5); font-size: 12px; color: #7C7E8C; margin-top: 24px;
}
.groww-dot { opacity: 0.5; }

.groww-section-label {
  font-size: 12px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em;
  color: #7C7E8C; margin-bottom: 12px;
}
.groww-quote-block {
  border-left: 4px solid rgba(0,208,156,0.35); background: #fbf8ff;
  padding: 20px 24px; border-radius: 8px; margin-bottom: 16px;
}
.groww-quote-mark { color: #00D09C; font-size: 24px; margin: 0; line-height: 1; }
.groww-quote-text { font-style: italic; color: #44475B; margin: 8px 0 0; font-size: 14px; line-height: 1.5; }

.groww-num-item { display: flex; align-items: center; gap: 16px; margin-bottom: 12px; }
.groww-num-badge {
  width: 24px; height: 24px; border-radius: 4px; background: rgba(0,208,156,0.1);
  color: #006c4f; font-size: 12px; font-weight: 700; display: flex; align-items: center;
  justify-content: center;
}
.groww-num-text { font-size: 16px; color: #171a2c; }

.groww-phase { display: flex; gap: 12px; padding: 12px 0; border-bottom: 1px solid #E9E9EB; }
.groww-phase-icon { font-weight: 700; color: #00D09C; width: 20px; }
.groww-phase-pending .groww-phase-icon { color: #7C7E8C; }
.groww-phase-status { display: block; font-size: 12px; color: #7C7E8C; }
.groww-phase-link { font-size: 12px; color: #00D09C; font-weight: 600; margin-left: 8px; }

.groww-page-footer {
  text-align: center; font-size: 12px; color: #7C7E8C; margin-top: 48px; padding: 24px 0;
}
"""


def inject_styles() -> None:
    st.markdown(f"<style>{_STITCH_CSS}</style>", unsafe_allow_html=True)


def _suggested_bff_url() -> str:
    if url := st.session_state.get("pulse_api_url"):
        return str(url).rstrip("/")
    if url := env_api_url():
        return url
    if is_streamlit_cloud():
        return ""
    return default_api_url() or ""


def api_connection_sidebar(*, expanded: bool = False) -> None:
    with st.sidebar.expander("API connection", expanded=expanded):
        url = st.text_input(
            "BFF base URL",
            value=_suggested_bff_url(),
            placeholder="https://groww-pulse-api.onrender.com",
            help="Render groww-pulse-api URL (not localhost on Streamlit Cloud).",
            key="pulse_bff_url_input",
        )
        if st.button(
            "Connect & refresh",
            type="primary",
            use_container_width=True,
            key="pulse_bff_connect_btn",
        ):
            cleaned = url.strip().rstrip("/")
            if cleaned.startswith("http://127.0.0.1") and is_streamlit_cloud():
                st.error("On Streamlit Cloud use your Render URL, not localhost.")
            else:
                st.session_state["pulse_api_url"] = cleaned
                api.clear_cache()
                st.rerun()


def sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="groww-brand">
          <div class="groww-logo">G</div>
          <div>
            <div class="groww-brand-title">App Reviews</div>
            <div class="groww-brand-sub">Weekly Review Pulse</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_connection_status() -> None:
    ok, msg = api.test_connection()
    if ok:
        st.sidebar.markdown(
            '<p style="font-size:12px;color:#00D09C;font-weight:600;margin:0;">● API connected</p>',
            unsafe_allow_html=True,
        )
    else:
        short = msg if len(msg) < 80 else msg[:77] + "..."
        st.sidebar.warning(short)
    st.sidebar.divider()


def render_top_bar(week_label: str, pii_passed: bool) -> None:
    pii_cls = "groww-pii-ok" if pii_passed else "groww-pii-bad"
    pii_text = "PII cleared ✓" if pii_passed else "PII blocked"
    st.markdown(
        f"""
        <div class="groww-topbar">
          <div class="groww-topbar-title">Weekly Review Pulse</div>
          <div class="groww-topbar-meta">
            <span class="groww-week">Week ending {week_label}</span>
            <span class="groww-pii {pii_cls}">{pii_text}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_footer() -> None:
    st.markdown(
        '<p class="groww-page-footer">Data from public App Store &amp; Play exports · Updated via weekly pipeline</p>',
        unsafe_allow_html=True,
    )


def init_page(*, show_connection: bool = False, connection_expanded: bool = False) -> None:
    """Shared page setup: Stitch styles, sidebar brand, optional API expander."""
    inject_styles()
    sidebar_brand()
    if show_connection:
        api_connection_sidebar(expanded=connection_expanded)
    else:
        ok, _ = api.test_connection()
        if not ok:
            api_connection_sidebar(expanded=True)
    sidebar_connection_status()


def show_connection_help() -> None:
    st.error("Cannot load dashboard — BFF is not reachable.")
    base = api.api_base() or "(not set)"
    st.markdown(f"**Current URL:** `{base}`")
    if is_streamlit_cloud():
        st.warning("Set **Streamlit Secrets** → `PULSE_API_URL` to your Render URL, then reboot.")
        st.code('PULSE_API_URL = "https://groww-pulse-api.onrender.com"', language="toml")
    else:
        st.markdown(f"Local: run `./scripts/run_streamlit.sh` or API at `{LOCAL_BFF}`")


def ensure_api_connected() -> bool:
    ok, _ = api.test_connection()
    if ok:
        return True
    show_connection_help()
    return False


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
    """Inline chip (used on pulse page)."""
    from .components import pii_chip

    st.markdown(pii_chip(passed), unsafe_allow_html=True)
