# Phase I Implementation Tasks

> Atomic, sequential tasks for Todo CLI (In-Memory)
> All tasks derived from spec.md and plan.md

---

## Document Information

| Attribute | Value |
|-----------|-------|
| **Phase** | I |
| **Feature** | Todo CLI (In-Memory) |
| **Spec Version** | 1.0.0 |
| **Plan Version** | 1.0.0 |
| **Total Tasks** | 24 |
| **Created** | 2024-12-27 |

---

## Task Legend

| Status | Meaning |
|--------|---------|
| `[ ]` | Not started |
| `[~]` | In progress |
| `[x]` | Completed |
| `[!]` | Blocked |

---

## Section 1: Project Setup & Exceptions

### TASK-001: Create project directory structure

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-001 |
| **Description** | Create the folder structure for Phase I application |
| **Preconditions** | None (first task) |
| **Expected Output** | Empty directory tree matching plan section 1.2 |
| **Artifacts** | Create directories: `src/`, `src/models/`, `src/services/`, `src/ui/` |
| **Spec Reference** | spec.md §6.1 Architecture |
| **Plan Reference** | plan.md §1.2 File Structure |

**Steps:**
1. Create `src/` directory
2. Create `src/models/` directory
3. Create `src/services/` directory
4. Create `src/ui/` directory

**Status:** `[x]`

---

### TASK-002: Create package __init__.py files

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-002 |
| **Description** | Create __init__.py files to mark directories as Python packages |
| **Preconditions** | TASK-001 completed |
| **Expected Output** | All directories are valid Python packages |
| **Artifacts** | Create: `src/__init__.py`, `src/models/__init__.py`, `src/services/__init__.py`, `src/ui/__init__.py` |
| **Spec Reference** | spec.md §6.1 Architecture |
| **Plan Reference** | plan.md §1.2 File Structure |

**Steps:**
1. Create `src/__init__.py` (empty)
2. Create `src/models/__init__.py` (will export Task)
3. Create `src/services/__init__.py` (will export TaskService)
4. Create `src/ui/__init__.py` (will export Menu, Display, InputHandler)

**Status:** `[x]`

---

### TASK-003: Create custom exceptions module

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-003 |
| **Description** | Create exception hierarchy for application errors |
| **Preconditions** | TASK-001 completed |
| **Expected Output** | Exception classes: TodoAppError, TaskNotFoundError, AmbiguousIdError, ValidationError |
| **Artifacts** | Create: `src/exceptions.py` |
| **Spec Reference** | spec.md §5.1 Error Cases |
| **Plan Reference** | plan.md §6.1 Exception Hierarchy |

**Implementation:**
```python
class TodoAppError(Exception):
    """Base exception for all application errors."""
    pass

class TaskNotFoundError(TodoAppError):
    """Raised when task ID doesn't match any task."""
    pass

class AmbiguousIdError(TodoAppError):
    """Raised when partial ID matches multiple tasks."""
    pass

class ValidationError(TodoAppError):
    """Raised when input fails validation."""
    pass
```

**Status:** `[x]`

---

## Section 2: Task Data Model

### TASK-004: Create Task dataclass

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-004 |
| **Description** | Create Task dataclass with all required fields |
| **Preconditions** | TASK-002 completed |
| **Expected Output** | Task class with id, title, description, completed, created_at, updated_at |
| **Artifacts** | Create: `src/models/task.py` |
| **Spec Reference** | spec.md §3.1 Task Entity, §3.2 Field Specifications |
| **Plan Reference** | plan.md §2.2 Task Model |

**Implementation:**
```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    completed: bool = False
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
```

**Status:** `[x]`

---

### TASK-005: Add short_id property to Task

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-005 |
| **Description** | Add short_id property that returns first 8 characters of UUID |
| **Preconditions** | TASK-004 completed |
| **Expected Output** | Task.short_id returns "a1b2c3d4" from full UUID |
| **Artifacts** | Modify: `src/models/task.py` |
| **Spec Reference** | spec.md §3.3 Short ID |
| **Plan Reference** | plan.md §3.3 ID Display |

