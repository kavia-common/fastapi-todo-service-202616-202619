"""Repository layer for Todo CRUD operations."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Todo
from .schemas import TodoCreate, TodoUpdate


def list_todos(db: Session) -> list[Todo]:
    """Return all todos ordered by id ascending."""
    stmt = select(Todo).order_by(Todo.id.asc())
    return list(db.execute(stmt).scalars().all())


def get_todo(db: Session, todo_id: int) -> Todo | None:
    """Return a todo by id or None if not found."""
    return db.get(Todo, todo_id)


def create_todo(db: Session, payload: TodoCreate) -> Todo:
    """Create and persist a new todo."""
    now = datetime.utcnow()
    todo = Todo(
        title=payload.title,
        description=payload.description,
        completed=payload.completed,
        created_at=now,
        updated_at=now,
    )
    db.add(todo)
    db.flush()  # Assign id
    return todo


def update_todo(db: Session, todo: Todo, payload: TodoUpdate) -> Todo:
    """Update an existing todo in-place and persist."""
    if payload.title is not None:
        todo.title = payload.title
    if payload.description is not None:
        todo.description = payload.description
    if payload.completed is not None:
        todo.completed = payload.completed

    todo.updated_at = datetime.utcnow()
    db.add(todo)
    db.flush()
    return todo


def delete_todo(db: Session, todo: Todo) -> None:
    """Delete a todo."""
    db.delete(todo)
    db.flush()
