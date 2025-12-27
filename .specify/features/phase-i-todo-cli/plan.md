# Phase I Technical Plan: Todo CLI (In-Memory)

> **Implementation Plan** — Evolution of Todo Project
> Defines HOW the Phase I specification will be implemented

---

## Document Information

| Attribute | Value |
|-----------|-------|
| **Phase** | I |
| **Feature** | Todo CLI (In-Memory) |
| **Spec Version** | 1.0.0 |
| **Plan Version** | 1.0.0 |
| **Status** | Draft |
| **Created** | 2024-12-27 |

---

## Constitution Compliance Check

### Phase I Constraints ✓

| Rule | Status | Notes |
|------|--------|-------|
| Console I/O only | ✓ PASS | Using `print()` and `input()` |
| In-memory storage | ✓ PASS | Python `dict` for task storage |
| Basic CRUD only | ✓ PASS | 6 operations per spec |
| Python stdlib only | ✓ PASS | dataclasses, uuid, datetime, typing, sys |
| No file persistence | ✓ PASS | No file I/O in design |
| No database | ✓ PASS | No DB modules |
| No network | ✓ PASS | No network modules |
| No external deps | ✓ PASS | No pip packages |

### Code Quality Standards ✓

| Standard | Implementation |
|----------|----------------|
| PEP 8 | Enforced via style |
| Type hints | All function signatures |
| Docstrings | All public interfaces |
| Functions < 30 lines | Enforced via design |
| Single responsibility | Layer separation |
| No global mutable state | Encapsulated in service class |

---

## 1. High-Level Application Structure

### 1.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          main.py                                │
│                     (Entry Point)                               │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          src/app.py                             │
│                    (Application Bootstrap)                      │
│  - Creates TaskService instance                                 │
│  - Creates Menu with service                                    │
│  - Displays welcome, runs menu loop                             │
└─────────────────────────────┬───────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   src/ui/       │  │  src/services/  │  │   src/models/   │
│                 │  │                 │  │                 │
│ menu.py         │  │ task_service.py │  │ task.py         │
│ display.py      │  │                 │  │                 │
│ input_handler.py│  │                 │  │                 │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         │     UI Layer       │   Business Logic   │   Data Model
         │   (Presentation)   │      (Service)     │    (Domain)
         └────────────────────┴────────────────────┘
```

### 1.2 File Structure

```
to-do-app/
├── main.py                    # Entry point: calls TodoApp().run()
└── src/
    ├── __init__.py            # Empty, marks package
    ├── app.py                 # TodoApp class - bootstraps application
    ├── exceptions.py          # Custom exception classes
    ├── models/
    │   ├── __init__.py        # Exports Task
    │   └── task.py            # Task dataclass
    ├── services/
    │   ├── __init__.py        # Exports TaskService
    │   └── task_service.py    # Business logic, in-memory storage
    └── ui/
        ├── __init__.py        # Exports Menu, Display, InputHandler
        ├── menu.py            # Menu controller, command routing
        ├── display.py         # Output formatting functions
        └── input_handler.py   # Input prompts, validation
```

### 1.3 Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|----------------|--------------|
| `main.py` | Entry point only | `src.app` |
| `app.py` | Bootstrap, wire dependencies | `services`, `ui` |
| `task.py` | Task data structure | `dataclasses`, `uuid`, `datetime` |
| `task_service.py` | CRUD operations, storage | `models`, `exceptions` |
| `menu.py` | Menu loop, command dispatch | `services`, `ui.display`, `ui.input_handler` |
| `display.py` | All print statements | `models` |
| `input_handler.py` | All input() calls | None |
| `exceptions.py` | Custom exceptions | None |

---

## 2. In-Memory Data Structures

### 2.1 Primary Storage

```python
# In TaskService class
class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}  # key: full UUID, value: Task
```

**Design Decision**: Use `dict` for O(1) lookup by ID.

### 2.2 Task Model

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

    @property
    def short_id(self) -> str:
        """Return first 8 characters of UUID."""
        return self.id[:8]
```

