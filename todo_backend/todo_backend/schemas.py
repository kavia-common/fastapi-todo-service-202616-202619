"""Pydantic schemas for the Todo API."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TodoBase(BaseModel):
    """Shared fields for todo objects."""

    title: str = Field(..., min_length=1, max_length=255, description="Todo title")
    description: str | None = Field(
        default=None, description="Optional longer description"
    )
    completed: bool = Field(default=False, description="Whether the todo is completed")


class TodoCreate(TodoBase):
    """Request body for creating a todo."""


class TodoUpdate(BaseModel):
    """Request body for updating a todo.

    All fields are optional; only provided fields are updated.
    """

    title: str | None = Field(
        default=None, min_length=1, max_length=255, description="Todo title"
    )
    description: str | None = Field(
        default=None, description="Optional longer description"
    )
    completed: bool | None = Field(
        default=None, description="Whether the todo is completed"
    )

    model_config = ConfigDict(extra="forbid")


class TodoRead(TodoBase):
    """Response model for a todo."""

    id: int = Field(..., description="Unique todo id")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")

    model_config = ConfigDict(from_attributes=True)
