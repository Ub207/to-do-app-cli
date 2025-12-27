# Constitution: Python Console Todo List Application

> **Spec-Kit-Plus Constitution** — The supreme governing document for this project.
> All code, features, and decisions MUST align with these principles.

---

## 1. Project Identity

| Attribute       | Value                                      |
|-----------------|--------------------------------------------|
| **Name**        | Console Todo List                          |
| **Type**        | Command-Line Interface (CLI) Application   |
| **Language**    | Python 3.10+                               |
| **Paradigm**    | Object-Oriented with Functional Elements   |
| **Philosophy**  | Simplicity, Reliability, Maintainability   |

---

## 2. Non-Negotiable Principles

These rules are **absolute** and cannot be violated under any circumstances.

### 2.1 Application Type Constraints

```
MUST: Pure console/CLI application using input() and print() for all user interaction
MUST NOT: GUI frameworks (tkinter, PyQt, etc.)
MUST NOT: Web servers or frameworks (Flask, Django, FastAPI, etc.)
MUST NOT: Browser integration or HTTP endpoints
MUST NOT: External process execution or shell commands
MUST NOT: Network access or remote API calls
```

### 2.2 Code Quality Standards

```
MUST: Follow PEP 8 style guidelines
MUST: Use type hints (typing module) for all function signatures
MUST: Use meaningful, descriptive variable and function names
MUST: Keep functions small and single-purpose (< 30 lines preferred)
MUST: Maintain clear separation of concerns
MUST: Write self-documenting code with docstrings for public interfaces
MUST NOT: Use global mutable state (except controlled singletons for app state)
MUST NOT: Use magic numbers or hardcoded strings without constants
```

### 2.3 Dependency Constraints

```
ALLOWED (Standard Library Only):
  - json          → Data serialization
  - datetime      → Date/time handling
  - uuid          → Unique ID generation
  - typing        → Type annotations
  - pathlib       → File path handling
  - unittest      → Testing framework
  - dataclasses   → Data class definitions
  - enum          → Enumerations
  - re            → Regular expressions (for search)
  - os            → Environment variables only
  - sys           → System exit codes only

CONDITIONALLY ALLOWED (Optional Enhancement):
  - rich          → Enhanced CLI display (optional)
  - tabulate      → Table formatting (optional)

FORBIDDEN:
  - Any database library except sqlite3
  - Any web framework
  - Any GUI library
  - Any network/HTTP library
  - Any subprocess/shell execution library
```

### 2.4 Data Persistence Rules

```
MUST: Store all task data in a local JSON file (default: tasks.json)
MUST: Handle file not found gracefully (create new file)
MUST: Handle JSON parsing errors gracefully
MUST: Implement atomic writes (write to temp, then rename)
MUST: Preserve data integrity on crash/interrupt
MUST NOT: Use binary formats without JSON fallback
MUST NOT: Store sensitive data without user consent
```

### 2.5 Security & Safety

```
MUST NOT: Execute external commands or processes
MUST NOT: Access network or make HTTP requests
MUST NOT: Eval or exec user-provided strings
MUST NOT: Access files outside designated data directory
MUST NOT: Store or transmit user data externally
MUST: Sanitize all user inputs before processing
MUST: Validate file paths to prevent directory traversal
```

---

## 3. Architecture Specification

### 3.1 Core Data Model

```python
# Required Task attributes
@dataclass
class Task:
    id: str              # UUID4 string, immutable after creation
    title: str           # Required, non-empty, max 200 chars
    description: str     # Optional, max 2000 chars
    completed: bool      # Default: False
    priority: Priority   # Enum: NONE, LOW, MEDIUM, HIGH
    tags: list[str]      # List of tag strings, max 10 tags
    due_date: datetime | None  # Optional due date
    created_at: datetime # Auto-set on creation
    updated_at: datetime # Auto-updated on modification
```

### 3.2 Priority Enumeration

```python
class Priority(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
```

### 3.3 File Structure

```
to-do-app/
├── constitution.md          # This file - supreme law
├── main.py                  # Application entry point
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task dataclass
│   │   └── priority.py      # Priority enum
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py  # Business logic
│   │   └── storage_service.py # JSON persistence
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── menu.py          # Menu display and routing
│   │   ├── input_handler.py # User input processing
│   │   └── display.py       # Output formatting
│   └── utils/
│       ├── __init__.py
│       ├── validators.py    # Input validation
│       └── constants.py     # Application constants
├── tests/
│   ├── __init__.py
│   ├── test_task.py
│   ├── test_task_service.py
│   └── test_storage_service.py
├── data/
│   └── tasks.json           # Default data file location
└── README.md
```

