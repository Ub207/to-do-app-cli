# Phase I Implementation Tasks: Todo CLI (In-Memory)

> **Atomic, TDD-driven tasks** organized by user story
> Derived from spec.md v1.1.0 and plan.md v1.1.0
> Complies with Constitution v2.0.0 Article 6.6 (TDD Mandate)

---

## Document Information

| Attribute | Value |
|-----------|-------|
| **Phase** | I |
| **Feature** | Todo CLI (In-Memory) |
| **Spec Version** | 1.1.0 |
| **Plan Version** | 1.1.0 |
| **Constitution** | v2.0.0 |
| **Total Tasks** | 45 |
| **Created** | 2024-12-27 |
| **Updated** | 2025-12-29 |
| **TDD Approach** | RED-GREEN-REFACTOR |

---

## Task Format

Each task follows this format:
```
- [ ] [TaskID] [P] [Story] Description with file path
```

**Legend:**
- `[TaskID]`: Sequential task number (T001, T002, etc.)
- `[P]`: Task can be executed in parallel with others
- `[Story]`: User story reference (US1, US2, US3, etc.)
- File paths are always absolute or relative to project root

---

## Phase 1: Setup & Foundation

### Project Initialization

- [ ] T001 Create project directory structure (src/, src/models/, src/services/, src/ui/) per plan.md §1.2
- [ ] T002 Create Python package markers (__init__.py) in all directories per plan.md §1.2
- [ ] T003 [P] Create custom exceptions module in src/exceptions.py per plan.md §6.1

**Spec References:** spec.md §6.1 Architecture
**Plan References:** plan.md §1.2 File Structure, §6.1 Exception Hierarchy

---

## Phase 2: Core Data Model & Service Foundation

### Task Model (Foundational - Required for All Stories)

- [ ] T004 [RED] Write tests for Task dataclass creation in tests/test_task.py
- [ ] T005 [GREEN] Implement Task dataclass in src/models/task.py with 6 fields per spec.md §3.1
- [ ] T006 [GREEN] Add short_id property to Task in src/models/task.py per spec.md §3.3
- [ ] T007 [REFACTOR] Add type hints and docstrings to Task class per plan.md §1.3

### TaskService Foundation

- [ ] T008 [RED] Write tests for TaskService initialization in tests/test_task_service.py
- [ ] T009 [GREEN] Create TaskService class skeleton in src/services/task_service.py per plan.md §2.1
- [ ] T010 [GREEN] Implement in-memory storage (dict[str, Task]) in TaskService per plan.md §2.1
- [ ] T011 [REFACTOR] Add type hints and docstrings to TaskService init

**Spec References:** spec.md §3 Data Model
**Plan References:** plan.md §2 In-Memory Data Structures, §7.1 TaskService Interface

---

## Phase 3: User Story 1 - Add Task (US-001)

**Goal:** User can add a new task with title and optional description

**Independent Test Criteria:**
- User can create task with title only
- User can create task with title and description
- Empty title raises ValidationError
- Task gets unique ID and timestamps
- Task is retrievable after creation

### Tests (RED Phase)

- [ ] T012 [RED] [US1] Write test_add_task_with_title_only() in tests/test_task_service.py per spec.md §6.4 US-001
- [ ] T013 [RED] [US1] Write test_add_task_with_title_and_description() per spec.md §6.4 US-001
- [ ] T014 [RED] [US1] Write test_add_task_generates_unique_id() per spec.md §6.4 US-001
- [ ] T015 [RED] [US1] Write test_add_task_sets_pending_status() per spec.md §6.4 US-001
- [ ] T016 [RED] [US1] Write test_add_task_empty_title_raises_error() per spec.md §6.4 US-001
- [ ] T017 [RED] [US1] Write test_add_task_returns_task_id() per spec.md §6.4 US-001

### Implementation (GREEN Phase)

- [ ] T018 [GREEN] [US1] Implement add_task() method in src/services/task_service.py per plan.md §7.1
- [ ] T019 [GREEN] [US1] Add title validation (non-empty) in add_task() per spec.md §3.2
- [ ] T020 [GREEN] [US1] Add timestamp generation in add_task() per spec.md §3.1

### Refactoring

- [ ] T021 [REFACTOR] [US1] Add comprehensive docstrings to add_task() method
- [ ] T022 [REFACTOR] [US1] Ensure add_task() follows single responsibility principle

