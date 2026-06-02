"""Shared Anthropic Claude API client utilities."""

from __future__ import annotations

import os

from anthropic import Anthropic

DEFAULT_MODEL = "claude-3-5-sonnet-latest"


def _get_api_key() -> str:
    """Return Anthropic API key from environment variables."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set.")
    return api_key


def call_claude(
    system_prompt: str,
    user_prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1200,
    temperature: float = 0.2,
) -> str:
    """Call Anthropic Claude and return plain text output."""
    client = Anthropic(api_key=_get_api_key())
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    chunks: list[str] = []
    for block in message.content:
        text = getattr(block, "text", None)
        if text:
            chunks.append(text)
    return "".join(chunks).strip()
