"""Database wiring for the Todo backend.

Uses SQLite on-disk file shared with the `database` container.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

# This is the authoritative default path referenced by:
# fastapi-todo-service-202616-202621/database/db_connection.txt
_DEFAULT_SQLITE_PATH = (
    "/home/kavia/workspace/code-generation/"
    "fastapi-todo-service-202616-202621/database/myapp.db"
)


def _sqlite_url_from_path(sqlite_path: str) -> str:
    """Convert a filesystem path to a SQLAlchemy SQLite URL."""
    # SQLAlchemy expects 4 slashes for absolute paths: sqlite:////abs/path.db
    if os.path.isabs(sqlite_path):
        return f"sqlite:////{sqlite_path.lstrip('/')}"
    return f"sqlite:///{sqlite_path}"


def get_sqlite_path() -> str:
    """Return configured SQLite DB path (env override supported)."""
    return os.getenv("TODO_SQLITE_PATH", _DEFAULT_SQLITE_PATH)


def build_engine() -> Engine:
    """Create the SQLAlchemy engine for SQLite."""
    sqlite_path = get_sqlite_path()
    sqlite_url = _sqlite_url_from_path(sqlite_path)

    # check_same_thread=False allows usage with FastAPI's threaded concurrency.
    return create_engine(
        sqlite_url,
        connect_args={"check_same_thread": False},
        future=True,
    )


_ENGINE: Engine = build_engine()
_SessionLocal = sessionmaker(bind=_ENGINE, autocommit=False, autoflush=False, future=True)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Provide a transactional scope around a series of operations."""
    db = _SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
