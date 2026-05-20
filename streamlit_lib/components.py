"""Stitch-style HTML components for Streamlit (matches React frontend)."""

from __future__ import annotations

import html
from typing import Any


def _e(text: Any) -> str:
    return html.escape(str(text)) if text is not None else ""


def card_open(extra_class: str = "") -> str:
    cls = f"groww-card {extra_class}".strip()
    return f'<div class="{cls}">'


def card_close() -> str:
    return "</div>"


def metric_card(label: str, value: str, suffix: str = "", *, value_class: str = "") -> str:
    val_html = f'<span class="groww-metric-value {value_class}">{_e(value)}</span>'
    suffix_html = f'<span class="groww-metric-suffix">{_e(suffix)}</span>' if suffix else ""
    return f"""
{card_open()}
  <p class="groww-metric-label">{_e(label)}</p>
  <div class="groww-metric-row">{val_html}{suffix_html}</div>
{card_close()}
"""


def pii_chip(passed: bool) -> str:
    if passed:
        return '<span class="groww-chip groww-chip-ok">✓ Passed</span>'
    return '<span class="groww-chip groww-chip-err">Blocked</span>'


def theme_progress_bars(themes: list[dict[str, Any]], limit: int = 3) -> str:
    colors = ["#00D09C", "#00B88A", "#00A37A"]
    parts = [card_open(), '<h3 class="groww-card-title">Top 3 themes</h3>']
    for i, t in enumerate(themes[:limit]):
        label = _e(t.get("label", ""))
        pct = float(t.get("pct_of_sample") or 0)
        color = colors[i % len(colors)]
        parts.append(
            f"""
<div class="groww-bar-row">
  <div class="groww-bar-labels"><span class="groww-bar-name">{label}</span>
    <span class="groww-bar-pct">{pct:g}%</span></div>
  <div class="groww-bar-track"><div class="groww-bar-fill" style="width:{min(pct,100)}%;background:{color}"></div></div>
</div>"""
        )
    parts.append(card_close())
    return "\n".join(parts)


def doc_link_card(doc_url: str | None) -> str:
    if doc_url:
        return f"""
{card_open("groww-link-card")}
  <div class="groww-link-icon groww-icon-docs">📄</div>
  <div class="groww-link-body">
    <h3>Google Doc</h3>
    <p>Open weekly document</p>
    <a class="groww-btn-secondary" href="{_e(doc_url)}" target="_blank" rel="noopener">Open in Docs ↗</a>
  </div>
{card_close()}"""
    return f"""
{card_open("groww-link-card groww-muted")}
  <div class="groww-link-icon groww-icon-docs">📄</div>
  <div class="groww-link-body"><h3>Google Doc</h3><p>Not published yet</p></div>
{card_close()}"""


def draft_link_card(draft_url: str | None, has_draft: bool) -> str:
    if has_draft and draft_url:
        return f"""
{card_open("groww-link-card")}
  <div class="groww-link-icon groww-icon-mail">✉️</div>
  <div class="groww-link-body">
    <h3>Gmail draft</h3>
    <p>Review before sending</p>
    <a class="groww-btn-secondary" href="{_e(draft_url)}" target="_blank" rel="noopener">Open Drafts ↗</a>
  </div>
{card_close()}"""
    return f"""
{card_open("groww-link-card groww-muted")}
  <div class="groww-link-icon groww-icon-mail">✉️</div>
  <div class="groww-link-body"><h3>Gmail draft</h3><p>Not created yet</p></div>
{card_close()}"""


def pipeline_footer_strip(published_at: str | None) -> str:
    run = _e(published_at[:10] if published_at else "—")
    return f"""
<div class="groww-footer-strip">
  <span>🕐 Last pipeline run · {run}</span>
  <span class="groww-dot">·</span>
  <span>📅 GitHub Actions scheduled Mondays 06:00 UTC</span>
</div>"""


def section_label(text: str) -> str:
    return f'<p class="groww-section-label">{_e(text)}</p>'


def quote_block(text: str) -> str:
    return f"""
<div class="groww-quote-block">
  <p class="groww-quote-mark">“</p>
  <p class="groww-quote-text">{_e(text)}</p>
</div>"""


def numbered_theme(headline: str, index: int) -> str:
    return f"""
<div class="groww-num-item">
  <span class="groww-num-badge">{index}</span>
  <span class="groww-num-text">{_e(headline)}</span>
</div>"""


def phase_row(name: str, complete: bool, extra_link: str = "") -> str:
    icon = "✓" if complete else "○"
    cls = "groww-phase-done" if complete else "groww-phase-pending"
    link = f'<a class="groww-phase-link" href="{_e(extra_link)}" target="_blank" rel="noopener">View document ↗</a>' if extra_link else ""
    return f"""
<div class="groww-phase {cls}">
  <span class="groww-phase-icon">{icon}</span>
  <div><strong>{_e(name)}</strong>
    <span class="groww-phase-status">{"Complete" if complete else "Pending"}</span>{link}</div>
</div>"""
