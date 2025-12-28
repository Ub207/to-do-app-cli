"""Pydantic schemas for request/response validation."""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field("", max_length=2000, description="Task description")


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)


class TaskToggle(BaseModel):
    """Schema for toggling task completion."""
    completed: bool


class PriorityUpdate(BaseModel):
    """Schema for updating task priority."""
    priority: Optional[str] = Field(None, pattern="^(HIGH|MEDIUM|LOW)$")


class TagAdd(BaseModel):
    """Schema for adding a tag."""
    tag: str = Field(..., min_length=1, max_length=50, pattern="^[a-z0-9-]+$")


class TagRemove(BaseModel):
    """Schema for removing a tag."""
    tag: str


class DueDateUpdate(BaseModel):
    """Schema for updating due date."""
    due_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")


class RecurringUpdate(BaseModel):
    """Schema for updating recurring pattern."""
    recurring: Optional[str] = Field(None, pattern="^(daily|weekly|monthly)$")


class TaskResponse(BaseModel):
    """Schema for task response."""
    id: str
    title: str
    description: str
    completed: bool
    priority: Optional[str]
    tags: List[str]
    due_date: Optional[str]
    recurring: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for task list response."""
    total: int
    completed: int
    tasks: List[TaskResponse]


class ErrorResponse(BaseModel):
    """Schema for error response."""
    error: str
    detail: Optional[str] = None
