"""Thin LLM client wrapper for Claude requests."""

from __future__ import annotations

import os


try:
    from anthropic import Anthropic
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "anthropic package is required. Install with `pip install anthropic`."
    ) from exc


def call_claude(*, system_prompt: str, user_prompt: str, max_tokens: int = 1200) -> str:
    """Send a prompt to Claude and return the response text."""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest"),
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return "".join(block.text for block in response.content if getattr(block, "text", None)).strip()
