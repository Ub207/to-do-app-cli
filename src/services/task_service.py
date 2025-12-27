"""Business logic for task operations."""

from typing import Optional

from src.models import Task, Priority
from src.exceptions import TaskNotFoundError, AmbiguousIdError, ValidationError
from src.utils.constants import (
    MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH, MIN_ID_LENGTH,
    MAX_TAGS_PER_TASK, MAX_TAG_LENGTH, TAG_PATTERN, MIN_SEARCH_LENGTH
)
from src.utils.date_utils import parse_date, is_overdue, is_due_today, is_due_this_week, calculate_next_due
import re
import uuid


class TaskService:
    """Handles all task-related business logic."""

    def __init__(self, storage: "StorageService") -> None:
        """
        Initialize task service.

        Args:
            storage: StorageService instance for persistence
        """
        self._storage = storage
        self._tasks: list[Task] = []
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load tasks from storage."""
        self._tasks = self._storage.load()

    def _save_tasks(self) -> bool:
        """Save tasks to storage."""
        return self._storage.save(self._tasks)

    # ==================== CRUD Operations ====================

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task.

        Args:
            title: Task title (required, max 200 chars)
            description: Task description (optional, max 2000 chars)

        Returns:
            The created Task

        Raises:
            ValidationError: If title is empty or too long
        """
        title = title.strip()
        description = description.strip()

        if not title:
            raise ValidationError("Title cannot be empty.")
        if len(title) > MAX_TITLE_LENGTH:
            raise ValidationError(f"Title must be {MAX_TITLE_LENGTH} characters or less.")
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValidationError(f"Description must be {MAX_DESCRIPTION_LENGTH} characters or less.")

        task = Task.create(title, description)
        self._tasks.append(task)
        self._save_tasks()
        return task

    def get_task(self, task_id: str) -> Task:
        """
        Get a task by full ID.

        Args:
            task_id: Full UUID of the task

        Returns:
            The Task if found

        Raises:
            TaskNotFoundError: If no task matches
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(f"No task found with ID '{task_id}'.")

    def find_by_partial_id(self, partial_id: str) -> Task:
        """
        Find a task by partial ID.

        Args:
            partial_id: First N characters of the task ID

        Returns:
            The matching Task

        Raises:
            ValidationError: If partial_id is too short
            TaskNotFoundError: If no task matches
            AmbiguousIdError: If multiple tasks match
        """
        partial_id = partial_id.strip().lower()

        if len(partial_id) < MIN_ID_LENGTH:
            raise ValidationError(f"Task ID must be at least {MIN_ID_LENGTH} characters.")

        matches = [t for t in self._tasks if t.id.lower().startswith(partial_id)]

        if len(matches) == 0:
            raise TaskNotFoundError(f"No task found matching '{partial_id}'.")
        if len(matches) > 1:
            raise AmbiguousIdError(f"Multiple tasks match '{partial_id}'. Please be more specific.")

        return matches[0]

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks.

        Returns:
            List of all tasks (newest first)
        """
        return sorted(self._tasks, key=lambda t: t.created_at, reverse=True)

    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update a task's title and/or description.

        Args:
            task_id: Full or partial task ID
            title: New title (None to keep current)
            description: New description (None to keep current, "" to clear)

        Returns:
            The updated Task
        """
        task = self.find_by_partial_id(task_id)

        if title is not None:
            title = title.strip()
            if not title:
                raise ValidationError("Title cannot be empty.")
            if len(title) > MAX_TITLE_LENGTH:
                raise ValidationError(f"Title must be {MAX_TITLE_LENGTH} characters or less.")
            task.title = title

        if description is not None:
            description = description.strip() if description != "" else ""
            if len(description) > MAX_DESCRIPTION_LENGTH:
                raise ValidationError(f"Description must be {MAX_DESCRIPTION_LENGTH} characters or less.")
            task.description = description

        task.mark_updated()
        self._save_tasks()
        return task

    def delete_task(self, task_id: str) -> Task:
        """
        Delete a task.

        Args:
            task_id: Full or partial task ID

        Returns:
            The deleted Task (for confirmation message)
        """
        task = self.find_by_partial_id(task_id)
        self._tasks.remove(task)
        self._save_tasks()
        return task

    def toggle_complete(self, task_id: str) -> tuple[Task, Optional[Task]]:
        """
        Toggle a task's completed status.

        Args:
            task_id: Full or partial task ID

        Returns:
            Tuple of (updated Task, new recurring Task or None)
        """
        task = self.find_by_partial_id(task_id)
        was_incomplete = not task.completed
        task.completed = not task.completed
        task.mark_updated()

        new_task = None
        if was_incomplete and task.completed and task.recurring:
            new_task = self.handle_recurring_completion(task)
        else:
            self._save_tasks()

        return task, new_task

    def get_task_count(self) -> tuple[int, int]:
        """
        Get total and completed task counts.

        Returns:
            Tuple of (total_count, completed_count)
        """
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.completed)
        return total, completed

    # ==================== Priority Operations ====================

    def set_priority(self, task_id: str, priority: Priority) -> Task:
        """Set a task's priority."""
        task = self.find_by_partial_id(task_id)
        task.priority = priority
        task.mark_updated()
        self._save_tasks()
        return task

    # ==================== Tag Operations ====================

    def add_tag(self, task_id: str, tag: str) -> Task:
        """Add a tag to a task."""
        task = self.find_by_partial_id(task_id)
        tag = tag.strip().lower()

        if not tag:
            raise ValidationError("Tag cannot be empty.")
        if len(tag) > MAX_TAG_LENGTH:
            raise ValidationError(f"Tag must be {MAX_TAG_LENGTH} characters or less.")
        if not re.match(TAG_PATTERN, tag):
            raise ValidationError("Tags can only contain lowercase letters, numbers, and hyphens.")
        if len(task.tags) >= MAX_TAGS_PER_TASK:
            raise ValidationError(f"Maximum {MAX_TAGS_PER_TASK} tags per task.")
        if tag in task.tags:
            raise ValidationError(f"Tag '{tag}' already exists on this task.")

        task.tags.append(tag)
        task.mark_updated()
        self._save_tasks()
        return task

    def remove_tag(self, task_id: str, tag: str) -> Task:
        """Remove a tag from a task."""
        task = self.find_by_partial_id(task_id)
        tag = tag.lower()

        if tag not in task.tags:
            raise ValidationError(f"Tag '{tag}' not found on this task.")

        task.tags.remove(tag)
        task.mark_updated()
        self._save_tasks()
        return task

    def get_all_tags(self) -> list[str]:
        """Get all unique tags across all tasks."""
        tags = set()
        for task in self._tasks:
            tags.update(task.tags)
        return sorted(tags)

    # ==================== Search & Filter ====================

    def search(self, query: str) -> list[Task]:
        """Search tasks by title, description, or tags."""
        query = query.strip()
        if len(query) < MIN_SEARCH_LENGTH:
            raise ValidationError(f"Search query must be at least {MIN_SEARCH_LENGTH} characters.")

        query_lower = query.lower()
        results = []

        for task in self._tasks:
            if query_lower in task.title.lower():
                results.append((task, 1))
            elif query_lower in task.description.lower():
                results.append((task, 2))
            elif any(query_lower in tag for tag in task.tags):
                results.append((task, 3))

        results.sort(key=lambda x: (x[1], x[0].created_at), reverse=False)
        return [task for task, _ in results]

    def filter_by_status(self, completed: bool) -> list[Task]:
        """Filter tasks by completion status."""
        return [t for t in self._tasks if t.completed == completed]

    def filter_by_priority(self, priority: Priority) -> list[Task]:
        """Filter tasks by priority."""
        return [t for t in self._tasks if t.priority == priority]

    def filter_by_tag(self, tag: str) -> list[Task]:
        """Filter tasks by tag."""
        tag = tag.lower()
        return [t for t in self._tasks if tag in t.tags]

    # ==================== Sort ====================

    def sort_tasks(self, tasks: list[Task], sort_key: str, reverse: bool = False) -> list[Task]:
        """Sort a list of tasks."""
        sort_functions = {
            "priority": lambda t: (-t.priority.value, t.title.lower()),
            "priority_asc": lambda t: (t.priority.value, t.title.lower()),
            "due_date": lambda t: (t.due_date or "9999-99-99", t.title.lower()),
            "title": lambda t: t.title.lower(),
            "created": lambda t: t.created_at,
        }
        if sort_key not in sort_functions:
            return tasks
        return sorted(tasks, key=sort_functions[sort_key], reverse=reverse)

    # ==================== Due Date Operations ====================

    def set_due_date(self, task_id: str, due_date: str) -> Task:
        """Set a task's due date."""
        task = self.find_by_partial_id(task_id)
        try:
            parse_date(due_date)
        except ValueError:
            raise ValidationError("Date must be in YYYY-MM-DD format.")
        task.due_date = due_date
        task.mark_updated()
        self._save_tasks()
        return task

    def clear_due_date(self, task_id: str) -> Task:
        """Clear a task's due date and recurring."""
        task = self.find_by_partial_id(task_id)
        task.due_date = None
        task.recurring = None
        task.mark_updated()
        self._save_tasks()
        return task

    def get_overdue(self) -> list[Task]:
        """Get all overdue incomplete tasks."""
        return [t for t in self._tasks if is_overdue(t.due_date) and not t.completed]

    def get_due_today(self) -> list[Task]:
        """Get all tasks due today."""
        return [t for t in self._tasks if is_due_today(t.due_date) and not t.completed]

    def get_due_this_week(self) -> list[Task]:
        """Get all tasks due in the next 7 days."""
        tasks = [t for t in self._tasks if is_due_this_week(t.due_date) and not t.completed]
        return sorted(tasks, key=lambda t: t.due_date)

    # ==================== Recurring Operations ====================

    def set_recurring(self, task_id: str, pattern: Optional[str]) -> Task:
        """Set a task's recurrence pattern."""
        task = self.find_by_partial_id(task_id)
        if pattern and not task.due_date:
            raise ValidationError("Task must have a due date before setting recurrence.")
        if pattern and pattern not in ["daily", "weekly", "monthly"]:
            raise ValidationError("Recurrence must be daily, weekly, or monthly.")
        task.recurring = pattern
        task.mark_updated()
        self._save_tasks()
        return task

    def handle_recurring_completion(self, task: Task) -> Optional[Task]:
        """Create new task instance when recurring task is completed."""
        if not task.recurring or not task.due_date:
            return None

        new_due = calculate_next_due(task.due_date, task.recurring)
        new_task = Task(
            id=str(uuid.uuid4()),
            title=task.title,
            description=task.description,
            completed=False,
            priority=task.priority,
            tags=task.tags.copy(),
            due_date=new_due,
            recurring=task.recurring
        )
        self._tasks.append(new_task)
        self._save_tasks()
        return new_task