### 3.4 Module Responsibilities

| Module | Responsibility |
|--------|----------------|
| `main.py` | Entry point, application bootstrap, main loop |
| `models/` | Data structures only, no business logic |
| `services/` | Business logic and data access |
| `ui/` | User interaction, display, input handling |
| `utils/` | Shared utilities, validators, constants |
| `tests/` | Unit tests for all modules |

---

## 4. Feature Implementation Levels

Features MUST be implemented in order. Higher levels require lower levels to be complete.

### Level 1: Basic (MVP) — Required First

| Feature | Command | Description |
|---------|---------|-------------|
| Add Task | `add` | Create task with title (required), description (optional) |
| List Tasks | `list` | Display all tasks with status |
| View Task | `view <id>` | Show single task details |
| Update Task | `update <id>` | Modify title/description |
| Delete Task | `delete <id>` | Remove task permanently |
| Complete Task | `done <id>` | Mark task as completed |
| Uncomplete Task | `undone <id>` | Mark task as not completed |
| Exit | `exit` / `quit` | Save and exit application |
| Help | `help` | Show available commands |

### Level 2: Intermediate — After Level 1

| Feature | Command | Description |
|---------|---------|-------------|
| Set Priority | `priority <id> <level>` | Set HIGH/MEDIUM/LOW/NONE |
| Add Tags | `tag <id> <tag>` | Add tag to task |
| Remove Tags | `untag <id> <tag>` | Remove tag from task |
| Filter by Status | `list --done` / `list --pending` | Filter completed/pending |
| Filter by Priority | `list --priority high` | Filter by priority level |
| Filter by Tag | `list --tag <tag>` | Filter by tag |
| Search | `search <query>` | Search in title/description |
| Sort | `list --sort <field>` | Sort by priority/date/title |

### Level 3: Advanced — After Level 2

| Feature | Command | Description |
|---------|---------|-------------|
| Due Dates | `due <id> <date>` | Set due date (YYYY-MM-DD) |
| List Overdue | `list --overdue` | Show overdue tasks |
| List Due Today | `list --today` | Show tasks due today |
| List Due This Week | `list --week` | Show tasks due this week |
| Clear Due Date | `cleardue <id>` | Remove due date |
| Bulk Complete | `done --all` | Mark all as complete |
| Bulk Delete | `delete --done` | Delete all completed |
| Export | `export <file>` | Export to JSON file |
| Import | `import <file>` | Import from JSON file |

---

## 5. User Interface Specifications

### 5.1 Command Format

```
<command> [arguments] [--options]

Examples:
  add "Buy groceries"
  add "Buy groceries" --desc "Milk, eggs, bread"
  list --priority high --sort due_date
  done 3
  delete 5
```

### 5.2 Display Format

```
Tasks (5 total, 2 completed)
================================================================================
ID   STATUS  PRI   TITLE                          DUE         TAGS
--------------------------------------------------------------------------------
1    [ ]     !!!   Buy groceries                  2024-01-15  shopping, urgent
2    [x]     !!    Call mom                       -           family
3    [ ]     !     Read book                      2024-01-20  personal
4    [ ]     -     Clean room                     -           home
5    [x]     -     Submit report                  -           work
================================================================================

Legend: [x]=Done [ ]=Pending | !!!=High !!=Medium !=Low -=None
```

### 5.3 Input Validation Messages

```
Error messages MUST be:
  - Clear and actionable
  - Non-technical for user errors
  - Suggest correct usage

Examples:
  "Invalid command. Type 'help' for available commands."
  "Task ID '99' not found. Use 'list' to see all tasks."
  "Priority must be one of: high, medium, low, none"
  "Date format must be YYYY-MM-DD (e.g., 2024-01-15)"
```

### 5.4 Confirmation Prompts

```
REQUIRE confirmation for:
  - Deleting a task
  - Bulk operations (delete all, complete all)
  - Importing data (overwrites existing)

Format: "Are you sure you want to delete task 'Buy groceries'? (y/N): "
Default: No (capital N indicates default)
```

---

## 6. Error Handling Specifications

### 6.1 Error Categories

