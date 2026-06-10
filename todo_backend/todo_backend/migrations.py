"""Lightweight migration helpers.

Because this project uses SQLite and aims to stay minimal, we create missing tables
on startup (idempotent). This is compatible with the existing database container,
which already creates other tables in the same SQLite file.
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.engine import Engine


def ensure_todos_table(engine: Engine) -> None:
    """Ensure the `todos` table exists with the required columns.

    This is intentionally idempotent and uses CREATE TABLE IF NOT EXISTS.
    """
    # Note: storing timestamps as TEXT in SQLite is common; SQLAlchemy will
    # deserialize for us when mapped as DateTime if values are ISO strings.
    # Here we create as DATETIME with defaults using CURRENT_TIMESTAMP.
    ddl = """
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        completed BOOLEAN NOT NULL DEFAULT 0,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))

        # Helpful indexes for typical lookups/filters (optional but safe).
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_todos_completed ON todos(completed);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at);"))
