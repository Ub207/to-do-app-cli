"""Task model definition."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

from .priority import Priority


@dataclass
class Task:
    """
    Represents a single todo task.

    Invariants:
    - id is immutable after creation
    - title is never empty after strip()
    - tags are always lowercase
    - created_at <= updated_at
    """
    id: str
    title: str
    description: str = ""
    completed: bool = False
    priority: Priority = Priority.NONE
    tags: list[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    due_date: Optional[str] = None
    recurring: Optional[str] = None

    def __post_init__(self) -> None:
        """Set timestamps if not provided."""
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

    @classmethod
    def create(cls, title: str, description: str = "") -> "Task":
        """
        Factory method to create a new task with generated ID and timestamps.

        Args:
            title: The task title (required)
            description: Optional task description

        Returns:
            A new Task instance
        """
        return cls(
            id=str(uuid.uuid4()),
            title=title.strip(),
            description=description.strip()
        )

    def to_dict(self) -> dict:
        """
        Convert task to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority.name.lower() if self.priority != Priority.NONE else None,
            "tags": self.tags.copy(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_date": self.due_date,
            "recurring": self.recurring
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        Create a Task from a dictionary (JSON deserialization).

        Args:
            data: Dictionary containing task data

        Returns:
            A new Task instance
        """
        priority_str = data.get("priority")
        if priority_str is None:
            priority = Priority.NONE
        else:
            priority = Priority[priority_str.upper()]

        return cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
            priority=priority,
            tags=data.get("tags", []),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            due_date=data.get("due_date"),
            recurring=data.get("recurring")
        )

    def mark_updated(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    @property
    def short_id(self) -> str:
        """Return first 8 characters of ID for display."""
        return self.id[:8]