**Spec References:** spec.md §2 US-001, §6.4 TDD Test Scenarios
**Plan References:** plan.md §7.1 TaskService Interface

---

## Phase 4: User Story 2 - View All Tasks (US-002)

**Goal:** User can see all their tasks in a list

**Independent Test Criteria:**
- Returns all tasks (pending and completed)
- Returns empty list when no tasks exist
- Tasks are in creation order
- Each task shows ID (short form), status, title

### Tests (RED Phase)

- [ ] T023 [RED] [US2] Write test_list_tasks_shows_all_tasks() in tests/test_task_service.py per spec.md §6.4 US-002
- [ ] T024 [RED] [US2] Write test_list_tasks_empty_state_message() per spec.md §6.4 US-002
- [ ] T025 [RED] [US2] Write test_list_tasks_shows_id_status_title() per spec.md §6.4 US-002
- [ ] T026 [RED] [US2] Write test_list_tasks_creation_order() per spec.md §6.4 US-002
- [ ] T027 [RED] [US2] Write test_list_tasks_displays_pending_and_completed() per spec.md §6.4 US-002

### Implementation (GREEN Phase)

- [ ] T028 [GREEN] [US2] Implement get_all_tasks() in src/services/task_service.py per plan.md §7.1
- [ ] T029 [GREEN] [US2] Implement get_task_count() for statistics in src/services/task_service.py per plan.md §7.1
- [ ] T030 [GREEN] [US2] Create Display.task_list() in src/ui/display.py per plan.md §7.2
- [ ] T031 [GREEN] [US2] Add formatted output with headers and legend in Display.task_list() per spec.md §4.3

### Refactoring

- [ ] T032 [REFACTOR] [US2] Optimize task_list display formatting
- [ ] T033 [REFACTOR] [US2] Add type hints to Display.task_list()

**Spec References:** spec.md §2 US-002, §4.3 List Tasks, §6.4 TDD Test Scenarios
**Plan References:** plan.md §7.1 TaskService Interface, §7.2 Display Interface

---

## Phase 5: User Story 3 - View Task Details (US-003)

**Goal:** User can view full details of a specific task

**Independent Test Criteria:**
- Can find task by full ID
- Can find task by partial ID (min 4 chars)
- Error when task not found
- Error when partial ID is ambiguous
- Displays all 6 task fields

### Tests (RED Phase)

- [ ] T034 [RED] [US3] Write test_view_task_by_full_id() in tests/test_task_service.py per spec.md §6.4 US-003
- [ ] T035 [RED] [US3] Write test_view_task_by_partial_id() per spec.md §6.4 US-003
- [ ] T036 [RED] [US3] Write test_view_task_not_found_error() per spec.md §6.4 US-003
- [ ] T037 [RED] [US3] Write test_view_task_displays_all_fields() per spec.md §6.4 US-003

### Implementation (GREEN Phase)

- [ ] T038 [GREEN] [US3] Implement get_task() in src/services/task_service.py per plan.md §7.1
- [ ] T039 [GREEN] [US3] Implement find_by_partial_id() in src/services/task_service.py per plan.md §3.2
- [ ] T040 [GREEN] [US3] Add ambiguous ID detection in find_by_partial_id() per spec.md §5.1
- [ ] T041 [GREEN] [US3] Create Display.task_details() in src/ui/display.py per plan.md §7.2

### Refactoring

- [ ] T042 [REFACTOR] [US3] Optimize partial ID matching algorithm
- [ ] T043 [REFACTOR] [US3] Add comprehensive error handling in find_by_partial_id()

**Spec References:** spec.md §2 US-003, §3.3 Short ID, §4.3 View Task Details, §6.4 TDD Test Scenarios
**Plan References:** plan.md §3.2 Short ID Resolution, §7.1 TaskService Interface

---

## Phase 6: User Story 4 - Update Task (US-004)

**Goal:** User can update an existing task's title or description

**Independent Test Criteria:**
- Can update title only
- Can update description only
- Can update both fields
- Can keep current values (press Enter)
- Can clear description ('-')
- Updated timestamp changes
- Error when task not found

### Tests (RED Phase)