**Implementation:**
```python
@property
def short_id(self) -> str:
    """Return first 8 characters of UUID."""
    return self.id[:8]
```

**Status:** `[x]`

---

### TASK-006: Export Task from models package

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-006 |
| **Description** | Update models __init__.py to export Task class |
| **Preconditions** | TASK-005 completed |
| **Expected Output** | `from src.models import Task` works |
| **Artifacts** | Modify: `src/models/__init__.py` |
| **Spec Reference** | spec.md §6.1 Architecture |
| **Plan Reference** | plan.md §1.2 File Structure |

**Implementation:**
```python
from src.models.task import Task

__all__ = ["Task"]
```

**Status:** `[x]`

---

## Section 3: Task Service (In-Memory Storage)

### TASK-007: Create TaskService class with storage

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-007 |
| **Description** | Create TaskService with in-memory dict storage |
| **Preconditions** | TASK-006 completed |
| **Expected Output** | TaskService class with _tasks dict initialized |
| **Artifacts** | Create: `src/services/task_service.py` |
| **Spec Reference** | spec.md §6.1 Architecture |
| **Plan Reference** | plan.md §2.1 Primary Storage |

**Implementation:**
```python
from src.models import Task

class TaskService:
    """Service for managing tasks in memory."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
```

**Status:** `[x]`

---

### TASK-008: Implement add_task method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-008 |
| **Description** | Implement method to create and store new task |
| **Preconditions** | TASK-007 completed |
| **Expected Output** | add_task(title, description) creates Task, stores it, returns it |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §2 US-001 Add a Task |
| **Plan Reference** | plan.md §7.1 TaskService Interface |

**Implementation:**
```python
def add_task(self, title: str, description: str = "") -> Task:
    """Create a new task."""
    title = title.strip()
    if not title:
        raise ValidationError("Title cannot be empty.")

    task = Task(title=title, description=description.strip())
    self._tasks[task.id] = task
    return task
```

**Status:** `[x]`

---

### TASK-009: Implement get_all_tasks method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-009 |
| **Description** | Implement method to return all tasks in creation order |
| **Preconditions** | TASK-007 completed |
| **Expected Output** | Returns list of all Task objects |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §2 US-002 View All Tasks |
| **Plan Reference** | plan.md §7.1 TaskService Interface |

**Implementation:**
```python
def get_all_tasks(self) -> list[Task]:
    """Get all tasks in creation order."""
    return list(self._tasks.values())
```

**Status:** `[x]`

---

### TASK-010: Implement get_task method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-010 |
| **Description** | Implement method to get task by exact ID |
| **Preconditions** | TASK-007 completed |
| **Expected Output** | Returns Task or raises TaskNotFoundError |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §2 US-003 View Task Details |
| **Plan Reference** | plan.md §7.1 TaskService Interface |

**Implementation:**
```python
def get_task(self, task_id: str) -> Task:
    """Get task by exact ID."""
    if task_id not in self._tasks:
        raise TaskNotFoundError(f"No task found with ID '{task_id}'.")
    return self._tasks[task_id]
```

**Status:** `[x]`

---

### TASK-011: Implement find_by_partial_id method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-011 |
| **Description** | Implement partial ID matching with prefix search |
| **Preconditions** | TASK-010 completed |
| **Expected Output** | Returns Task for unique match, raises error otherwise |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §3.3 Short ID, §5.1 Error Cases |
| **Plan Reference** | plan.md §3.2 Short ID Resolution |

**Implementation:**
```python
def find_by_partial_id(self, partial: str) -> Task:
    """Find task by partial ID prefix."""
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
```

**Status:** `[x]`

---

### TASK-012: Implement update_task method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-012 |
| **Description** | Implement method to update task title and/or description |
| **Preconditions** | TASK-010 completed |
| **Expected Output** | Updates task fields, updates timestamp, returns task |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §2 US-004 Update a Task |
| **Plan Reference** | plan.md §7.1 TaskService Interface |

**Implementation:**
```python
def update_task(
    self,
    task_id: str,
    title: str | None = None,
    description: str | None = None
) -> Task:
    """Update task fields."""
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
```

**Status:** `[x]`

---

