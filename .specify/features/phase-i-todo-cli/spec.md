# Phase I Specification: Todo CLI (In-Memory)

> **Feature Specification** — Evolution of Todo Project
> Phase I: Console-based todo application with in-memory storage

---

## Document Information

| Attribute | Value |
|-----------|-------|
| **Phase** | I |
| **Feature** | Todo CLI (In-Memory) |
| **Version** | 1.0.0 |
| **Status** | Draft |
| **Created** | 2024-12-27 |
| **Constitution** | v1.0.0 |

---

## 1. Overview

### 1.1 Purpose

Build a simple, console-based todo application in Python that allows users to manage tasks during a single session. All data is stored in-memory and does not persist beyond the application runtime.

### 1.2 Scope

This specification covers **Phase I ONLY** — a minimal viable todo application with basic CRUD operations.

### 1.3 Constraints (Per Constitution)

```
ALLOWED:
  - Console input/output only
  - In-memory task storage (session-scoped)
  - Basic CRUD operations
  - Simple data structures
  - Python standard library only

FORBIDDEN:
  - File persistence
  - Database connections
  - Network access
  - External dependencies beyond stdlib
  - Priority, tags, due dates (Phase II+)
  - Search, filter, sort (Phase II+)
```

---

## 2. User Stories

### US-001: Add a Task
**As a** user
**I want to** add a new task with a title
**So that** I can track what I need to do

**Acceptance Criteria:**
- User can enter a task title (required)
- User can optionally enter a description
- System generates a unique ID for the task
- Task is created with "pending" status
- System confirms task creation with the assigned ID

### US-002: View All Tasks
**As a** user
**I want to** see all my tasks in a list
**So that** I can review what I have to do

**Acceptance Criteria:**
- Display shows all tasks (pending and completed)
- Each task shows: ID (short form), status indicator, title
- Empty state message when no tasks exist
- Tasks displayed in creation order

### US-003: View Task Details
**As a** user
**I want to** view the full details of a specific task
**So that** I can see all information about it

**Acceptance Criteria:**
- User enters task ID (full or partial)
- System displays: ID, title, description, status, created timestamp
- Error message if task not found

### US-004: Update a Task
**As a** user
**I want to** update an existing task's title or description
**So that** I can correct or improve task information

**Acceptance Criteria:**
- User enters task ID to update
- User can update title (press Enter to keep current)
- User can update description (press Enter to keep, '-' to clear)
- System confirms update
- Updated timestamp is recorded

### US-005: Delete a Task
**As a** user
**I want to** delete a task I no longer need
**So that** my list stays clean and relevant

**Acceptance Criteria:**
- User enters task ID to delete
- System asks for confirmation before deletion
- Task is permanently removed from memory
- System confirms deletion
- Cancellation returns to menu without deleting

### US-006: Toggle Task Completion
**As a** user
**I want to** mark a task as complete or incomplete
**So that** I can track my progress

**Acceptance Criteria:**
- User enters task ID
- If pending → marked complete
- If complete → marked pending
- System confirms the new status

---

## 3. Data Model

### 3.1 Task Entity

```python
@dataclass
class Task:
    id: str              # UUID v4 string
    title: str           # Required, non-empty
    description: str     # Optional, can be empty string
    completed: bool      # Default: False
    created_at: str      # ISO 8601 timestamp
    updated_at: str      # ISO 8601 timestamp
```

### 3.2 Field Specifications

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| `id` | string | Yes | Auto-generated | UUID v4 format |
| `title` | string | Yes | - | Non-empty, max 200 chars |
| `description` | string | No | "" | Max 1000 chars |
| `completed` | boolean | Yes | False | - |
| `created_at` | string | Yes | Auto-generated | ISO 8601 format |
| `updated_at` | string | Yes | Auto-generated | ISO 8601 format |

### 3.3 Short ID

For user convenience, tasks can be referenced by the first 8 characters of their UUID. The system must resolve partial IDs if unique.

---

## 4. CLI Interaction Flow

### 4.1 Application Startup

```
================================================================================
                           CONSOLE TODO APP v1.0.0
================================================================================

```

### 4.2 Main Menu

```
================================================================================
                                  MAIN MENU
================================================================================
  1. Add task              4. Update task
  2. List all tasks        5. Delete task
  3. View task details     6. Mark complete/incomplete

                           0. Exit
                           h. Help
--------------------------------------------------------------------------------
Enter choice:
```

### 4.3 Command Flow Examples

#### Add Task
```
--- Add New Task ---

Title: Buy groceries
Description (Enter to skip): Milk, bread, eggs

Task added! ID: a1b2c3d4
```

