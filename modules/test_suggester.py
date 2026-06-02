"""Generate dbt schema.yml test suggestions from model SQL using Claude."""

from __future__ import annotations

from pathlib import Path

from utils.llm_client import call_claude

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "test_suggester.txt"


def suggest_tests(model_sql: str) -> str:
    """Return a schema.yml YAML block with recommended dbt tests for the given model SQL."""
    cleaned_sql = model_sql.strip()
    if not cleaned_sql:
        return "# Please provide SQL input."

    try:
        return call_claude(
            system_prompt=PROMPT_FILE.read_text(encoding="utf-8").strip(),
            user_prompt=cleaned_sql,
        )
    except Exception as exc:  # noqa: BLE001
        return f"# Unable to generate tests due to an error: {exc}"
