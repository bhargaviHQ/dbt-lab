"""Refactor SQL using dbt best-practice suggestions."""

from __future__ import annotations


def refactor_sql(raw_sql: str) -> str:
    """Return a placeholder SQL refactor response."""
    if not raw_sql.strip():
        return "Please provide SQL."
    return "SQL refactor tool is not implemented yet."
