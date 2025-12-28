"""Task model definition - Phase I (In-Memory only)."""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Task:
    """
    Represents a single todo task.

    Phase I: In-memory only with basic fields.
    No priorities, tags, due dates, or persistence features.

    Attributes:
        id: Unique identifier (UUID v4)
        title: Task title (required, non-empty)
        description: Optional task description
        completed: Completion status (default: False)
        created_at: ISO 8601 timestamp of creation
        updated_at: ISO 8601 timestamp of last update
    """
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def short_id(self) -> str:
        """
        Return first 8 characters of UUID for display.

        Returns:
            str: Short ID (first 8 characters of UUID)
        """
        return self.id[:8]