### TASK-013: Implement delete_task method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-013 |
| **Description** | Implement method to remove task from storage |
| **Preconditions** | TASK-010 completed |
| **Expected Output** | Removes task from _tasks dict |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §2 US-005 Delete a Task |
| **Plan Reference** | plan.md §7.1 TaskService Interface |

**Implementation:**
```python
def delete_task(self, task_id: str) -> None:
    """Delete task by ID."""
    if task_id not in self._tasks:
        raise TaskNotFoundError(f"No task found with ID '{task_id}'.")
    del self._tasks[task_id]
```

**Status:** `[x]`

---

### TASK-014: Implement toggle_complete method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-014 |
| **Description** | Implement method to toggle task completion status |
| **Preconditions** | TASK-010 completed |
| **Expected Output** | Toggles completed flag, updates timestamp, returns task |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §2 US-006 Toggle Task Completion |
| **Plan Reference** | plan.md §7.1 TaskService Interface |

**Implementation:**
```python
def toggle_complete(self, task_id: str) -> Task:
    """Toggle task completion status."""
    task = self.get_task(task_id)
    task.completed = not task.completed
    task.updated_at = datetime.now().isoformat()
    return task
```

**Status:** `[x]`

---

### TASK-015: Implement get_task_count method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-015 |
| **Description** | Implement method to return total and completed counts |
| **Preconditions** | TASK-007 completed |
| **Expected Output** | Returns tuple (total, completed) |
| **Artifacts** | Modify: `src/services/task_service.py` |
| **Spec Reference** | spec.md §4.3 List Tasks display |
| **Plan Reference** | plan.md §7.1 TaskService Interface |

**Implementation:**
```python
def get_task_count(self) -> tuple[int, int]:
    """Get task counts."""
    total = len(self._tasks)
    completed = sum(1 for t in self._tasks.values() if t.completed)
    return total, completed
```

**Status:** `[x]`

---

### TASK-016: Export TaskService from services package

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-016 |
| **Description** | Update services __init__.py to export TaskService |
| **Preconditions** | TASK-015 completed |
| **Expected Output** | `from src.services import TaskService` works |
| **Artifacts** | Modify: `src/services/__init__.py` |
| **Spec Reference** | spec.md §6.1 Architecture |
| **Plan Reference** | plan.md §1.2 File Structure |

**Status:** `[x]`

---

## Section 4: UI Layer - Input Handler

### TASK-017: Create InputHandler class

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-017 |
| **Description** | Create InputHandler with prompt, menu_choice, and confirm methods |
| **Preconditions** | TASK-002 completed |
| **Expected Output** | InputHandler class with 3 static methods |
| **Artifacts** | Create: `src/ui/input_handler.py` |
| **Spec Reference** | spec.md §5.2 Input Validation |
| **Plan Reference** | plan.md §7.3 InputHandler Interface |

**Implementation:**
```python
class InputHandler:
    """Static methods for user input."""

    @staticmethod
    def prompt(message: str) -> str:
        """Get user input with prompt."""
        return input(message).strip()

    @staticmethod
    def menu_choice() -> str:
        """Get menu choice from user."""
        return input("Enter choice: ").strip().lower()

    @staticmethod
    def confirm(message: str) -> bool:
        """Get yes/no confirmation."""
        response = input(message).strip().lower()
        return response == "y"
```

**Status:** `[x]`

---

## Section 5: UI Layer - Display

### TASK-018: Create Display class with basic methods

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-018 |
| **Description** | Create Display class with welcome, menu, help, success, error, goodbye |
| **Preconditions** | TASK-002 completed |
| **Expected Output** | Display class with output formatting methods |
| **Artifacts** | Create: `src/ui/display.py` |
| **Spec Reference** | spec.md §4.1-4.4 CLI Interaction Flow |
| **Plan Reference** | plan.md §7.2 Display Interface |

**Methods to implement:**
- `welcome()` - Banner per spec §4.1
- `menu()` - Menu per spec §4.2
- `help()` - Help text
- `success(message)` - Success output
- `error(message)` - "Error: " prefix
- `goodbye()` - Exit message per spec §4.4

**Status:** `[x]`

---

