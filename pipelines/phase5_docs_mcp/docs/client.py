from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from typing import Any

logger = logging.getLogger(__name__)


class McpServerError(RuntimeError):
    pass


def health_check(base_url: str, timeout: float = 30.0) -> dict[str, Any]:
    url = f"{base_url.rstrip('/')}/"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_tools(base_url: str, timeout: float = 30.0) -> list[dict[str, Any]]:
    url = f"{base_url.rstrip('/')}/tools"
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if isinstance(data, list):
        return data
    return []


def append_to_doc(
    base_url: str,
    *,
    doc_id: str,
    content: str,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """POST /append_to_doc on the deployed MCP server."""
    url = f"{base_url.rstrip('/')}/append_to_doc"
    body = json.dumps({"doc_id": doc_id, "content": content}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise McpServerError(f"MCP server HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise McpServerError(f"Cannot reach MCP server at {base_url}: {e}") from e
