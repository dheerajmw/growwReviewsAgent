from __future__ import annotations

import re
from pathlib import Path

from pipelines.phase2_themes.themes.groq_client import chat_completion, load_dotenv

from .config import REPO_ROOT, Phase4Config
from .gate import run_pii_gate


def redact_note_md(config: Phase4Config | None = None) -> Path:
    """LLM redaction pass on note.md; re-run gate. Raises if still failing."""
    cfg = config or Phase4Config.load()
    if not cfg.note_md_path.is_file():
        raise FileNotFoundError(cfg.note_md_path)

    load_dotenv(REPO_ROOT)
    original = cfg.note_md_path.read_text(encoding="utf-8")
    prompt_tpl = cfg.redact_prompt_path.read_text(encoding="utf-8")
    user = f"{prompt_tpl}\n\n---\n\n{original}"

    content, _tokens = chat_completion(
        system="You redact PII from executive markdown notes. Output markdown only.",
        user=user,
        model=cfg.redact_model,
        temperature=cfg.redact_temperature,
        max_tokens=cfg.redact_max_tokens,
    )
    cleaned = _strip_fences(content)
    cfg.note_md_path.write_text(cleaned, encoding="utf-8")
    return cfg.note_md_path


def _strip_fences(text: str) -> str:
    fence = re.search(r"```(?:markdown|md)?\s*([\s\S]*?)```", text.strip())
    if fence:
        return fence.group(1).strip() + "\n"
    return text.strip() + "\n"


def redact_and_validate(config: Phase4Config | None = None) -> bool:
    cfg = config or Phase4Config.load()
    redact_note_md(cfg)
    result = run_pii_gate(cfg.note_md_path, cfg, write_blockers_file=True)
    return result.passed