### 2.3 Memory Lifecycle

```
Application Start
       │
       ▼
┌──────────────────┐
│ _tasks = {}      │  Empty dict created
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ User adds tasks  │  Tasks added to dict
│ _tasks[id] = t   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Application Exit │  Dict garbage collected
│ _tasks = None    │  All data lost (expected)
└──────────────────┘
```

---

## 3. Task Identification Strategy

### 3.1 ID Generation

```python
from uuid import uuid4

def generate_id() -> str:
    """Generate UUID v4 as string."""
    return str(uuid4())

# Example: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

**Why UUID v4:**
- Guaranteed uniqueness without coordination
- Standard library (`uuid` module)
- No external dependencies
- Human-readable when truncated

### 3.2 Short ID Resolution

Users can enter partial IDs (minimum 4 characters). The system resolves to full ID:

```python
def find_by_partial_id(self, partial: str) -> Task:
    """
    Find task by partial ID match.

    Args:
        partial: At least 4 characters of task ID

    Returns:
        Task if exactly one match found

    Raises:
        TaskNotFoundError: No tasks match
        AmbiguousIdError: Multiple tasks match
    """
    matches = [
        task for task in self._tasks.values()
        if task.id.startswith(partial)
    ]

    if len(matches) == 0:
        raise TaskNotFoundError(f"No task found with ID '{partial}'")
    if len(matches) > 1:
        raise AmbiguousIdError(
            f"Multiple tasks match '{partial}'. Use more characters."
        )
    return matches[0]
```

### 3.3 ID Display

| Context | Format | Example |
|---------|--------|---------|
| List view | First 8 chars | `a1b2c3d4` |
| Detail view | Full UUID | `a1b2c3d4-e5f6-7890-abcd-ef1234567890` |
| User input | 4+ chars | `a1b2` (resolved by system) |

---

## 4. CLI Control Flow

### 4.1 Main Loop

```python
# In Menu class
def main_loop(self) -> None:
    """Run the main menu loop until exit."""
    while True:
        Display.menu()
        choice = InputHandler.menu_choice()

        try:
            if choice in ["0", "q", "quit", "exit"]:
                self._handle_exit()  # sys.exit(0)
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
                print("Invalid choice. Enter 1-6, 0, or 'h' for help.")
        except TodoAppError as e:
            Display.error(str(e))
```

### 4.2 State Machine

```
                    ┌─────────────────────┐
                    │                     │
                    ▼                     │
┌────────┐    ┌──────────┐    ┌──────────┴────┐
│ START  │───▶│   MENU   │───▶│   COMMAND     │
└────────┘    └────┬─────┘    │   HANDLER     │
                   │          └───────────────┘
                   │                │
                   │    ┌───────────┘
                   │    │ (after command completes)
                   │    │
                   ▼    │
              ┌────────┴┐
              │  EXIT   │
              │ (0/q)   │
              └─────────┘
```

### 4.3 Command Handler Pattern

Each handler follows the same pattern:

```python
def _handle_<command>(self) -> None:
    """Handle <command> operation."""
    # 1. Display header
    print("--- <Command> ---\n")

    # 2. Get input (if needed)
    task_id = InputHandler.prompt("Enter task ID: ")
    if not task_id:
        return  # User cancelled

    # 3. Call service method
    task = self.task_service.<operation>(task_id)

    # 4. Display result
    Display.success("<Operation> complete!")
