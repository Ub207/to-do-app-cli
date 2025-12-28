"""Task service - Business logic for task management (Phase I: In-Memory)."""

from datetime import datetime
from typing import Optional

from ..models.task import Task
from ..exceptions import ValidationError, TaskNotFoundError, AmbiguousIdError


class TaskService:
    """
    Service for managing tasks in memory.

    Phase I: Simple in-memory storage using a dictionary.
    No persistence, no file I/O, no database.

    Attributes:
        _tasks: Dictionary storing tasks (key: full UUID, value: Task)
    """

    def __init__(self) -> None:
        """Initialize task service with empty in-memory storage."""
        self._tasks: dict[str, Task] = {}

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task.

        Args:
            title: Task title (required, non-empty after strip)
            description: Optional task description

        Returns:
            Created Task with generated ID and timestamps

        Raises:
            ValidationError: If title is empty after stripping whitespace
        """
        title = title.strip()
        if not title:
            raise ValidationError("Title cannot be empty.")

        task = Task(
            title=title,
            description=description.strip()
        )
        self._tasks[task.id] = task
        return task

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks in creation order.

        Returns:
            List of all tasks (may be empty), sorted by created_at
        """
        tasks = list(self._tasks.values())
        tasks.sort(key=lambda t: t.created_at)
        return tasks

    def get_task(self, task_id: str) -> Task:
        """
        Get task by exact full ID.

        Args:
            task_id: Full UUID string

        Returns:
            Task if found

        Raises:
            TaskNotFoundError: If ID not found
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"No task found with ID '{task_id}'.")
        return self._tasks[task_id]

    def find_by_partial_id(self, partial: str) -> Task:
        """
        Find task by partial ID prefix (minimum 4 characters).

        Args:
            partial: At least 4 characters of task ID

        Returns:
            Task if exactly one match found

        Raises:
            TaskNotFoundError: No tasks match the partial ID
            AmbiguousIdError: Multiple tasks match the partial ID
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
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update task fields.

        Args:
            task_id: Full UUID string
            title: New title (None = keep current, must be non-empty if provided)
            description: New description (None = keep current, "" = clear)

        Returns:
            Updated Task

        Raises:
            TaskNotFoundError: If ID not found
            ValidationError: If new title is empty
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
        """
        Delete task by ID.

        Args:
            task_id: Full UUID string

        Raises:
            TaskNotFoundError: If ID not found
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"No task found with ID '{task_id}'.")
        del self._tasks[task_id]

    def toggle_complete(self, task_id: str) -> Task:
        """
        Toggle task completion status.

        Args:
            task_id: Full UUID string

        Returns:
            Updated Task with toggled status

        Raises:
            TaskNotFoundError: If ID not found
        """
        task = self.get_task(task_id)
        task.completed = not task.completed
        task.updated_at = datetime.now().isoformat()
        return task

    def get_task_count(self) -> tuple[int, int]:
        """
        Get task statistics.

        Returns:
            Tuple of (total_count, completed_count)
        """
        total = len(self._tasks)
        completed = sum(1 for task in self._tasks.values() if task.completed)
        return (total, completed)
