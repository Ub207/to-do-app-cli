"""Task service with in-memory storage."""

from datetime import datetime

from src_phase1.models import Task
from src_phase1.exceptions import (
    TaskNotFoundError,
    AmbiguousIdError,
    ValidationError,
)


class TaskService:
    """Service for managing tasks in memory."""

    def __init__(self) -> None:
        """Initialize with empty task storage."""
        self._tasks: dict[str, Task] = {}

    def add_task(self, title: str, description: str = "") -> Task:
        """Create a new task.

        Args:
            title: Task title (required, non-empty).
            description: Task description (optional).

        Returns:
            Created Task with generated ID.

        Raises:
            ValidationError: If title is empty.
        """
        title = title.strip()
        if not title:
            raise ValidationError("Title cannot be empty.")

        task = Task(title=title, description=description.strip())
        self._tasks[task.id] = task
        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks in creation order.

        Returns:
            List of all tasks (may be empty).
        """
        return list(self._tasks.values())

    def get_task(self, task_id: str) -> Task:
        """Get task by exact ID.

        Args:
            task_id: Full UUID string.

        Returns:
            Task if found.

        Raises:
            TaskNotFoundError: If ID not found.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"No task found with ID '{task_id}'.")
        return self._tasks[task_id]

    def find_by_partial_id(self, partial: str) -> Task:
        """Find task by partial ID prefix.

        Args:
            partial: At least 4 characters of task ID.

        Returns:
            Task if exactly one match.

        Raises:
            TaskNotFoundError: No matches.
            AmbiguousIdError: Multiple matches.
        """
        matches = [
            task for task in self._tasks.values()
            if task.id.startswith(partial)
        ]

        if len(matches) == 0:
            raise TaskNotFoundError(f"No task found with ID '{partial}'.")
        if len(matches) > 1:
            raise AmbiguousIdError(
                f"Multiple tasks match '{partial}'. Please use more characters."
            )
        return matches[0]

    def update_task(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None
    ) -> Task:
        """Update task fields.

        Args:
            task_id: Full UUID string.
            title: New title (None = keep current).
            description: New description (None = keep, "" = clear).

        Returns:
            Updated Task.

        Raises:
            TaskNotFoundError: If ID not found.
            ValidationError: If new title is empty.
        """
        task = self.get_task(task_id)

        if title is not None:
            title = title.strip()
            if not title:
                raise ValidationError("Title cannot be empty.")
            task.title = title

        if description is not None:
            task.description = description.strip()

        task.updated_at = datetime.now().isoformat()
        return task

    def delete_task(self, task_id: str) -> None:
        """Delete task by ID.

        Args:
            task_id: Full UUID string.

        Raises:
            TaskNotFoundError: If ID not found.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"No task found with ID '{task_id}'.")
        del self._tasks[task_id]

    def toggle_complete(self, task_id: str) -> Task:
        """Toggle task completion status.

        Args:
            task_id: Full UUID string.

        Returns:
            Updated Task with toggled status.

        Raises:
            TaskNotFoundError: If ID not found.
        """
        task = self.get_task(task_id)
        task.completed = not task.completed
        task.updated_at = datetime.now().isoformat()
        return task

    def get_task_count(self) -> tuple[int, int]:
        """Get task counts.

        Returns:
            Tuple of (total_count, completed_count).
        """
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks.values() if t.completed)
        return total, completed