- [ ] T044 [RED] [US4] Write test_update_task_title() in tests/test_task_service.py per spec.md §6.4 US-004
- [ ] T045 [RED] [US4] Write test_update_task_description() per spec.md §6.4 US-004
- [ ] T046 [RED] [US4] Write test_update_task_both_fields() per spec.md §6.4 US-004
- [ ] T047 [RED] [US4] Write test_update_task_keep_current_values() per spec.md §6.4 US-004
- [ ] T048 [RED] [US4] Write test_update_task_clear_description() per spec.md §6.4 US-004
- [ ] T049 [RED] [US4] Write test_update_timestamp_changes() per spec.md §6.4 US-004
- [ ] T050 [RED] [US4] Write test_update_task_not_found_error() per spec.md §6.4 US-004

### Implementation (GREEN Phase)

- [ ] T051 [GREEN] [US4] Implement update_task() in src/services/task_service.py per plan.md §7.1
- [ ] T052 [GREEN] [US4] Add optional parameter handling (None = keep) in update_task()
- [ ] T053 [GREEN] [US4] Add updated_at timestamp refresh in update_task() per spec.md §3.1
- [ ] T054 [GREEN] [US4] Add empty title validation in update_task() per spec.md §5.2

### Refactoring

- [ ] T055 [REFACTOR] [US4] Simplify update_task() parameter handling
- [ ] T056 [REFACTOR] [US4] Add defensive validation for update_task()

**Spec References:** spec.md §2 US-004, §4.3 Update Task, §6.4 TDD Test Scenarios
**Plan References:** plan.md §7.1 TaskService Interface

---

## Phase 7: User Story 5 - Delete Task (US-005)

**Goal:** User can delete a task they no longer need

**Independent Test Criteria:**
- Task is removed from memory
- Confirmation required before deletion
- Can cancel deletion
- Error when task not found
- Deleted task cannot be retrieved

### Tests (RED Phase)

- [ ] T057 [RED] [US5] Write test_delete_task_with_confirmation() in tests/test_task_service.py per spec.md §6.4 US-005
- [ ] T058 [RED] [US5] Write test_delete_task_cancel() per spec.md §6.4 US-005
- [ ] T059 [RED] [US5] Write test_delete_task_not_found_error() per spec.md §6.4 US-005
- [ ] T060 [RED] [US5] Write test_delete_task_removes_from_memory() per spec.md §6.4 US-005

### Implementation (GREEN Phase)

- [ ] T061 [GREEN] [US5] Implement delete_task() in src/services/task_service.py per plan.md §7.1
- [ ] T062 [GREEN] [US5] Add permanent removal from storage dict in delete_task()
- [ ] T063 [GREEN] [US5] Add TaskNotFoundError handling in delete_task() per spec.md §5.1

### Refactoring

- [ ] T064 [REFACTOR] [US5] Add defensive checks to delete_task()
- [ ] T065 [REFACTOR] [US5] Ensure delete_task() is idempotent

**Spec References:** spec.md §2 US-005, §4.3 Delete Task, §6.4 TDD Test Scenarios
**Plan References:** plan.md §7.1 TaskService Interface

---

## Phase 8: User Story 6 - Toggle Task Completion (US-006)

**Goal:** User can mark a task as complete or incomplete

**Independent Test Criteria:**
- Pending task becomes completed
- Completed task becomes pending
- Error when task not found
- Updated timestamp changes on toggle

### Tests (RED Phase)

- [ ] T066 [RED] [US6] Write test_toggle_pending_to_complete() in tests/test_task_service.py per spec.md §6.4 US-006
- [ ] T067 [RED] [US6] Write test_toggle_complete_to_pending() per spec.md §6.4 US-006
- [ ] T068 [RED] [US6] Write test_toggle_task_not_found_error() per spec.md §6.4 US-006
- [ ] T069 [RED] [US6] Write test_toggle_updates_timestamp() per spec.md §6.4 US-006

### Implementation (GREEN Phase)

- [ ] T070 [GREEN] [US6] Implement toggle_complete() in src/services/task_service.py per plan.md §7.1
- [ ] T071 [GREEN] [US6] Add boolean flip logic in toggle_complete()
- [ ] T072 [GREEN] [US6] Add updated_at timestamp refresh in toggle_complete()

### Refactoring

- [ ] T073 [REFACTOR] [US6] Simplify toggle_complete() logic
- [ ] T074 [REFACTOR] [US6] Add clear status messaging in toggle_complete()