### TASK-019: Implement task_list display method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-019 |
| **Description** | Implement task list display with ID, status, title columns |
| **Preconditions** | TASK-018 completed, TASK-006 completed |
| **Expected Output** | Formatted task list per spec §4.3 List Tasks |
| **Artifacts** | Modify: `src/ui/display.py` |
| **Spec Reference** | spec.md §4.3 List Tasks format |
| **Plan Reference** | plan.md §7.2 Display Interface |

**Format:**
```
================================================================================
                        TASKS (3 total, 1 completed)
================================================================================
ID        STATUS   TITLE
--------------------------------------------------------------------------------
a1b2c3d4  [ ]      Buy groceries
================================================================================
Legend: [x] = Completed  [ ] = Pending
```

**Status:** `[x]`

---

### TASK-020: Implement task_details display method

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-020 |
| **Description** | Implement full task details display |
| **Preconditions** | TASK-018 completed, TASK-006 completed |
| **Expected Output** | Formatted task details per spec §4.3 View Task Details |
| **Artifacts** | Modify: `src/ui/display.py` |
| **Spec Reference** | spec.md §4.3 View Task Details format |
| **Plan Reference** | plan.md §7.2 Display Interface |

**Format:**
```
================================================================================
                              TASK DETAILS
================================================================================
ID:          a1b2c3d4-e5f6-7890-abcd-ef1234567890
Title:       Buy groceries
Description: Milk, bread, eggs
Status:      Pending
Created:     2024-12-27 10:30:45
Updated:     2024-12-27 10:30:45
================================================================================
```

**Status:** `[x]`

---

## Section 6: UI Layer - Menu Controller

### TASK-021: Create Menu class with main_loop

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-021 |
| **Description** | Create Menu class with main_loop and command routing |
| **Preconditions** | TASK-016, TASK-017, TASK-020 completed |
| **Expected Output** | Menu class with while-loop and choice dispatch |
| **Artifacts** | Create: `src/ui/menu.py` |
| **Spec Reference** | spec.md §4.2 Main Menu |
| **Plan Reference** | plan.md §4.1 Main Loop, §4.2 State Machine |

**Implementation skeleton:**
```python
class Menu:
    def __init__(self, task_service: TaskService) -> None:
        self.task_service = task_service

    def main_loop(self) -> None:
        while True:
            Display.menu()
            choice = InputHandler.menu_choice()
            try:
                # Route to handlers
            except TodoAppError as e:
                Display.error(str(e))
```

**Status:** `[x]`

---

### TASK-022: Implement all menu command handlers

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-022 |
| **Description** | Implement _handle_add, _handle_list, _handle_view, _handle_update, _handle_delete, _handle_toggle, _handle_help, _handle_exit |
| **Preconditions** | TASK-021 completed |
| **Expected Output** | All 8 command handlers working |
| **Artifacts** | Modify: `src/ui/menu.py` |
| **Spec Reference** | spec.md §4.3 Command Flow Examples |
| **Plan Reference** | plan.md §4.3 Command Handler Pattern |

**Handlers:**
1. `_handle_add()` - US-001
2. `_handle_list()` - US-002
3. `_handle_view()` - US-003
4. `_handle_update()` - US-004
5. `_handle_delete()` - US-005
6. `_handle_toggle()` - US-006
7. `_handle_help()` - Display help
8. `_handle_exit()` - sys.exit(0)

**Status:** `[x]`

---

### TASK-023: Export UI classes from ui package

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-023 |
| **Description** | Update ui __init__.py to export Menu, Display, InputHandler |
| **Preconditions** | TASK-022 completed |
| **Expected Output** | `from src.ui import Menu, Display, InputHandler` works |
| **Artifacts** | Modify: `src/ui/__init__.py` |
| **Spec Reference** | spec.md §6.1 Architecture |
| **Plan Reference** | plan.md §1.2 File Structure |

**Status:** `[x]`

---

## Section 7: Application Bootstrap

### TASK-024: Create TodoApp class and main.py

