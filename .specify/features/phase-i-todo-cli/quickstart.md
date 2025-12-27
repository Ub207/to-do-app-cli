# Phase I Quickstart Guide

> Quick reference for implementing Todo CLI (In-Memory)

---

## Setup

```bash
# No setup required - Python stdlib only
# Requires Python 3.10+

python --version  # Verify 3.10+
```

---

## Project Structure

```
to-do-app/
├── main.py                    # Entry point
└── src/
    ├── __init__.py
    ├── app.py                 # TodoApp class
    ├── exceptions.py          # Custom exceptions
    ├── models/
    │   ├── __init__.py
    │   └── task.py            # Task dataclass
    ├── services/
    │   ├── __init__.py
    │   └── task_service.py    # Business logic
    └── ui/
        ├── __init__.py
        ├── menu.py            # Menu controller
        ├── display.py         # Output formatting
        └── input_handler.py   # Input handling
```

---

## Core Components

### 1. Task Model

```python
# src/models/task.py
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
        return self.id[:8]
```

### 2. Task Service

```python
# src/services/task_service.py
class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add_task(self, title: str, description: str = "") -> Task: ...
    def get_all_tasks(self) -> list[Task]: ...
    def find_by_partial_id(self, partial: str) -> Task: ...
    def update_task(self, task_id: str, title: str | None, desc: str | None) -> Task: ...
    def delete_task(self, task_id: str) -> None: ...
    def toggle_complete(self, task_id: str) -> Task: ...
```

### 3. Menu Loop

```python
# src/ui/menu.py
class Menu:
    def __init__(self, task_service: TaskService) -> None:
        self.task_service = task_service

    def main_loop(self) -> None:
        while True:
            Display.menu()
            choice = InputHandler.menu_choice()
            # Route to handler based on choice
```

---

## Run the App

```bash
python main.py
```

---

## Menu Options

| Option | Action |
|:------:|--------|
| 1 | Add task |
| 2 | List all tasks |
| 3 | View task details |
| 4 | Update task |
| 5 | Delete task |
| 6 | Toggle complete/incomplete |
| 0 | Exit |
| h | Help |

---

## Constraints Checklist

- [x] Python stdlib only
- [x] No file I/O
- [x] No database
- [x] No network
- [x] No priority/tags/due dates
- [x] No search/filter/sort
- [x] In-memory storage only