| Category | Handling | User Message |
|----------|----------|--------------|
| Invalid Input | Reject, show help | "Invalid input. Expected: <format>" |
| Task Not Found | Reject operation | "Task with ID '<id>' not found" |
| File Read Error | Use empty state | "Could not load tasks. Starting fresh." |
| File Write Error | Retry, warn user | "Warning: Could not save tasks. Data may be lost." |
| Validation Error | Reject, explain | "Title cannot be empty" |
| Unexpected Error | Log, continue | "An error occurred. Please try again." |

### 6.2 Recovery Behavior

```
File corruption: Backup corrupted file, start fresh, warn user
Interrupt (Ctrl+C): Save current state, exit gracefully
Invalid JSON: Attempt repair, fallback to backup, warn user
```

---

## 7. Testing Requirements

### 7.1 Test Coverage Minimums

| Module | Minimum Coverage |
|--------|------------------|
| `models/` | 100% |
| `services/` | 90% |
| `utils/` | 90% |
| `ui/` | 70% (integration) |

### 7.2 Required Test Categories

```
Unit Tests:
  - Task creation with valid/invalid data
  - Priority assignment and comparison
  - Tag operations (add, remove, validate)
  - Date parsing and validation
  - JSON serialization/deserialization
  - Search and filter logic

Integration Tests:
  - Full CRUD workflow
  - File persistence round-trip
  - Menu navigation flow
```

### 7.3 Test File Naming

```
tests/test_<module_name>.py
tests/test_integration_<feature>.py
```

---

## 8. Code Patterns & Anti-Patterns

### 8.1 Required Patterns

```python
# Use dataclasses for models
@dataclass
class Task:
    ...

# Use Enum for fixed choices
class Priority(Enum):
    ...

# Use type hints everywhere
def add_task(title: str, description: str = "") -> Task:
    ...

# Use pathlib for file paths
data_file = Path("data") / "tasks.json"

# Use context managers for file operations
with open(file_path, 'w') as f:
    json.dump(data, f)
```

### 8.2 Forbidden Anti-Patterns

```python
# NO global mutable state
tasks = []  # FORBIDDEN at module level

# NO bare except
try:
    ...
except:  # FORBIDDEN
    pass

# NO string concatenation for paths
path = "data/" + filename  # FORBIDDEN

# NO eval/exec
eval(user_input)  # FORBIDDEN

# NO shell execution
os.system(command)  # FORBIDDEN
subprocess.run(...)  # FORBIDDEN
```

---

## 9. Configuration

### 9.1 Application Constants

```python
# File paths
DEFAULT_DATA_FILE = "data/tasks.json"
BACKUP_SUFFIX = ".backup"

# Validation limits
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000
MAX_TAGS_PER_TASK = 10
MAX_TAG_LENGTH = 50

# Display settings
LIST_PAGE_SIZE = 20
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
```

### 9.2 Exit Codes

```python
EXIT_SUCCESS = 0
EXIT_ERROR = 1
EXIT_INVALID_USAGE = 2
```

---

## 10. Version Control & Documentation

### 10.1 Commit Message Format

```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore
Scope: models, services, ui, utils, tests

Examples:
  feat(services): add task filtering by priority
  fix(storage): handle JSON decode errors gracefully
  test(models): add unit tests for Task validation
```

### 10.2 Code Documentation

```python
def add_task(title: str, description: str = "", priority: Priority = Priority.NONE) -> Task:
    """
    Create a new task and add it to the task list.

    Args:
        title: The task title (required, max 200 chars)
        description: Optional task description (max 2000 chars)
        priority: Task priority level (default: NONE)

    Returns:
        The newly created Task object

    Raises:
        ValueError: If title is empty or exceeds max length
    """
```

---

## 11. Amendment Process

This constitution may only be amended when:

1. A requirement directly conflicts with user needs
2. A technical limitation makes a rule impossible
3. A security vulnerability requires immediate change

**Amendment requires:**
- Clear justification documented
- Impact analysis on existing code
- Update to this constitution file
- Version increment in header

---

## 12. Compliance Checklist

Before any code merge, verify:

- [ ] No forbidden dependencies added
- [ ] No network/shell access introduced
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] Unit tests exist for new code
- [ ] PEP 8 compliance verified
- [ ] Error handling is graceful
- [ ] User messages are clear
- [ ] Data persistence is atomic
- [ ] No security vulnerabilities introduced

---

*This constitution is the supreme law of this project. All code must comply.*

**Version:** 1.0.0
**Effective Date:** 2024-01-01
**Last Updated:** 2024-01-01
