"""Suggest dbt tests for a dbt model definition."""

from __future__ import annotations


def suggest_tests(model_sql: str) -> str:
    """Return a placeholder dbt test suggestion response."""
    if not model_sql.strip():
        return "Please provide a dbt model."
    return "Test suggester is not implemented yet."
