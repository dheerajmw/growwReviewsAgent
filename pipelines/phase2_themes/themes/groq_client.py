from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def load_dotenv(repo_root: Path | None = None) -> None:
    try:
        from dotenv import load_dotenv as _load
    except ImportError:
        return
    root = repo_root or Path(__file__).resolve().parents[3]
    env_path = root / ".env"
    if env_path.is_file():
        _load(env_path)


def groq_api_key() -> str:
    key = (os.environ.get("GROQ_API_KEY") or "").strip().strip('"').strip("'").replace("\r", "")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to .env or export it before running Phase 2."
        )
    return key


def chat_completion(
    *,
    system: str,
    user: str,
    model: str,
    temperature: float,
    max_tokens: int,
    max_retries: int = 5,
) -> tuple[str, int]:
    """Return (content, total_tokens). Retries on 429 with backoff."""
    import time

    try:
        from openai import OpenAI
        import openai
    except ImportError as e:
        raise RuntimeError("Install openai: pip install openai") from e

    client = OpenAI(api_key=groq_api_key(), base_url=GROQ_BASE_URL, max_retries=0)
    last_err: Exception | None = None

    for attempt in range(max_retries):
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = ""
            if resp.choices and resp.choices[0].message:
                content = (resp.choices[0].message.content or "").strip()
            tokens = 0
            if resp.usage:
                tokens = int((resp.usage.prompt_tokens or 0) + (resp.usage.completion_tokens or 0))
            return content, tokens
        except openai.RateLimitError as exc:
            last_err = exc
            wait = 35
            if getattr(exc, "response", None) is not None:
                retry_after = exc.response.headers.get("retry-after")
                if retry_after:
                    try:
                        wait = max(int(float(retry_after)), 10)
                    except ValueError:
                        pass
            wait += attempt * 5
            time.sleep(wait)
        except Exception as exc:
            last_err = exc
            if "429" in str(exc):
                time.sleep(35 + attempt * 5)
                continue
            raise

    raise RuntimeError(f"Groq rate limit persists after {max_retries} retries") from last_err


def parse_assignments_json(raw: str) -> list[dict[str, str]]:
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    data = json.loads(text)
    if isinstance(data, dict) and "assignments" in data:
        data = data["assignments"]
    if not isinstance(data, list):
        raise ValueError("Expected JSON array of assignments")
    out: list[dict[str, str]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        rid = item.get("review_id")
        theme = item.get("theme")
        if rid and theme:
            out.append({"review_id": str(rid), "theme": str(theme).lower().strip()})
    return out
