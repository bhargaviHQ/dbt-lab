"""Generate dbt schema.yml test suggestions from model SQL using Claude."""

from __future__ import annotations

from pathlib import Path

from llm_client import call_claude

_PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "test_suggester.txt"


def suggest_tests(model_sql: str) -> str:
    """Return a schema.yml YAML block with recommended dbt tests for the given model SQL.

    Args:
        model_sql: Raw SQL text of a dbt model.

    Returns:
        A ready-to-paste schema.yml YAML string containing suggested dbt tests.
    """
    system_prompt = _PROMPT_PATH.read_text(encoding="utf-8")
    return call_claude(system_prompt=system_prompt, user_prompt=model_sql)