#### List Tasks
```
================================================================================
                        TASKS (3 total, 1 completed)
================================================================================
ID        STATUS   TITLE
--------------------------------------------------------------------------------
a1b2c3d4  [ ]      Buy groceries
e5f6g7h8  [x]      Call dentist
i9j0k1l2  [ ]      Finish report
================================================================================
Legend: [x] = Completed  [ ] = Pending
```

#### View Task Details
```
--- View Task ---

Enter task ID: a1b2
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

#### Update Task
```
--- Update Task ---

Enter task ID: a1b2

Current title: Buy groceries
New title (Enter to keep): Buy groceries and snacks
Current description: Milk, bread, eggs
New description (Enter to keep, '-' to clear): Milk, bread, eggs, chips

Task updated!
```

#### Delete Task
```
--- Delete Task ---

Enter task ID: a1b2

Delete "Buy groceries and snacks"? (y/N): y

Task deleted!
```

#### Toggle Complete
```
--- Toggle Status ---

Enter task ID: a1b2

"Buy groceries" marked as completed.
```

### 4.4 Exit
```
Goodbye! Your tasks were stored in memory only and have been discarded.
```

---

## 5. Error Handling

### 5.1 Error Cases

| Error | Message | Recovery |
|-------|---------|----------|
| Empty title | "Error: Title cannot be empty." | Return to menu |
| Task not found | "Error: No task found with ID 'xxx'." | Return to menu |
| Ambiguous ID | "Error: Multiple tasks match 'xx'. Please use more characters." | Return to menu |
| Invalid menu choice | "Invalid choice. Enter 1-6, 0, or 'h' for help." | Show menu again |

### 5.2 Input Validation

- **Title**: Must be non-empty after trimming whitespace
- **Task ID**: Must match existing task (full or unique partial)
- **Menu choice**: Must be valid option (0-6, h)
- **Confirmation**: Only 'y' or 'Y' means yes, anything else means no

---

## 6. Technical Requirements

### 6.1 Architecture

```
main.py
└── src/
    ├── __init__.py
    ├── app.py              # Application entry point
    ├── models/
    │   ├── __init__.py
    │   └── task.py         # Task dataclass
    ├── services/
    │   ├── __init__.py
    │   └── task_service.py # Business logic
    ├── ui/
    │   ├── __init__.py
    │   ├── menu.py         # Menu controller
    │   ├── display.py      # Output formatting
    │   └── input_handler.py # Input handling
    └── exceptions.py       # Custom exceptions
```

### 6.2 Dependencies

**Allowed (Python stdlib only):**
- `dataclasses` - Task model
- `uuid` - ID generation
- `datetime` - Timestamps
- `typing` - Type hints
- `sys` - Exit handling

**Forbidden:**
- Any external packages
- File I/O modules for persistence
- Network modules

### 6.3 Code Standards

Per Constitution Section 6.2:
- PEP 8 compliance
- Type hints on all function signatures
- Docstrings on all public interfaces
- Functions under 30 lines
- Single responsibility principle
- No global mutable state

---

## 7. Acceptance Criteria Summary

### 7.1 Functional Requirements

- [ ] AC-001: User can add a task with title and optional description
- [ ] AC-002: User can view list of all tasks with ID, status, and title
- [ ] AC-003: User can view full details of a specific task
- [ ] AC-004: User can update task title and/or description
- [ ] AC-005: User can delete a task with confirmation
- [ ] AC-006: User can toggle task completion status
- [ ] AC-007: Tasks are stored in memory during session
- [ ] AC-008: Application exits cleanly with goodbye message

### 7.2 Non-Functional Requirements

- [ ] NF-001: No external dependencies (stdlib only)
- [ ] NF-002: No file persistence
- [ ] NF-003: No network access
- [ ] NF-004: Responsive menu (< 100ms for operations)
- [ ] NF-005: Clear error messages for all error cases
- [ ] NF-006: PEP 8 compliant code

---

## 8. Out of Scope (Phase II+)

The following features are explicitly **NOT** part of Phase I:

- Priority levels (Phase II)
- Tags/categories (Phase II)
- Due dates (Phase II)
- Search functionality (Phase II)
- Filter by status/priority (Phase II)
- Sort options (Phase II)
- File persistence (Phase II)
- Database storage (Phase III)
- API endpoints (Phase III)
- Web interface (Phase IV)
- AI features (Phase V)

---

## 9. Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Specification Author | AI Agent | 2024-12-27 | ✓ |
| Technical Reviewer | | | |
| Product Owner | | | |

---

*This specification complies with Constitution v1.0.0.*
*No implementation shall begin until this specification is approved.*