| Attribute | Value |
|-----------|-------|
| **ID** | TASK-024 |
| **Description** | Create app.py with TodoApp class and main.py entry point |
| **Preconditions** | TASK-023 completed |
| **Expected Output** | Application runs with `python main.py` |
| **Artifacts** | Create: `src/app.py`, `main.py` |
| **Spec Reference** | spec.md §4.1 Application Startup, §4.4 Exit |
| **Plan Reference** | plan.md §1.1 Architecture Overview |

**Implementation:**

`src/app.py`:
```python
from src.services import TaskService
from src.ui import Menu, Display

class TodoApp:
    """Main application class."""

    def __init__(self) -> None:
        self.task_service = TaskService()
        self.menu = Menu(self.task_service)

    def run(self) -> None:
        """Run the application."""
        Display.welcome()
        self.menu.main_loop()
```

`main.py`:
```python
from src.app import TodoApp

def main() -> None:
    app = TodoApp()
    app.run()

if __name__ == "__main__":
    main()
```

**Status:** `[x]`

---

## Task Dependency Graph

```
TASK-001 (directories)
    │
    ├──▶ TASK-002 (__init__.py files)
    │        │
    │        ├──▶ TASK-004 (Task dataclass)
    │        │        │
    │        │        └──▶ TASK-005 (short_id)
    │        │                 │
    │        │                 └──▶ TASK-006 (export Task)
    │        │                          │
    │        │                          └──▶ TASK-007 (TaskService)
    │        │                                   │
    │        │                                   ├──▶ TASK-008 (add_task)
    │        │                                   ├──▶ TASK-009 (get_all_tasks)
    │        │                                   ├──▶ TASK-010 (get_task)
    │        │                                   │        │
    │        │                                   │        ├──▶ TASK-011 (find_by_partial_id)
    │        │                                   │        ├──▶ TASK-012 (update_task)
    │        │                                   │        ├──▶ TASK-013 (delete_task)
    │        │                                   │        └──▶ TASK-014 (toggle_complete)
    │        │                                   │
    │        │                                   └──▶ TASK-015 (get_task_count)
    │        │                                            │
    │        │                                            └──▶ TASK-016 (export TaskService)
    │        │
    │        ├──▶ TASK-017 (InputHandler)
    │        │
    │        └──▶ TASK-018 (Display basic)
    │                 │
    │                 ├──▶ TASK-019 (task_list)
    │                 └──▶ TASK-020 (task_details)
    │
    └──▶ TASK-003 (exceptions)

TASK-016 + TASK-017 + TASK-020
    │
    └──▶ TASK-021 (Menu class)
             │
             └──▶ TASK-022 (handlers)
                      │
                      └──▶ TASK-023 (export UI)
                               │
                               └──▶ TASK-024 (app.py + main.py)
```

---

## Summary

| Section | Tasks | Description |
|---------|-------|-------------|
| 1. Setup | TASK-001 to TASK-003 | Directory structure, packages, exceptions |
| 2. Model | TASK-004 to TASK-006 | Task dataclass |
| 3. Service | TASK-007 to TASK-016 | TaskService with all CRUD |
| 4. Input | TASK-017 | InputHandler |
| 5. Display | TASK-018 to TASK-020 | Display formatting |
| 6. Menu | TASK-021 to TASK-023 | Menu controller |
| 7. Bootstrap | TASK-024 | App entry point |

**Total: 24 tasks**

---

## Verification Checklist

After all tasks complete:

- [x] `python main.py` starts application
- [x] Welcome banner displays
- [x] Menu shows options 1-6, 0, h
- [x] Option 1: Add task works
- [x] Option 2: List tasks works (empty state + with tasks)
- [x] Option 3: View task details works
- [x] Option 4: Update task works
- [x] Option 5: Delete task works (with confirmation)
- [x] Option 6: Toggle complete works
- [x] Option h: Help displays
- [x] Option 0: Exit with goodbye message
- [x] Error: Empty title rejected
- [x] Error: Invalid ID shows message
- [x] Error: Ambiguous ID shows message
- [x] Error: Invalid menu choice shows message
- [x] All errors return to menu (no crash)

---

*Tasks derived from Phase I Specification v1.0.0 and Plan v1.0.0*
*Constitution v1.0.0 compliance verified*
