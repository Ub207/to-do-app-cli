# Implementation Plan: Console Todo App

> **Spec-Kit-Plus Implementation Roadmap**
> A phased, incremental approach to building a reliable CLI todo application.
> Each phase is testable and delivers working functionality.

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Development Phases Overview](#2-development-phases-overview)
3. [Phase 1: Foundation](#3-phase-1-foundation)
4. [Phase 2: Basic Features (MVP)](#4-phase-2-basic-features-mvp)
5. [Phase 3: Persistence & Robustness](#5-phase-3-persistence--robustness)
6. [Phase 4: Intermediate Features](#6-phase-4-intermediate-features)
7. [Phase 5: Advanced Features](#7-phase-5-advanced-features)
8. [Phase 6: Polish & Testing](#8-phase-6-polish--testing)
9. [Risk Mitigation](#9-risk-mitigation)
10. [Quick Reference](#10-quick-reference)

---

## 1. Project Structure

### 1.1 Directory Layout

```
to-do-app/
├── main.py                      # Entry point (< 50 lines)
├── constitution.md              # Project governance rules (exists)
├── .specify                     # Specification file (exists)
├── IMPLEMENTATION_PLAN.md       # This file
├── README.md                    # User documentation
│
├── src/
│   ├── __init__.py              # Package marker
│   ├── app.py                   # Application orchestrator
│   │
│   ├── models/
│   │   ├── __init__.py          # Exports: Task, Priority
│   │   ├── task.py              # Task dataclass
│   │   └── priority.py          # Priority enum
│   │
│   ├── services/
│   │   ├── __init__.py          # Exports: TaskService, StorageService
│   │   ├── task_service.py      # Business logic
│   │   └── storage_service.py   # JSON persistence
│   │
│   ├── ui/
│   │   ├── __init__.py          # Exports: Menu, Display, InputHandler
│   │   ├── menu.py              # Menu display and routing
│   │   ├── display.py           # Output formatting
│   │   └── input_handler.py     # Input prompts and validation
│   │
│   ├── utils/
│   │   ├── __init__.py          # Exports: validators, date_utils, constants
│   │   ├── constants.py         # All magic values
│   │   ├── validators.py        # Validation functions
│   │   └── date_utils.py        # Date parsing/formatting
│   │
│   └── exceptions.py            # Custom exceptions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── test_task.py
│   ├── test_priority.py
│   ├── test_task_service.py
│   ├── test_storage_service.py
│   ├── test_validators.py
│   ├── test_date_utils.py
│   └── test_integration.py
│
└── data/
    ├── .gitkeep                 # Ensure directory in repo
    └── tasks.json               # Created at runtime
```

### 1.2 File Creation Order

Files should be created in this exact order to manage dependencies:

```
Phase 1:
  1. src/__init__.py
  2. src/utils/__init__.py
  3. src/utils/constants.py
  4. src/exceptions.py
  5. src/models/__init__.py
  6. src/models/priority.py
  7. src/models/task.py
  8. tests/__init__.py
  9. tests/conftest.py
  10. tests/test_priority.py
  11. tests/test_task.py

Phase 2:
  12. src/services/__init__.py
  13. src/services/storage_service.py
  14. src/services/task_service.py
  15. src/ui/__init__.py
  16. src/ui/display.py
  17. src/ui/input_handler.py
  18. src/ui/menu.py
  19. src/app.py
  20. main.py
  21. tests/test_storage_service.py
  22. tests/test_task_service.py

Phase 3+:
  23. src/utils/validators.py
  24. src/utils/date_utils.py
  25. tests/test_validators.py
  26. tests/test_date_utils.py
  27. tests/test_integration.py
  28. README.md
```

---

## 2. Development Phases Overview

| Phase | Name | Duration | Deliverable | Gate Criteria |
|-------|------|----------|-------------|---------------|
| 1 | Foundation | 1-2 hours | Core models, constants, exceptions | Unit tests pass |
| 2 | Basic Features | 2-3 hours | Working MVP (add, list, view, update, delete, toggle) | Manual test all 6 options |
| 3 | Persistence | 1-2 hours | Reliable JSON storage, error recovery | Restart app, data persists |
| 4 | Intermediate | 2-3 hours | Priority, tags, search, filter, sort | All Level 2 tests pass |
| 5 | Advanced | 2-3 hours | Due dates, recurring, reminders | All Level 3 tests pass |
| 6 | Polish | 1-2 hours | Documentation, cleanup, final tests | 85%+ coverage |

**Total Estimated Time: 9-15 hours**

---

## 3. Phase 1: Foundation

### 3.1 Objective

Create the foundational data structures, constants, and exceptions that all other code depends on.

### 3.2 Files to Create

#### 3.2.1 `src/__init__.py`

```python
"""Console Todo App - Main Package."""

__version__ = "1.0.0"
```

#### 3.2.2 `src/utils/__init__.py`

```python
"""Utility modules."""

from .constants import *
```

#### 3.2.3 `src/utils/constants.py`

```python
"""Application constants and configuration."""

from pathlib import Path

# Version
APP_VERSION = "1.0.0"
DATA_VERSION = "1.0.0"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DATA_FILE = DATA_DIR / "tasks.json"
BACKUP_SUFFIX = ".backup"
TEMP_SUFFIX = ".tmp"

# Validation Limits
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000
MAX_TAGS_PER_TASK = 10
MAX_TAG_LENGTH = 50
MIN_SEARCH_LENGTH = 2
MIN_ID_LENGTH = 4

# Display
SHORT_ID_LENGTH = 8
TITLE_DISPLAY_LENGTH = 35
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DISPLAY_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Exit Codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1

# Validation Patterns
TAG_PATTERN = r"^[a-z0-9][a-z0-9-]{0,49}$"

# Menu Options by Level
LEVEL_1_OPTIONS = {0, 1, 2, 3, 4, 5, 6}
LEVEL_2_OPTIONS = LEVEL_1_OPTIONS | {7, 8, 9, 10, 11, 12}
LEVEL_3_OPTIONS = LEVEL_2_OPTIONS | {13, 14, 15, 16, 17, 18}
```

#### 3.2.4 `src/exceptions.py`

```python
"""Custom exception classes for the Todo App."""


class TodoAppError(Exception):
    """Base exception for all application errors."""
    pass


class ValidationError(TodoAppError):
    """Raised when user input fails validation."""
    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task ID doesn't match any task."""
    pass


class AmbiguousIdError(TodoAppError):
    """Raised when a partial task ID matches multiple tasks."""
    pass


class StorageError(TodoAppError):
    """Raised when file operations fail."""
    pass
```

#### 3.2.5 `src/models/__init__.py`

```python
"""Data models."""

from .priority import Priority
from .task import Task

__all__ = ["Priority", "Task"]
```

#### 3.2.6 `src/models/priority.py`

```python
"""Priority enumeration for tasks."""

from enum import Enum


class Priority(Enum):
    """
    Task priority levels.

    Ordered for comparison: NONE < LOW < MEDIUM < HIGH
    """
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def display_short(self) -> str:
        """Return short display string for list view."""
        mapping = {
            Priority.NONE: "-",
            Priority.LOW: "LOW",
            Priority.MEDIUM: "MED",
            Priority.HIGH: "HIGH"
        }
        return mapping[self]

    def display_full(self) -> str:
        """Return full display string for detail view."""
        mapping = {
            Priority.NONE: "None",
            Priority.LOW: "Low",
            Priority.MEDIUM: "Medium",
            Priority.HIGH: "High"
        }
        return mapping[self]
```

#### 3.2.7 `src/models/task.py`

```python
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
```

### 3.3 Tests to Create

#### `tests/conftest.py`

```python
"""Shared test fixtures."""

import pytest
from src.models import Task, Priority


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task for testing."""
    return Task.create("Test Task", "Test Description")


@pytest.fixture
def completed_task() -> Task:
    """Create a completed task for testing."""
    task = Task.create("Completed Task")
    task.completed = True
    task.mark_updated()
    return task
```

#### `tests/test_priority.py`

```python
"""Tests for Priority enum."""

import unittest
from src.models import Priority


class TestPriority(unittest.TestCase):
    """Test Priority enumeration."""

    def test_priority_values_ordered(self):
        """Priority values should be ordered NONE < LOW < MEDIUM < HIGH."""
        self.assertLess(Priority.NONE.value, Priority.LOW.value)
        self.assertLess(Priority.LOW.value, Priority.MEDIUM.value)
        self.assertLess(Priority.MEDIUM.value, Priority.HIGH.value)

    def test_display_short(self):
        """Short display strings should be correct."""
        self.assertEqual(Priority.NONE.display_short(), "-")
        self.assertEqual(Priority.LOW.display_short(), "LOW")
        self.assertEqual(Priority.MEDIUM.display_short(), "MED")
        self.assertEqual(Priority.HIGH.display_short(), "HIGH")

    def test_display_full(self):
        """Full display strings should be correct."""
        self.assertEqual(Priority.NONE.display_full(), "None")
        self.assertEqual(Priority.LOW.display_full(), "Low")
        self.assertEqual(Priority.MEDIUM.display_full(), "Medium")
        self.assertEqual(Priority.HIGH.display_full(), "High")


if __name__ == "__main__":
    unittest.main()
```

#### `tests/test_task.py`

```python
"""Tests for Task model."""

import unittest
import time
from src.models import Task, Priority


class TestTask(unittest.TestCase):
    """Test Task dataclass."""

    def test_create_with_title_only(self):
        """Task can be created with just title."""
        task = Task.create("Buy milk")

        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, Priority.NONE)
        self.assertEqual(task.tags, [])
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.recurring)
        self.assertEqual(len(task.id), 36)  # UUID format
        self.assertNotEqual(task.created_at, "")
        self.assertNotEqual(task.updated_at, "")

    def test_create_with_description(self):
        """Task can be created with title and description."""
        task = Task.create("Buy groceries", "Milk, eggs, bread")

        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, eggs, bread")

    def test_create_strips_whitespace(self):
        """Title and description should be stripped of whitespace."""
        task = Task.create("  Buy milk  ", "  Get 2%  ")

        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.description, "Get 2%")

    def test_short_id_returns_first_8_chars(self):
        """short_id property returns first 8 characters."""
        task = Task.create("Test")

        self.assertEqual(len(task.short_id), 8)
        self.assertTrue(task.id.startswith(task.short_id))

    def test_mark_updated_changes_timestamp(self):
        """mark_updated() should update the updated_at field."""
        task = Task.create("Test")
        old_updated = task.updated_at

        time.sleep(0.01)  # Small delay to ensure different timestamp
        task.mark_updated()

        self.assertGreater(task.updated_at, old_updated)

    def test_to_dict_serialization(self):
        """to_dict() should serialize all fields correctly."""
        task = Task.create("Test", "Description")
        task.priority = Priority.HIGH
        task.tags = ["work", "urgent"]
        task.completed = True

        data = task.to_dict()

        self.assertEqual(data["id"], task.id)
        self.assertEqual(data["title"], "Test")
        self.assertEqual(data["description"], "Description")
        self.assertTrue(data["completed"])
        self.assertEqual(data["priority"], "high")
        self.assertEqual(data["tags"], ["work", "urgent"])

    def test_from_dict_deserialization(self):
        """from_dict() should deserialize all fields correctly."""
        data = {
            "id": "test-uuid-1234",
            "title": "Test Task",
            "description": "Test Description",
            "completed": True,
            "priority": "medium",
            "tags": ["work"],
            "created_at": "2024-01-15T09:00:00",
            "updated_at": "2024-01-15T10:00:00",
            "due_date": "2024-01-20",
            "recurring": "weekly"
        }

        task = Task.from_dict(data)

        self.assertEqual(task.id, "test-uuid-1234")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, Priority.MEDIUM)
        self.assertEqual(task.due_date, "2024-01-20")
        self.assertEqual(task.recurring, "weekly")

    def test_to_dict_from_dict_roundtrip(self):
        """Serialization should be reversible."""
        original = Task.create("Test", "Description")
        original.priority = Priority.HIGH
        original.tags = ["work", "urgent"]

        data = original.to_dict()
        restored = Task.from_dict(data)

        self.assertEqual(restored.id, original.id)
        self.assertEqual(restored.title, original.title)
        self.assertEqual(restored.description, original.description)
        self.assertEqual(restored.priority, original.priority)
        self.assertEqual(restored.tags, original.tags)

    def test_priority_none_serializes_as_null(self):
        """Priority.NONE should serialize as None/null."""
        task = Task.create("Test")
        data = task.to_dict()

        self.assertIsNone(data["priority"])

    def test_from_dict_handles_missing_optional_fields(self):
        """from_dict() should handle missing optional fields gracefully."""
        data = {
            "id": "test-uuid",
            "title": "Test",
            "created_at": "2024-01-15T09:00:00",
            "updated_at": "2024-01-15T09:00:00"
        }

        task = Task.from_dict(data)

        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, Priority.NONE)
        self.assertEqual(task.tags, [])


if __name__ == "__main__":
    unittest.main()
```

### 3.4 Manual Testing

After Phase 1, run:

```bash
# Run all tests
python -m pytest tests/ -v

# Or with unittest
python -m unittest discover tests/ -v
```

**Expected Result:** All tests pass.

### 3.5 Phase 1 Completion Checklist

- [ ] All files created in `src/utils/`, `src/models/`, `src/exceptions.py`
- [ ] `tests/test_priority.py` passes
- [ ] `tests/test_task.py` passes
- [ ] No import errors when running `python -c "from src.models import Task, Priority"`

---

## 4. Phase 2: Basic Features (MVP)

### 4.1 Objective

Implement the core CRUD operations with a working menu system.

### 4.2 Files to Create

#### 4.2.1 `src/services/__init__.py`

```python
"""Service layer."""

from .storage_service import StorageService
from .task_service import TaskService

__all__ = ["StorageService", "TaskService"]
```

#### 4.2.2 `src/services/storage_service.py`

```python
"""JSON file storage service."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.models import Task
from src.exceptions import StorageError
from src.utils.constants import (
    DATA_DIR, DEFAULT_DATA_FILE, BACKUP_SUFFIX, TEMP_SUFFIX, DATA_VERSION
)


class StorageService:
    """Handles JSON file persistence for tasks."""

    def __init__(self, file_path: Optional[Path] = None) -> None:
        """
        Initialize storage service.

        Args:
            file_path: Path to JSON file. Defaults to data/tasks.json
        """
        self.file_path = file_path or DEFAULT_DATA_FILE
        self.backup_path = Path(str(self.file_path) + BACKUP_SUFFIX)
        self.temp_path = Path(str(self.file_path) + TEMP_SUFFIX)
        self._memory_only_mode = False

    def load(self) -> list[Task]:
        """
        Load tasks from JSON file.

        Returns:
            List of Task objects
        """
        # Ensure data directory exists
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents=True)
            print("Created data directory.")

        # If file doesn't exist, create empty
        if not self.file_path.exists():
            self._create_empty_file()
            print("Created new task list.")
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate structure
            if "tasks" not in data:
                raise KeyError("Missing 'tasks' key")

            tasks = [Task.from_dict(t) for t in data["tasks"]]
            return tasks

        except (json.JSONDecodeError, KeyError) as e:
            # Backup corrupted file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            corrupted_path = Path(f"{self.file_path}.corrupted.{timestamp}")
            shutil.copy2(self.file_path, corrupted_path)

            print(f"Warning: Task file was corrupted. Starting fresh.")
            print(f"Corrupted file backed up to: {corrupted_path.name}")

            self._create_empty_file()
            return []

        except PermissionError:
            print("Error: Cannot read task file. Check file permissions.")
            print("Running in memory-only mode. Changes will not be saved.")
            self._memory_only_mode = True
            return []

    def save(self, tasks: list[Task]) -> bool:
        """
        Save tasks to JSON file atomically.

        Args:
            tasks: List of Task objects to save

        Returns:
            True if save successful, False otherwise
        """
        if self._memory_only_mode:
            return True  # Pretend success

        data = {
            "version": DATA_VERSION,
            "last_modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "tasks": [task.to_dict() for task in tasks]
        }

        try:
            # Write to temp file
            with open(self.temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            # Backup existing file
            if self.file_path.exists():
                shutil.copy2(self.file_path, self.backup_path)

            # Atomic rename
            self.temp_path.replace(self.file_path)
            return True

        except Exception as e:
            print(f"Warning: Could not save tasks. Your changes may be lost.")
            # Clean up temp file
            if self.temp_path.exists():
                self.temp_path.unlink()
            return False

    def _create_empty_file(self) -> None:
        """Create an empty tasks file."""
        data = {
            "version": DATA_VERSION,
            "last_modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "tasks": []
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
```

#### 4.2.3 `src/services/task_service.py` (Phase 2 - Basic)

```python
"""Business logic for task operations."""

from typing import Optional

from src.models import Task, Priority
from src.exceptions import TaskNotFoundError, AmbiguousIdError, ValidationError
from src.utils.constants import MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH, MIN_ID_LENGTH


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

    def toggle_complete(self, task_id: str) -> Task:
        """
        Toggle a task's completed status.

        Args:
            task_id: Full or partial task ID

        Returns:
            The updated Task
        """
        task = self.find_by_partial_id(task_id)
        task.completed = not task.completed
        task.mark_updated()
        self._save_tasks()
        return task

    def get_task_count(self) -> tuple[int, int]:
        """
        Get total and completed task counts.

        Returns:
            Tuple of (total_count, completed_count)
        """
        total = len(self._tasks)
        completed = sum(1 for t in self._tasks if t.completed)
        return total, completed
```

#### 4.2.4 `src/ui/__init__.py`

```python
"""User interface components."""

from .display import Display
from .input_handler import InputHandler
from .menu import Menu

__all__ = ["Display", "InputHandler", "Menu"]
```

#### 4.2.5 `src/ui/display.py`

```python
"""Output formatting functions."""

from typing import Optional
from src.models import Task
from src.utils.constants import SHORT_ID_LENGTH, TITLE_DISPLAY_LENGTH, APP_VERSION


class Display:
    """Handles all output formatting."""

    SEPARATOR = "=" * 80
    LINE = "-" * 80

    @staticmethod
    def welcome() -> None:
        """Display welcome banner."""
        print(Display.SEPARATOR)
        print(f"{'CONSOLE TODO APP v' + APP_VERSION:^80}")
        print(Display.SEPARATOR)
        print()

    @staticmethod
    def menu_level_1() -> None:
        """Display Level 1 (Basic) menu."""
        print(Display.SEPARATOR)
        print(f"{'MAIN MENU':^80}")
        print(Display.SEPARATOR)
        print("  1. Add task              5. Delete task")
        print("  2. List all tasks        6. Mark complete/incomplete")
        print("  3. View task details")
        print("  4. Update task           0. Exit")
        print("                           h. Help")
        print(Display.LINE)

    @staticmethod
    def task_list(tasks: list[Task], total: int, completed: int) -> None:
        """Display formatted task list."""
        print(Display.SEPARATOR)
        print(f"{'TASKS (' + str(total) + ' total, ' + str(completed) + ' completed)':^80}")
        print(Display.SEPARATOR)

        if not tasks:
            print()
            print("  No tasks yet! Use option 1 to add your first task.")
            print()
        else:
            print(f"{'ID':<10}{'STATUS':<8}{'PRI':<6}{'TITLE':<37}{'DUE':<12}TAGS")
            print(Display.LINE)

            for task in tasks:
                status = "[x]" if task.completed else "[ ]"
                pri = task.priority.display_short()
                title = task.title[:TITLE_DISPLAY_LENGTH]
                if len(task.title) > TITLE_DISPLAY_LENGTH:
                    title = title[:TITLE_DISPLAY_LENGTH-3] + "..."
                due = task.due_date or "-"
                tags = ", ".join(task.tags[:3]) if task.tags else "-"
                if len(task.tags) > 3:
                    tags += f" +{len(task.tags) - 3}"

                print(f"{task.short_id:<10}{status:<8}{pri:<6}{title:<37}{due:<12}{tags}")

        print(Display.SEPARATOR)
        print("Legend: [x] = Completed  [ ] = Pending  |  HIGH/MED/LOW/- = Priority")

    @staticmethod
    def task_details(task: Task) -> None:
        """Display full task details."""
        print(Display.SEPARATOR)
        print(f"{'TASK DETAILS':^80}")
        print(Display.SEPARATOR)
        print(f"ID:          {task.id}")
        print(f"Title:       {task.title}")
        print(f"Description: {task.description or '(no description)'}")
        print(f"Status:      {'Completed' if task.completed else 'Pending'}")
        print(f"Priority:    {task.priority.display_full()}")
        print(f"Tags:        {', '.join(task.tags) if task.tags else '(no tags)'}")
        print(f"Due Date:    {task.due_date or 'Not set'}")
        print(f"Recurring:   {task.recurring.capitalize() if task.recurring else 'Not set'}")
        print(f"Created:     {task.created_at.replace('T', ' ')}")
        print(f"Updated:     {task.updated_at.replace('T', ' ')}")
        print(Display.SEPARATOR)

    @staticmethod
    def help_level_1() -> None:
        """Display Level 1 help."""
        print(Display.SEPARATOR)
        print(f"{'HELP':^80}")
        print(Display.SEPARATOR)
        print()
        print("COMMANDS:")
        print("  1  - Add a new task")
        print("  2  - List all tasks")
        print("  3  - View task details (shows all information for one task)")
        print("  4  - Update a task (change title or description)")
        print("  5  - Delete a task (permanent, requires confirmation)")
        print("  6  - Toggle complete/incomplete status")
        print()
        print("  0  - Exit the application")
        print("  h  - Show this help message")
        print()
        print("TIPS:")
        print("  - Task IDs can be entered partially (first 4+ characters if unique)")
        print("  - When updating, press Enter to keep current value, or '-' to clear")
        print("  - Use 'list' to see all task IDs before other operations")
        print()
        print(Display.SEPARATOR)

    @staticmethod
    def success(message: str) -> None:
        """Display success message."""
        print(message)

    @staticmethod
    def error(message: str) -> None:
        """Display error message."""
        print(f"Error: {message}")

    @staticmethod
    def warning(message: str) -> None:
        """Display warning message."""
        print(f"Warning: {message}")

    @staticmethod
    def goodbye() -> None:
        """Display exit message."""
        print()
        print("Goodbye! Your tasks have been saved.")
```

#### 4.2.6 `src/ui/input_handler.py`

```python
"""Input prompts and validation."""


class InputHandler:
    """Handles user input with prompts."""

    @staticmethod
    def prompt(message: str) -> str:
        """
        Prompt for input and return stripped result.

        Args:
            message: Prompt message

        Returns:
            Stripped user input
        """
        return input(message).strip()

    @staticmethod
    def confirm(message: str) -> bool:
        """
        Prompt for yes/no confirmation.

        Args:
            message: Confirmation message (should include "(y/N)")

        Returns:
            True if user entered 'y' or 'Y', False otherwise
        """
        response = input(message).strip().lower()
        return response == 'y'

    @staticmethod
    def menu_choice() -> str:
        """
        Prompt for menu choice.

        Returns:
            User's menu choice (lowercase, stripped)
        """
        return input("Enter choice: ").strip().lower()

    @staticmethod
    def wait_for_enter() -> None:
        """Wait for user to press Enter."""
        input("Press Enter to continue...")
```

#### 4.2.7 `src/ui/menu.py`

```python
"""Menu display and command routing."""

import sys

from src.services import TaskService
from src.exceptions import TodoAppError
from src.ui.display import Display
from src.ui.input_handler import InputHandler


class Menu:
    """Main menu controller."""

    def __init__(self, task_service: TaskService) -> None:
        """
        Initialize menu.

        Args:
            task_service: TaskService instance
        """
        self.task_service = task_service
        self.display = Display()
        self.input = InputHandler()

    def main_loop(self) -> None:
        """Run the main menu loop."""
        while True:
            Display.menu_level_1()
            choice = InputHandler.menu_choice()

            if choice in ["0", "q", "quit", "exit"]:
                self._handle_exit()
            elif choice in ["h", "help"]:
                self._handle_help()
            elif choice == "1":
                self._handle_add()
            elif choice == "2":
                self._handle_list()
            elif choice == "3":
                self._handle_view()
            elif choice == "4":
                self._handle_update()
            elif choice == "5":
                self._handle_delete()
            elif choice == "6":
                self._handle_toggle()
            else:
                print("Invalid choice. Please enter a number from the menu or 'h' for help.")

            print()  # Blank line before next menu

    def _handle_exit(self) -> None:
        """Handle exit command."""
        Display.goodbye()
        sys.exit(0)

    def _handle_help(self) -> None:
        """Handle help command."""
        Display.help_level_1()
        InputHandler.wait_for_enter()

    def _handle_add(self) -> None:
        """Handle add task command."""
        print("--- Add New Task ---")
        print()

        title = InputHandler.prompt("Title: ")
        if not title:
            Display.error("Title cannot be empty.")
            return

        description = InputHandler.prompt("Description (press Enter to skip): ")

        try:
            task = self.task_service.add_task(title, description)
            print()
            Display.success(f"Task added successfully! ID: {task.short_id}")
        except TodoAppError as e:
            Display.error(str(e))

    def _handle_list(self) -> None:
        """Handle list tasks command."""
        tasks = self.task_service.get_all_tasks()
        total, completed = self.task_service.get_task_count()
        Display.task_list(tasks, total, completed)

    def _handle_view(self) -> None:
        """Handle view task command."""
        print("--- View Task ---")
        print()

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            Display.error("Task ID cannot be empty.")
            return

        try:
            task = self.task_service.find_by_partial_id(task_id)
            Display.task_details(task)
        except TodoAppError as e:
            Display.error(str(e))

    def _handle_update(self) -> None:
        """Handle update task command."""
        print("--- Update Task ---")
        print()

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            Display.error("Task ID cannot be empty.")
            return

        try:
            task = self.task_service.find_by_partial_id(task_id)

            print()
            print(f"Current title: {task.title}")
            new_title = InputHandler.prompt("New title (press Enter to keep current): ")

            print()
            print(f"Current description: {task.description or '(no description)'}")
            new_desc = InputHandler.prompt("New description (press Enter to keep current, '-' to clear): ")

            # Determine what to update
            title_to_set = new_title if new_title else None
            desc_to_set = "" if new_desc == "-" else (new_desc if new_desc else None)

            self.task_service.update_task(task.id, title_to_set, desc_to_set)
            print()
            Display.success("Task updated successfully!")

        except TodoAppError as e:
            Display.error(str(e))

    def _handle_delete(self) -> None:
        """Handle delete task command."""
        print("--- Delete Task ---")
        print()

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            Display.error("Task ID cannot be empty.")
            return

        try:
            task = self.task_service.find_by_partial_id(task_id)

            print()
            if not InputHandler.confirm(f'Delete task "{task.title}"? This cannot be undone. (y/N): '):
                print("Delete cancelled.")
                return

            self.task_service.delete_task(task.id)
            print()
            Display.success("Task deleted successfully.")

        except TodoAppError as e:
            Display.error(str(e))

    def _handle_toggle(self) -> None:
        """Handle toggle complete command."""
        print("--- Toggle Task Status ---")
        print()

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            Display.error("Task ID cannot be empty.")
            return

        try:
            task = self.task_service.toggle_complete(task_id)
            status = "completed" if task.completed else "pending"
            print()
            Display.success(f'Task "{task.title}" marked as {status}.')

        except TodoAppError as e:
            Display.error(str(e))
```

#### 4.2.8 `src/app.py`

```python
"""Main application class."""

import signal
import sys

from src.services import TaskService, StorageService
from src.ui import Menu, Display


class TodoApp:
    """Main application orchestrator."""

    def __init__(self, data_file: str = None) -> None:
        """
        Initialize the application.

        Args:
            data_file: Optional path to data file
        """
        self.storage = StorageService(data_file)
        self.task_service = TaskService(self.storage)
        self.menu = Menu(self.task_service)

        # Setup interrupt handler
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def run(self) -> None:
        """Start the application."""
        Display.welcome()
        self.menu.main_loop()

    def _handle_interrupt(self, signum, frame) -> None:
        """Handle Ctrl+C gracefully."""
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
```

#### 4.2.9 `main.py`

```python
#!/usr/bin/env python3
"""Console Todo App - Entry Point."""

from src.app import TodoApp


def main() -> None:
    """Initialize and run the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
```

### 4.3 Manual Testing Checklist

After Phase 2, test each option manually:

```
[ ] Run: python main.py
[ ] Option 1: Add task with title only
[ ] Option 1: Add task with title and description
[ ] Option 1: Try empty title (should error)
[ ] Option 2: List tasks (should show added tasks)
[ ] Option 3: View task by partial ID
[ ] Option 4: Update task title
[ ] Option 4: Update task description
[ ] Option 4: Clear description with '-'
[ ] Option 5: Delete task (confirm yes)
[ ] Option 5: Delete task (confirm no - should cancel)
[ ] Option 6: Toggle task to completed
[ ] Option 6: Toggle task back to pending
[ ] Option h: Show help
[ ] Option 0: Exit
[ ] Restart app - tasks should persist
```

### 4.4 Phase 2 Completion Checklist

- [ ] All menu options work
- [ ] Tasks persist after restart
- [ ] Error messages are clear
- [ ] Partial ID matching works

---

## 5. Phase 3: Persistence & Robustness

### 5.1 Objective

Ensure reliable data storage and graceful error handling.

### 5.2 Enhancements

#### 5.2.1 Add to `src/services/storage_service.py`

Add backup restoration method:

```python
def restore_from_backup(self) -> list[Task]:
    """
    Attempt to restore from backup file.

    Returns:
        List of tasks from backup, or empty list
    """
    if not self.backup_path.exists():
        return []

    try:
        with open(self.backup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [Task.from_dict(t) for t in data.get("tasks", [])]
    except Exception:
        return []
```

### 5.3 Tests to Add

#### `tests/test_storage_service.py`

```python
"""Tests for StorageService."""

import unittest
import json
import tempfile
from pathlib import Path

from src.services import StorageService
from src.models import Task


class TestStorageService(unittest.TestCase):
    """Test StorageService persistence."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test_tasks.json"

    def test_save_and_load_roundtrip(self):
        """Tasks should persist correctly."""
        storage = StorageService(self.test_file)

        # Create and save tasks
        tasks = [Task.create("Task 1"), Task.create("Task 2")]
        storage.save(tasks)

        # Load tasks
        loaded = storage.load()

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Task 1")
        self.assertEqual(loaded[1].title, "Task 2")

    def test_load_nonexistent_file_creates_empty(self):
        """Loading nonexistent file should create empty list."""
        storage = StorageService(self.test_file)
        tasks = storage.load()

        self.assertEqual(tasks, [])
        self.assertTrue(self.test_file.exists())

    def test_load_corrupted_file_recovers(self):
        """Loading corrupted file should recover gracefully."""
        # Write invalid JSON
        with open(self.test_file, 'w') as f:
            f.write("not valid json {{{")

        storage = StorageService(self.test_file)
        tasks = storage.load()

        self.assertEqual(tasks, [])

    def test_backup_created_on_save(self):
        """Backup file should be created on save."""
        storage = StorageService(self.test_file)

        # First save
        storage.save([Task.create("Task 1")])

        # Second save (creates backup)
        storage.save([Task.create("Task 1"), Task.create("Task 2")])

        self.assertTrue(storage.backup_path.exists())


if __name__ == "__main__":
    unittest.main()
```

### 5.4 Phase 3 Completion Checklist

- [ ] Backup file created on save
- [ ] Corrupted file handled gracefully
- [ ] Permission errors handled
- [ ] Atomic writes working

---

## 6. Phase 4: Intermediate Features

### 6.1 Objective

Add priority, tags, search, filter, and sort functionality.

### 6.2 Files to Modify

#### 6.2.1 Add to `src/services/task_service.py`

```python
# Add these imports at top
import re
from src.utils.constants import MAX_TAGS_PER_TASK, MAX_TAG_LENGTH, TAG_PATTERN, MIN_SEARCH_LENGTH

# Add these methods to TaskService class:

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
            # Priority: title > description > tags
            if query_lower in task.title.lower():
                results.append((task, 1))
            elif query_lower in task.description.lower():
                results.append((task, 2))
            elif any(query_lower in tag for tag in task.tags):
                results.append((task, 3))

        # Sort by priority, then by created_at descending
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
            "due_date_desc": lambda t: (t.due_date or "0000-00-00", t.title.lower()),
            "title": lambda t: t.title.lower(),
            "created": lambda t: t.created_at,
        }

        if sort_key not in sort_functions:
            return tasks

        return sorted(tasks, key=sort_functions[sort_key], reverse=reverse)
```

#### 6.2.2 Update `src/ui/menu.py`

Add handlers for options 7-12 and update the main loop.

### 6.3 Phase 4 Completion Checklist

- [ ] Option 7 (Priority): Works correctly
- [ ] Option 8 (Add Tag): Validates and adds
- [ ] Option 9 (Remove Tag): Works by name or number
- [ ] Option 10 (Search): Finds in title/description/tags
- [ ] Option 11 (Filter): All filter types work
- [ ] Option 12 (Sort): All sort options work
- [ ] Tags are lowercase
- [ ] Duplicate tags rejected
- [ ] Max 10 tags enforced

---

## 7. Phase 5: Advanced Features

### 7.1 Objective

Add due dates, reminders, and recurring tasks.

### 7.2 Files to Create

#### 7.2.1 `src/utils/date_utils.py`

```python
"""Date parsing and formatting utilities."""

from datetime import date, datetime, timedelta
from typing import Optional
import calendar


def parse_date(date_str: str) -> date:
    """Parse YYYY-MM-DD string to date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def format_date(d: date) -> str:
    """Format date as YYYY-MM-DD string."""
    return d.isoformat()


def get_today() -> date:
    """Get today's date."""
    return date.today()


def is_overdue(due_date: Optional[str]) -> bool:
    """Check if a due date is in the past."""
    if due_date is None:
        return False
    return parse_date(due_date) < get_today()


def is_due_today(due_date: Optional[str]) -> bool:
    """Check if a due date is today."""
    if due_date is None:
        return False
    return parse_date(due_date) == get_today()


def is_due_this_week(due_date: Optional[str]) -> bool:
    """Check if a due date is within the next 7 days."""
    if due_date is None:
        return False
    due = parse_date(due_date)
    today = get_today()
    return today <= due <= today + timedelta(days=7)


def calculate_next_due(current_due: str, pattern: str) -> str:
    """Calculate the next due date based on recurrence pattern."""
    due = parse_date(current_due)

    if pattern == "daily":
        new_due = due + timedelta(days=1)
    elif pattern == "weekly":
        new_due = due + timedelta(weeks=1)
    elif pattern == "monthly":
        year = due.year
        month = due.month + 1
        if month > 12:
            month = 1
            year += 1
        # Handle day overflow (e.g., Jan 31 -> Feb 28)
        day = min(due.day, calendar.monthrange(year, month)[1])
        new_due = date(year, month, day)
    else:
        new_due = due

    return format_date(new_due)


def format_relative(due_date: Optional[str]) -> str:
    """Format due date as relative string (Today, Tomorrow, etc.)."""
    if due_date is None:
        return "-"

    due = parse_date(due_date)
    today = get_today()
    diff = (due - today).days

    if diff < 0:
        return "OVERDUE"
    elif diff == 0:
        return "Today"
    elif diff == 1:
        return "Tomorrow"
    else:
        return due_date
```

### 7.3 Files to Modify

Add due date operations to `TaskService`:

```python
# Add to TaskService class:

    # ==================== Due Date Operations ====================

    def set_due_date(self, task_id: str, due_date: str) -> Task:
        """Set a task's due date."""
        task = self.find_by_partial_id(task_id)

        # Validate date format
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
        return [t for t in self._tasks
                if is_overdue(t.due_date) and not t.completed]

    def get_due_today(self) -> list[Task]:
        """Get all tasks due today."""
        return [t for t in self._tasks
                if is_due_today(t.due_date) and not t.completed]

    def get_due_this_week(self) -> list[Task]:
        """Get all tasks due in the next 7 days."""
        tasks = [t for t in self._tasks
                 if is_due_this_week(t.due_date) and not t.completed]
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
```

### 7.4 Phase 5 Completion Checklist

- [ ] Option 13 (Set Due): Date validation works
- [ ] Option 14 (Clear Due): Removes recurring too
- [ ] Option 15 (Overdue): Shows only overdue incomplete
- [ ] Option 16 (Due Today): Works correctly
- [ ] Option 17 (Due Week): Shows sorted by date
- [ ] Option 18 (Recurring): Requires due date
- [ ] Completing recurring task creates new instance
- [ ] Startup reminders work

---

## 8. Phase 6: Polish & Testing

### 8.1 Objective

Final cleanup, documentation, and comprehensive testing.

### 8.2 Tasks

1. **Add missing validators** in `src/utils/validators.py`
2. **Write integration tests** in `tests/test_integration.py`
3. **Create README.md** with usage instructions
4. **Run coverage report** and add tests for gaps
5. **Code cleanup** - remove any debug code, ensure PEP 8

### 8.3 Final Test Command

```bash
# Run all tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=html

# Open coverage report
# open htmlcov/index.html
```

### 8.4 Phase 6 Completion Checklist

- [ ] All tests pass
- [ ] Coverage ≥ 85%
- [ ] README.md complete
- [ ] No hardcoded values
- [ ] All public functions have docstrings
- [ ] PEP 8 compliant

---

## 9. Risk Mitigation

### 9.1 Potential Issues

| Risk | Impact | Mitigation |
|------|--------|------------|
| UUID collisions | Data corruption | UUID4 has negligible collision probability |
| File corruption | Data loss | Backup before every save |
| Date parsing errors | Crashes | Strict validation, try/except |
| Large task list | Slow performance | Keep in-memory, save only on change |
| Cross-platform paths | Breaks on different OS | Use pathlib everywhere |
| Ctrl+C during save | Partial write | Atomic write via temp file |

### 9.2 Safe Defaults

| Scenario | Default Behavior |
|----------|------------------|
| File not found | Create empty file |
| Corrupted JSON | Backup and start fresh |
| Permission denied | Memory-only mode |
| Invalid date | Reject with clear error |
| Empty title | Reject with error |

### 9.3 Recovery Procedures

**Corrupted File:**
```
1. App detects invalid JSON
2. Copies corrupted file to tasks.json.corrupted.<timestamp>
3. Creates new empty file
4. Warns user
```

**Permission Error:**
```
1. App detects permission error
2. Enables memory-only mode
3. Warns user changes won't persist
4. Continues operation normally
```

---

## 10. Quick Reference

### 10.1 Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point |
| `src/app.py` | Application orchestrator |
| `src/models/task.py` | Task dataclass |
| `src/services/task_service.py` | Business logic |
| `src/services/storage_service.py` | JSON persistence |
| `src/ui/menu.py` | Menu controller |
| `src/utils/constants.py` | All constants |

### 10.2 Key Commands

```bash
# Run application
python main.py

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src

# Type checking (if mypy installed)
python -m mypy src/
```

### 10.3 Implementation Order

```
1. constants.py → exceptions.py → priority.py → task.py
2. storage_service.py → task_service.py
3. display.py → input_handler.py → menu.py
4. app.py → main.py
5. Tests throughout
```

---

**Document Version:** 1.0.0
**Created:** Based on constitution.md v1.0.0 and .specify v2.0.0
**Compliance:** Fully aligned with project governance and specifications
