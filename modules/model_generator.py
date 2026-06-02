"""Generate dbt model artifacts from raw SQL."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from utils.llm_client import call_claude

PROMPT_FILE = Path(__file__).resolve().parent.parent / "prompts" / "model_generator.txt"
TABLE_PATTERN = re.compile(
    r"\b(?:from|join)\s+([\w\-.]+)",
    flags=re.IGNORECASE,
)
JSON_BLOCK_PATTERN = re.compile(r"\{.*\}", flags=re.DOTALL)


def _load_prompt() -> str:
    """Load the system prompt used for model generation."""
    return PROMPT_FILE.read_text(encoding="utf-8").strip()


def _extract_raw_tables(raw_sql: str) -> list[str]:
    """Extract potential raw table references from SQL text."""
    tables = []
    for match in TABLE_PATTERN.findall(raw_sql):
        table_name = match.strip().strip('"`')
        if "{{" in table_name or "ref(" in table_name:
            continue
        if table_name not in tables:
            tables.append(table_name)
    return tables


def _build_user_prompt(raw_sql: str, raw_tables: list[str]) -> str:
    """Build the user prompt payload for the LLM call."""
    tables_text = ", ".join(raw_tables) if raw_tables else "none_detected"
    return (
        "Input SQL:\n"
        f"{raw_sql}\n\n"
        "Detected raw tables:\n"
        f"{tables_text}\n\n"
        "Return JSON only with keys: model_sql, schema_yml, sources_yml."
    )


def _extract_json_payload(text: str) -> dict[str, Any]:
    """Extract and parse JSON payload from an LLM response."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = JSON_BLOCK_PATTERN.search(text)
        if not match:
            raise ValueError("Model generator response was not valid JSON.")
        return json.loads(match.group(0))


def _default_sources_yml(raw_tables: list[str]) -> str:
    """Generate a default sources.yml when raw tables are detected."""
    if not raw_tables:
        return "# No raw source tables detected"

    table_entries = "\n".join(
        f"      - name: {table.split('.')[-1]}\n        description: Source table {table}"
        for table in raw_tables
    )
    return (
        "version: 2\n"
        "sources:\n"
        "  - name: raw\n"
        "    schema: raw\n"
        "    tables:\n"
        f"{table_entries}\n"
    )


def generate_model_artifacts(raw_sql: str) -> dict[str, str]:
    """Generate model.sql, schema.yml, and sources.yml from raw SQL input."""
    cleaned_sql = raw_sql.strip()
    if not cleaned_sql:
        return {
            "model_sql": "-- Please provide SQL input.",
            "schema_yml": "# Please provide SQL input.",
            "sources_yml": "# Please provide SQL input.",
        }

    raw_tables = _extract_raw_tables(cleaned_sql)

    try:
        response_text = call_claude(
            system_prompt=_load_prompt(),
            user_prompt=_build_user_prompt(cleaned_sql, raw_tables),
        )
        payload = _extract_json_payload(response_text)
        model_sql = payload.get("model_sql", "-- No model_sql returned").strip()
        schema_yml = payload.get("schema_yml", "# No schema_yml returned").strip()
        sources_yml = payload.get("sources_yml", "").strip() or _default_sources_yml(raw_tables)
    except Exception as exc:  # noqa: BLE001
        return {
            "model_sql": f"-- Error generating dbt model: {exc}",
            "schema_yml": "# Unable to generate schema.yml due to an error.",
            "sources_yml": _default_sources_yml(raw_tables),
        }

    return {
        "model_sql": model_sql,
        "schema_yml": schema_yml,
        "sources_yml": sources_yml,
    }
