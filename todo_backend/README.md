# todo_backend (FastAPI)

FastAPI backend providing CRUD endpoints for Todo items persisted in SQLite.

## Endpoints

- `GET /todos` — list todos
- `POST /todos` — create todo
- `GET /todos/{id}` — get todo by id
- `PUT /todos/{id}` — update todo
- `DELETE /todos/{id}` — delete todo

Interactive docs are available at:

- `GET /docs`

## Database

This service uses a SQLite database file created by the `database` container.

Default path (per `fastapi-todo-service-202616-202621/database/db_connection.txt`):

`/home/kavia/workspace/code-generation/fastapi-todo-service-202616-202621/database/myapp.db`

You can override it with:

- `TODO_SQLITE_PATH` environment variable

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn todo_backend.main:app --host 0.0.0.0 --port 8000
```
