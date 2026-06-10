"""FastAPI Todo backend entrypoint."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from .db import _ENGINE, session_scope
from .migrations import ensure_todos_table
from .repository import create_todo, delete_todo, get_todo, list_todos, update_todo
from .schemas import TodoCreate, TodoRead, TodoUpdate

openapi_tags = [
    {
        "name": "todos",
        "description": "CRUD operations for todo items stored in SQLite.",
    },
    {
        "name": "meta",
        "description": "Service metadata and documentation helpers.",
    },
]

app = FastAPI(
    title="Todo Backend API",
    description=(
        "A minimal FastAPI service providing SQLite-backed CRUD endpoints for todos.\n\n"
        "Persistence uses the SQLite DB file created by the `database` container."
    ),
    version="0.1.0",
    openapi_tags=openapi_tags,
)


@app.on_event("startup")
def _startup() -> None:
    """Initialize database schema on startup (idempotent)."""
    ensure_todos_table(_ENGINE)


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["meta"],
    summary="Service health/info",
    description="Basic health check endpoint.",
    operation_id="get_root",
)
def root() -> dict[str, str]:
    """Return basic service status."""
    return {"status": "ok", "service": "todo_backend"}


# PUBLIC_INTERFACE
@app.get(
    "/todos",
    response_model=list[TodoRead],
    tags=["todos"],
    summary="List todos",
    description="Return all todos ordered by id ascending.",
    operation_id="list_todos",
)
def http_list_todos() -> list[TodoRead]:
    """List all todo items."""
    with session_scope() as db:
        return list_todos(db)


# PUBLIC_INTERFACE
@app.post(
    "/todos",
    response_model=TodoRead,
    status_code=201,
    tags=["todos"],
    summary="Create todo",
    description="Create a new todo item.",
    operation_id="create_todo",
)
def http_create_todo(payload: TodoCreate) -> TodoRead:
    """Create a todo item.

    Args:
        payload: Fields for the new todo.

    Returns:
        The newly created todo with server-generated fields (id, timestamps).
    """
    with session_scope() as db:
        todo = create_todo(db, payload)
        return todo


# PUBLIC_INTERFACE
@app.get(
    "/todos/{todo_id}",
    response_model=TodoRead,
    tags=["todos"],
    summary="Get todo",
    description="Retrieve a todo by its id.",
    operation_id="get_todo",
)
def http_get_todo(todo_id: int) -> TodoRead:
    """Get a single todo item by id."""
    with session_scope() as db:
        todo = get_todo(db, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo


# PUBLIC_INTERFACE
@app.put(
    "/todos/{todo_id}",
    response_model=TodoRead,
    tags=["todos"],
    summary="Update todo",
    description="Update an existing todo. Only provided fields are updated.",
    operation_id="update_todo",
)
def http_update_todo(todo_id: int, payload: TodoUpdate) -> TodoRead:
    """Update a todo by id."""
    with session_scope() as db:
        todo = get_todo(db, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return update_todo(db, todo, payload)


# PUBLIC_INTERFACE
@app.delete(
    "/todos/{todo_id}",
    tags=["todos"],
    summary="Delete todo",
    description="Delete a todo by id.",
    operation_id="delete_todo",
    responses={
        204: {"description": "Deleted"},
        404: {"description": "Todo not found"},
    },
)
def http_delete_todo(todo_id: int) -> JSONResponse:
    """Delete a todo by id.

    Returns:
        204 No Content on success.
    """
    with session_scope() as db:
        todo = get_todo(db, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        delete_todo(db, todo)
        return JSONResponse(status_code=204, content=None)
