from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


class McpServerError(RuntimeError):
    pass


def create_email_draft(
    base_url: str,
    *,
    to: str,
    subject: str,
    body: str,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """POST /create_email_draft on the deployed MCP server."""
    url = f"{base_url.rstrip('/')}/create_email_draft"
    payload = json.dumps({"to": to, "subject": subject, "body": body}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
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