```

---

## 5. Separation of Responsibilities

### 5.1 Layer Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        UI LAYER                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Menu      │  │  Display    │  │    InputHandler         │ │
│  │             │  │             │  │                         │ │
│  │ - main_loop │  │ - welcome() │  │ - prompt()              │ │
│  │ - _handle_* │  │ - menu()    │  │ - menu_choice()         │ │
│  │             │  │ - task_list │  │ - confirm()             │ │
│  │             │  │ - error()   │  │                         │ │
│  └──────┬──────┘  └─────────────┘  └─────────────────────────┘ │
│         │                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │ calls
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    TaskService                              ││
│  │                                                             ││
│  │  - add_task(title, description) -> Task                     ││
│  │  - get_all_tasks() -> list[Task]                            ││
│  │  - get_task(id) -> Task                                     ││
│  │  - update_task(id, title, description) -> Task              ││
│  │  - delete_task(id) -> None                                  ││
│  │  - toggle_complete(id) -> Task                              ││
│  │  - find_by_partial_id(partial) -> Task                      ││
│  │                                                             ││
│  │  _tasks: dict[str, Task]  # Internal storage                ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
          │ uses
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                       MODEL LAYER                               │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                       Task                                  ││
│  │                                                             ││
│  │  @dataclass                                                 ││
│  │  - id: str                                                  ││
│  │  - title: str                                               ││
│  │  - description: str                                         ││
│  │  - completed: bool                                          ││
│  │  - created_at: str                                          ││
│  │  - updated_at: str                                          ││
│  │                                                             ││
│  │  @property short_id -> str                                  ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Responsibility Matrix

| Responsibility | UI | Service | Model |
|----------------|:--:|:-------:|:-----:|
| Print output | ✓ | | |
| Read input | ✓ | | |
| Menu routing | ✓ | | |
| CRUD operations | | ✓ | |
| Task storage | | ✓ | |
| ID resolution | | ✓ | |
| Validation | | ✓ | |
| Data structure | | | ✓ |
| ID generation | | | ✓ |
| Timestamps | | | ✓ |

### 5.3 Dependency Rules

```
UI Layer ─────────────▶ Service Layer ─────────────▶ Model Layer
         depends on                   depends on

✓ UI can import Service
✓ UI can import Model (for type hints)
✓ Service can import Model
✗ Model CANNOT import Service
✗ Model CANNOT import UI
✗ Service CANNOT import UI
```

---

## 6. Error Handling Strategy

### 6.1 Exception Hierarchy

```python
# src/exceptions.py

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

### 6.2 Error Flow

```
User Input
     │
     ▼
┌────────────────┐
│ InputHandler   │──── Invalid format ───▶ Immediate feedback
└───────┬────────┘                         (no exception)
        │
        ▼
┌────────────────┐
│ TaskService    │──── Business rule ────▶ Raise TodoAppError
└───────┬────────┘     violation
        │
        ▼
┌────────────────┐
│ Menu (catch)   │──── Display.error() ──▶ Return to menu
└────────────────┘
```

### 6.3 Error Messages (Per Spec)

| Error Type | Trigger | Message |
|------------|---------|---------|
| `ValidationError` | Empty title | "Error: Title cannot be empty." |
| `TaskNotFoundError` | No match | "Error: No task found with ID 'xxx'." |
| `AmbiguousIdError` | Multiple matches | "Error: Multiple tasks match 'xx'. Please use more characters." |
| Invalid choice | Bad menu input | "Invalid choice. Enter 1-6, 0, or 'h' for help." |

### 6.4 Recovery Strategy

All errors result in returning to the main menu:

```python
# In Menu.main_loop()
try:
    # ... handle command
except TodoAppError as e:
    Display.error(str(e))
    # Loop continues, menu redisplayed
```

No crashes. No stack traces shown to user. Graceful degradation.

---

## 7. Interface Contracts

### 7.1 TaskService Interface