**Spec References:** spec.md §2 US-006, §4.3 Toggle Complete, §6.4 TDD Test Scenarios
**Plan References:** plan.md §7.1 TaskService Interface

---

## Phase 9: CLI User Interface Layer

### Input Handling

- [ ] T075 [P] Create InputHandler class skeleton in src/ui/input_handler.py per plan.md §7.3
- [ ] T076 [P] Implement InputHandler.prompt() in src/ui/input_handler.py per plan.md §7.3
- [ ] T077 [P] Implement InputHandler.menu_choice() in src/ui/input_handler.py per plan.md §7.3
- [ ] T078 [P] Implement InputHandler.confirm() in src/ui/input_handler.py per plan.md §7.3

### Display Output

- [ ] T079 [P] Create Display class skeleton in src/ui/display.py per plan.md §7.2
- [ ] T080 [P] Implement Display.welcome() banner in src/ui/display.py per spec.md §4.1
- [ ] T081 [P] Implement Display.menu() in src/ui/display.py per spec.md §4.2
- [ ] T082 [P] Implement Display.help() in src/ui/display.py per plan.md §7.2
- [ ] T083 [P] Implement Display.success() in src/ui/display.py per plan.md §7.2
- [ ] T084 [P] Implement Display.error() in src/ui/display.py per plan.md §7.2
- [ ] T085 [P] Implement Display.goodbye() in src/ui/display.py per spec.md §4.4

### Menu Controller

- [ ] T086 Create Menu class skeleton in src/ui/menu.py per plan.md §4.1
- [ ] T087 Implement Menu.__init__() with TaskService injection per plan.md §1.3
- [ ] T088 Implement Menu.main_loop() with while-true pattern per plan.md §4.1
- [ ] T089 Add command routing (if-elif) in main_loop() per plan.md §4.1
- [ ] T090 Implement Menu._handle_add() calling TaskService.add_task() per plan.md §4.3
- [ ] T091 Implement Menu._handle_list() calling TaskService.get_all_tasks() per plan.md §4.3
- [ ] T092 Implement Menu._handle_view() calling TaskService.get_task() per plan.md §4.3
- [ ] T093 Implement Menu._handle_update() calling TaskService.update_task() per plan.md §4.3
- [ ] T094 Implement Menu._handle_delete() with confirmation per plan.md §4.3
- [ ] T095 Implement Menu._handle_toggle() calling TaskService.toggle_complete() per plan.md §4.3
- [ ] T096 Implement Menu._handle_help() displaying help text per plan.md §4.3
- [ ] T097 Implement Menu._handle_exit() with goodbye message per plan.md §4.3

**Spec References:** spec.md §4 CLI Interaction Flow
**Plan References:** plan.md §4 CLI Control Flow, §7.2-7.3 Interface Contracts

---

## Phase 10: Application Bootstrap & Integration

### Application Entry

- [ ] T098 Create TodoApp class in src/app.py per plan.md §1.1
- [ ] T099 Implement TodoApp.__init__() creating TaskService and Menu instances per plan.md §1.1
- [ ] T100 Implement TodoApp.run() calling Display.welcome() and Menu.main_loop() per plan.md §1.1
- [ ] T101 Create main.py entry point calling TodoApp().run() per plan.md §1.2

### Error Handling Integration

- [ ] T102 Add try-except TodoAppError in Menu.main_loop() per plan.md §6.2
- [ ] T103 Add error display for all command handlers per plan.md §6.4
- [ ] T104 Ensure graceful degradation (return to menu) on all errors per plan.md §6.4

**Spec References:** spec.md §4.1 Application Startup, §4.4 Exit, §5 Error Handling
**Plan References:** plan.md §1.1 Architecture Overview, §6 Error Handling Strategy

---

## Phase 11: Polish & Cross-Cutting Concerns

### Code Quality

- [ ] T105 [P] Add comprehensive type hints to all public interfaces per plan.md §1.3
- [ ] T106 [P] Add docstrings to all public methods per plan.md §1.3
- [ ] T107 [P] Verify all functions are under 30 lines per plan.md §1.3
- [ ] T108 [P] Run PEP 8 validation on all modules per spec.md §6.3

### Package Exports

- [ ] T109 Update src/models/__init__.py to export Task
- [ ] T110 Update src/services/__init__.py to export TaskService
- [ ] T111 Update src/ui/__init__.py to export Menu, Display, InputHandler

