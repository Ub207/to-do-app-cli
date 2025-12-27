# Phase I Requirements Checklist

> Verification checklist for Phase I: Todo CLI (In-Memory)

---

## User Stories Verification

### US-001: Add a Task
- [ ] Title input is required
- [ ] Description input is optional
- [ ] UUID is auto-generated
- [ ] Task created with `completed: false`
- [ ] Confirmation shows short ID

### US-002: View All Tasks
- [ ] Shows all tasks (pending + completed)
- [ ] Displays: ID, status indicator, title
- [ ] Shows empty state message when no tasks
- [ ] Tasks in creation order

### US-003: View Task Details
- [ ] Accepts full or partial ID
- [ ] Shows all task fields
- [ ] Error if task not found

### US-004: Update a Task
- [ ] Accepts task ID
- [ ] Title update (Enter to keep)
- [ ] Description update (Enter to keep, '-' to clear)
- [ ] Updates `updated_at` timestamp

### US-005: Delete a Task
- [ ] Accepts task ID
- [ ] Confirmation required
- [ ] Task removed from memory
- [ ] Cancellation works

### US-006: Toggle Completion
- [ ] Accepts task ID
- [ ] Pending → Complete
- [ ] Complete → Pending
- [ ] Shows new status

---

## Technical Compliance

### Architecture
- [ ] `main.py` entry point exists
- [ ] `src/models/task.py` with dataclass
- [ ] `src/services/task_service.py` with business logic
- [ ] `src/ui/menu.py` with menu controller
- [ ] `src/ui/display.py` with output formatting
- [ ] `src/ui/input_handler.py` with input handling
- [ ] `src/exceptions.py` with custom exceptions

### Code Quality
- [ ] PEP 8 compliant
- [ ] Type hints on all functions
- [ ] Docstrings on public interfaces
- [ ] Functions under 30 lines
- [ ] No global mutable state

### Constraints
- [ ] Python stdlib only (no external deps)
- [ ] No file I/O for persistence
- [ ] No network access
- [ ] In-memory storage only

---

## Phase Isolation

### NOT Implemented (Phase II+)
- [ ] No priority levels
- [ ] No tags/categories
- [ ] No due dates
- [ ] No search functionality
- [ ] No filter options
- [ ] No sort options
- [ ] No file persistence

---

## Sign-off

| Check | Status | Notes |
|-------|--------|-------|
| All user stories implemented | | |
| Technical requirements met | | |
| Phase constraints respected | | |
| Tests passing | | |

**Approved:** _____________ **Date:** _____________