```python
class TaskService:
    """Service for managing tasks in memory."""

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional)

        Returns:
            Created Task with generated ID

        Raises:
            ValidationError: If title is empty
        """
        pass

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks in creation order.

        Returns:
            List of all tasks (may be empty)
        """
        pass

    def get_task(self, task_id: str) -> Task:
        """
        Get task by exact ID.

        Args:
            task_id: Full UUID string

        Returns:
            Task if found

        Raises:
            TaskNotFoundError: If ID not found
        """
        pass

    def find_by_partial_id(self, partial: str) -> Task:
        """
        Find task by partial ID prefix.

        Args:
            partial: At least 4 characters of task ID

        Returns:
            Task if exactly one match

        Raises:
            TaskNotFoundError: No matches
            AmbiguousIdError: Multiple matches
        """
        pass

    def update_task(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None
    ) -> Task:
        """
        Update task fields.

        Args:
            task_id: Full UUID string
            title: New title (None = keep current)
            description: New description (None = keep, "" = clear)

        Returns:
            Updated Task

        Raises:
            TaskNotFoundError: If ID not found
            ValidationError: If new title is empty
        """
        pass

    def delete_task(self, task_id: str) -> None:
        """
        Delete task by ID.

        Args:
            task_id: Full UUID string

        Raises:
            TaskNotFoundError: If ID not found
        """
        pass

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
        pass

    def get_task_count(self) -> tuple[int, int]:
        """
        Get task counts.

        Returns:
            Tuple of (total_count, completed_count)
        """
        pass
```

### 7.2 Display Interface

```python
class Display:
    """Static methods for all output formatting."""

    @staticmethod
    def welcome() -> None:
        """Display application banner."""
        pass

    @staticmethod
    def menu() -> None:
        """Display main menu options."""
        pass

    @staticmethod
    def task_list(tasks: list[Task], total: int, completed: int) -> None:
        """Display formatted task list."""
        pass

    @staticmethod
    def task_details(task: Task) -> None:
        """Display full task details."""
        pass

    @staticmethod
    def help() -> None:
        """Display help information."""
        pass

    @staticmethod
    def success(message: str) -> None:
        """Display success message."""
        pass

    @staticmethod
    def error(message: str) -> None:
        """Display error message with 'Error: ' prefix."""
        pass

    @staticmethod
    def goodbye() -> None:
        """Display exit message."""
        pass
```

### 7.3 InputHandler Interface

```python
class InputHandler:
    """Static methods for user input."""

    @staticmethod
    def prompt(message: str) -> str:
        """
        Get user input with prompt.

        Args:
            message: Prompt to display

        Returns:
            User input stripped of whitespace
        """
        pass

    @staticmethod
    def menu_choice() -> str:
        """
        Get menu choice from user.

        Returns:
            Lowercase, stripped choice string
        """
        pass

    @staticmethod
    def confirm(message: str) -> bool:
        """
        Get yes/no confirmation.

        Args:
            message: Confirmation prompt

        Returns:
            True only if user enters 'y' or 'Y'
        """
        pass
```

---

## 8. Implementation Notes

### 8.1 No Future Phase Concepts

This plan explicitly excludes:

| Concept | Phase | Notes |
|---------|-------|-------|
| Priority enum | II | Not needed for Phase I |
| Tags list | II | Not needed for Phase I |
| Due date field | II | Not needed for Phase I |
| Search method | II | Not needed for Phase I |
| Filter method | II | Not needed for Phase I |
| Sort method | II | Not needed for Phase I |
| Storage abstraction | II | In-memory dict is sufficient |
| JSON serialization | II | No persistence needed |

### 8.2 Stdlib Modules Used

| Module | Usage | Phase I Approved |
|--------|-------|:----------------:|
| `dataclasses` | Task model | ✓ |
| `uuid` | ID generation | ✓ |
| `datetime` | Timestamps | ✓ |
| `typing` | Type hints | ✓ |
| `sys` | Exit handling | ✓ |

### 8.3 Testing Strategy

| Test Type | Scope | Tool |
|-----------|-------|------|
| Unit tests | TaskService methods | `unittest` |
| Unit tests | Task model | `unittest` |
| Integration | Menu + Service | Manual / `unittest` |

---

## 9. Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Plan Author | AI Agent | 2024-12-27 | ✓ |
| Technical Reviewer | | | |
| Product Owner | | | |

---

*This plan implements Phase I Specification v1.0.0.*
*This plan complies with Constitution v1.0.0.*
*No implementation shall deviate from this plan without amendment.*