### Final Validation

- [ ] T112 Test complete user journey: add → list → view → update → toggle → delete
- [ ] T113 Verify all error cases show proper messages per spec.md §5.1
- [ ] T114 Verify application exits cleanly per spec.md §4.4
- [ ] T115 Verify no file I/O or network access per Constitution Article 4.3
- [ ] T116 Run all unit tests and verify 90%+ coverage per Constitution Article 6.5

**Spec References:** spec.md §6.3 Code Standards, §7 Acceptance Criteria
**Plan References:** plan.md §1.3 Module Responsibilities
**Constitution References:** Article 4.3 Phase I Scope, Article 6 Quality Principles

---

## Task Dependencies & Execution Strategy

### Critical Path (Must Execute Sequentially)

```
T001-T003 (Setup)
   ↓
T004-T011 (Foundation)
   ↓
T012-T022 (US1: Add Task)
   ↓
T023-T033 (US2: View All)
   ↓
T034-T043 (US3: View Details)
   ↓
T044-T056 (US4: Update)
   ↓
T057-T065 (US5: Delete)
   ↓
T066-T074 (US6: Toggle)
   ↓
T075-T097 (CLI Layer)
   ↓
T098-T104 (Bootstrap)
   ↓
T105-T116 (Polish)
```

### Parallel Execution Opportunities

**After Foundation (T011):**
- UI components (T075-T085) can be built in parallel with user story implementations
- All tasks marked `[P]` can run concurrently

**Independent User Stories:**
- US3, US4, US5, US6 can be implemented in parallel after US1 and US2 are complete
- Each user story's tests can be written in parallel

### Minimum Viable Product (MVP)

For quickest value delivery, implement in this order:
1. **MVP Scope:** T001-T033 (Setup + Foundation + US1 + US2)
2. **Increment 1:** Add US3 (View Details)
3. **Increment 2:** Add US4, US5 (Update, Delete)
4. **Increment 3:** Add US6 (Toggle Complete)
5. **Polish:** T105-T116

---

## Test Coverage Matrix

| User Story | Test Count | Implementation Tasks | Status |
|------------|------------|---------------------|--------|
| Foundation | 2 | T004-T011 | Ready |
| US-001 (Add) | 6 | T012-T022 | Ready |
| US-002 (View All) | 5 | T023-T033 | Ready |
| US-003 (View Details) | 4 | T034-T043 | Ready |
| US-004 (Update) | 7 | T044-T056 | Ready |
| US-005 (Delete) | 4 | T057-T065 | Ready |
| US-006 (Toggle) | 4 | T066-T074 | Ready |
| **TOTAL** | **32** | **116 tasks** | Ready |

---

## Constitutional Compliance

### Article 2: Spec-Driven Development ✅
- ✅ All tasks trace to spec.md or plan.md
- ✅ Task IDs enable traceability
- ✅ No features outside approved scope

### Article 3: Agent Behavior ✅
- ✅ Tasks are atomic and testable
- ✅ Each task has clear preconditions and outputs
- ✅ Full traceability chain maintained

### Article 4: Phase Governance ✅
- ✅ No Phase II+ features included
- ✅ Only Phase I scope (in-memory, console, basic CRUD)
- ✅ Technology constraints respected (Python stdlib only)

### Article 6.6: TDD Mandate ✅
- ✅ RED-GREEN-REFACTOR cycle followed
- ✅ Tests written before implementation
- ✅ 32 test scenarios covering all user stories
- ✅ Each user story has independent test criteria

---

## Success Criteria

**All 116 tasks completed means:**
- ✅ All 6 user stories (US-001 to US-006) fully implemented
- ✅ 32 unit tests passing with 90%+ coverage
- ✅ Clean architecture with 3-layer separation
- ✅ Full CLI with menu navigation
- ✅ Comprehensive error handling
- ✅ PEP 8 compliant code
- ✅ Type hints and docstrings on all public interfaces
- ✅ Application runs in-memory with no persistence
- ✅ Constitution v2.0.0 fully compliant

---

*Generated from spec.md v1.1.0 and plan.md v1.1.0*
*Complies with Constitution v2.0.0 Article 6.6 (TDD Mandate)*
*Ready for implementation using RED-GREEN-REFACTOR cycle*
