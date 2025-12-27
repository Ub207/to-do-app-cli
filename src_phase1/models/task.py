"""Task data model."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique identifier (UUID v4 string).
        title: Task title (required, non-empty).
        description: Task description (optional).
        completed: Whether the task is completed.
        created_at: ISO 8601 timestamp of creation.
        updated_at: ISO 8601 timestamp of last update.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def short_id(self) -> str:
        """Return first 8 characters of UUID for display."""
        return self.id[:8]
