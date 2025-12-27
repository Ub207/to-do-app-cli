# Spec-Kit-Plus Task Board

> **Console Todo App** — Executable task list for hackathon delivery
> Complete tasks in order. Each phase is a gate — don't skip ahead.
> Total estimated time: ~10-12 hours

---

## 🔴 Phase 1 — Foundation (Blocker - Must do first)

### Project Setup
- [ ] Create `src/` folder with `__init__.py` · Blocker · 5m
- [ ] Create `src/utils/` folder with `__init__.py` · Blocker · 5m
- [ ] Create `src/models/` folder with `__init__.py` · Blocker · 5m
- [ ] Create `src/services/` folder with `__init__.py` · Blocker · 5m
- [ ] Create `src/ui/` folder with `__init__.py` · Blocker · 5m
- [ ] Create `tests/` folder with `__init__.py` · Blocker · 5m
- [ ] Create `data/` folder with `.gitkeep` · Blocker · 5m

### Constants & Exceptions
- [ ] Create `src/utils/constants.py` with all validation limits (MAX_TITLE=200, MAX_DESC=2000, etc.) · Blocker · 15m
- [ ] Create `src/utils/constants.py` with file paths (DATA_DIR, DEFAULT_DATA_FILE, BACKUP_SUFFIX) · Blocker · 10m
- [ ] Create `src/utils/constants.py` with display constants (SHORT_ID_LENGTH=8, DATE_FORMAT, etc.) · Blocker · 10m
- [ ] Create `src/exceptions.py` with `TodoAppError` base class · Blocker · 5m
- [ ] Add `ValidationError(TodoAppError)` exception · Blocker · 5m
- [ ] Add `TaskNotFoundError(TodoAppError)` exception · Blocker · 5m
- [ ] Add `AmbiguousIdError(TodoAppError)` exception · Blocker · 5m
- [ ] Add `StorageError(TodoAppError)` exception · Blocker · 5m

### Priority Enum
- [ ] Create `src/models/priority.py` with `Priority(Enum)` class (NONE=0, LOW=1, MEDIUM=2, HIGH=3) · Blocker · 10m
- [ ] Add `display_short()` method returning "-", "LOW", "MED", "HIGH" · Blocker · 10m
- [ ] Add `display_full()` method returning "None", "Low", "Medium", "High" · Blocker · 5m

### Task Model
- [ ] Create `src/models/task.py` with `@dataclass` Task class · Blocker · 15m
- [ ] Add all Task fields: id, title, description, completed, priority, tags, created_at, updated_at, due_date, recurring · Blocker · 15m
- [ ] Implement `__post_init__()` to auto-set timestamps if empty · Blocker · 10m
- [ ] Implement `Task.create(title, description)` factory method with UUID generation · Blocker · 15m
- [ ] Implement `to_dict()` method for JSON serialization · Blocker · 15m
- [ ] Implement `from_dict(data)` classmethod for JSON deserialization · Blocker · 15m
- [ ] Implement `mark_updated()` method to refresh updated_at timestamp · Blocker · 5m
- [ ] Implement `short_id` property returning first 8 chars of ID · Blocker · 5m
- [ ] Update `src/models/__init__.py` to export Task and Priority · Blocker · 5m

### Phase 1 Tests
- [ ] Create `tests/conftest.py` with sample_task and completed_task fixtures · Blocker · 10m
- [ ] Create `tests/test_priority.py` with test for enum ordering · Blocker · 10m
- [ ] Add test for `display_short()` output · Blocker · 5m
- [ ] Add test for `display_full()` output · Blocker · 5m
- [ ] Create `tests/test_task.py` with test_create_with_title_only · Blocker · 10m
- [ ] Add test_create_with_description · Blocker · 5m
- [ ] Add test_create_strips_whitespace · Blocker · 5m
- [ ] Add test_short_id_returns_first_8_chars · Blocker · 5m
- [ ] Add test_mark_updated_changes_timestamp · Blocker · 10m
- [ ] Add test_to_dict_serialization · Blocker · 10m
- [ ] Add test_from_dict_deserialization · Blocker · 10m
- [ ] Add test_to_dict_from_dict_roundtrip · Blocker · 10m
- [ ] Run `python -m pytest tests/test_priority.py tests/test_task.py -v` and verify all pass · Blocker · 5m

**🎯 Phase 1 Gate:** All model tests pass. Run: `python -c "from src.models import Task, Priority"` without errors.

---

## 🟠 Phase 2 — Basic MVP Features (High Priority)

### Storage Service
- [ ] Create `src/services/storage_service.py` with `StorageService` class · High · 10m
- [ ] Add `__init__(file_path)` with default to `data/tasks.json` · High · 10m
- [ ] Implement `load()` method: create data/ dir if missing · High · 15m
- [ ] Implement `load()` method: create empty JSON if file missing · High · 15m
- [ ] Implement `load()` method: parse JSON and return list of Task objects · High · 15m
- [ ] Implement `load()` method: handle JSONDecodeError → backup corrupted file, start fresh · High · 20m
- [ ] Implement `load()` method: handle PermissionError → set memory_only_mode, warn user · High · 15m
- [ ] Implement `save(tasks)` method: write to temp file first · High · 15m
- [ ] Implement `save(tasks)` method: backup existing file before overwrite · High · 10m
- [ ] Implement `save(tasks)` method: atomic rename temp → main file · High · 10m
- [ ] Implement `_create_empty_file()` helper method · High · 10m
- [ ] Update `src/services/__init__.py` to export StorageService · High · 5m

### Task Service - Core CRUD
- [ ] Create `src/services/task_service.py` with `TaskService` class · High · 10m
- [ ] Add `__init__(storage)` that loads tasks on creation · High · 10m
- [ ] Implement `_load_tasks()` private method · High · 5m
- [ ] Implement `_save_tasks()` private method · High · 5m
- [ ] Implement `add_task(title, description)` with validation · High · 20m
- [ ] Implement `get_all_tasks()` returning sorted by created_at desc · High · 10m
- [ ] Implement `get_task_count()` returning (total, completed) tuple · High · 10m
- [ ] Implement `find_by_partial_id(partial_id)` with 4+ char minimum · High · 20m
- [ ] Handle AmbiguousIdError when multiple tasks match partial ID · High · 15m
- [ ] Implement `update_task(task_id, title, description)` · High · 20m
- [ ] Implement `delete_task(task_id)` · High · 15m
- [ ] Implement `toggle_complete(task_id)` · High · 15m
- [ ] Update `src/services/__init__.py` to export TaskService · High · 5m

### Display Module
- [ ] Create `src/ui/display.py` with `Display` class · High · 10m
- [ ] Add SEPARATOR and LINE class constants (80 chars) · High · 5m
- [ ] Implement `welcome()` static method with banner · High · 10m
- [ ] Implement `menu_level_1()` static method with 6 options + exit + help · High · 15m
- [ ] Implement `task_list(tasks, total, completed)` with formatted table · High · 30m
- [ ] Implement `task_details(task)` with all fields displayed · High · 20m
- [ ] Implement `help_level_1()` with command descriptions · High · 15m
- [ ] Implement `success(message)`, `error(message)`, `warning(message)` helpers · High · 10m
- [ ] Implement `goodbye()` exit message · High · 5m

### Input Handler Module
- [ ] Create `src/ui/input_handler.py` with `InputHandler` class · High · 10m
- [ ] Implement `prompt(message)` returning stripped input · High · 5m
- [ ] Implement `confirm(message)` returning True only for 'y'/'Y' · High · 10m
- [ ] Implement `menu_choice()` returning lowercase stripped choice · High · 5m
- [ ] Implement `wait_for_enter()` for "Press Enter to continue" · High · 5m

### Menu Module
- [ ] Create `src/ui/menu.py` with `Menu` class · High · 10m
- [ ] Add `__init__(task_service)` storing service reference · High · 5m
- [ ] Implement `main_loop()` with while True and choice routing · High · 20m
- [ ] Implement `_handle_exit()` with goodbye message and sys.exit(0) · High · 10m
- [ ] Implement `_handle_help()` displaying help and waiting for Enter · High · 10m
- [ ] Implement `_handle_add()` prompting for title and description · High · 20m
- [ ] Implement `_handle_list()` showing all tasks · High · 15m
- [ ] Implement `_handle_view()` prompting for ID and showing details · High · 20m
- [ ] Implement `_handle_update()` with current value display and optional update · High · 25m
- [ ] Implement `_handle_delete()` with confirmation prompt · High · 20m
- [ ] Implement `_handle_toggle()` flipping completion status · High · 15m
- [ ] Update `src/ui/__init__.py` to export Display, InputHandler, Menu · High · 5m

### App & Entry Point
- [ ] Create `src/app.py` with `TodoApp` class · High · 10m
- [ ] Add `__init__()` creating StorageService, TaskService, Menu · High · 15m
- [ ] Add signal handler for Ctrl+C (SIGINT) · High · 15m
- [ ] Implement `run()` method showing welcome and starting menu loop · High · 10m
- [ ] Create `main.py` entry point importing and running TodoApp · High · 10m

### Phase 2 Manual Testing
- [ ] Run app: `python main.py` — verify welcome banner shows · High · 5m
- [ ] Test Option 1: Add task with title only · High · 5m
- [ ] Test Option 1: Add task with title + description · High · 5m
- [ ] Test Option 1: Try empty title → should show error · High · 5m
- [ ] Test Option 2: List tasks → should show added tasks · High · 5m
- [ ] Test Option 3: View task by partial ID (4+ chars) · High · 5m
- [ ] Test Option 4: Update task title · High · 5m
- [ ] Test Option 4: Update description · High · 5m
- [ ] Test Option 4: Clear description with '-' · High · 5m
- [ ] Test Option 5: Delete task (confirm yes) · High · 5m
- [ ] Test Option 5: Delete task (confirm no) → should cancel · High · 5m
- [ ] Test Option 6: Toggle to completed · High · 5m
- [ ] Test Option 6: Toggle back to pending · High · 5m
- [ ] Test Option h: Show help · High · 5m
- [ ] Test Option 0: Exit gracefully · High · 5m
- [ ] Restart app → verify tasks persist from JSON · High · 5m

**🎯 Phase 2 Gate:** All 6 menu options work. Tasks survive restart. No crashes on invalid input.

---

## 🟡 Phase 3 — Persistence & Robustness (High)

### Storage Robustness
- [ ] Create `tests/test_storage_service.py` · High · 10m
- [ ] Add test_save_and_load_roundtrip · High · 15m
- [ ] Add test_load_nonexistent_file_creates_empty · High · 15m
- [ ] Add test_load_corrupted_file_recovers · High · 15m
- [ ] Add test_backup_created_on_save · High · 15m
- [ ] Run storage tests and verify all pass · High · 5m

### Enhanced Error Handling
- [ ] Add try/except around all menu handlers catching TodoAppError · High · 15m
- [ ] Verify error messages start with "Error: " prefix · High · 10m
- [ ] Verify empty list shows friendly "No tasks yet!" message · High · 10m
- [ ] Test with non-existent task ID → should show clear error · High · 5m
- [ ] Test with ambiguous partial ID → should ask for more specific · High · 5m

### Display Improvements
- [ ] Truncate long titles in list view at 35 chars with "..." · High · 15m
- [ ] Show "(no description)" for empty description in detail view · High · 5m
- [ ] Show "(no tags)" for empty tags in detail view · High · 5m
- [ ] Add legend at bottom of task list explaining symbols · High · 10m

**🎯 Phase 3 Gate:** Storage tests pass. Error messages are user-friendly. Display is clean.

---

## 🔵 Phase 4 — Intermediate Features (Medium+)

### Priority Support
- [ ] Add `set_priority(task_id, priority)` to TaskService · Medium · 15m
- [ ] Add Option 7 to menu: "Set priority" · Medium · 10m
- [ ] Implement `_handle_set_priority()` in Menu with sub-menu (1-4) · Medium · 20m
- [ ] Update task list display to show priority column · Medium · 10m

### Tags Support
- [ ] Add tag validation regex `^[a-z0-9][a-z0-9-]{0,49}$` to constants · Medium · 5m
- [ ] Add `add_tag(task_id, tag)` to TaskService with validation · Medium · 20m
- [ ] Add `remove_tag(task_id, tag)` to TaskService · Medium · 15m
- [ ] Add `get_all_tags()` to TaskService · Medium · 10m
- [ ] Add Option 8 to menu: "Add tag" · Medium · 10m
- [ ] Add Option 9 to menu: "Remove tag" · Medium · 10m
- [ ] Implement `_handle_add_tag()` with current tags display · Medium · 20m
- [ ] Implement `_handle_remove_tag()` with numbered tag list · Medium · 20m

### Search Feature
- [ ] Add `search(query)` to TaskService with 2+ char minimum · Medium · 20m
- [ ] Search in title (priority 1), description (priority 2), tags (priority 3) · Medium · 15m
- [ ] Add Option 10 to menu: "Search tasks" · Medium · 10m
- [ ] Implement `_handle_search()` showing results in list format · Medium · 20m

### Filter Feature
- [ ] Add `filter_by_status(completed)` to TaskService · Medium · 10m
- [ ] Add `filter_by_priority(priority)` to TaskService · Medium · 10m
- [ ] Add `filter_by_tag(tag)` to TaskService · Medium · 10m
- [ ] Add Option 11 to menu: "Filter tasks" · Medium · 10m
- [ ] Implement `_handle_filter()` with sub-menu (status/priority/tag/show all) · Medium · 30m

### Sort Feature
- [ ] Add `sort_tasks(tasks, sort_key, reverse)` to TaskService · Medium · 20m
- [ ] Support sort keys: priority, priority_asc, due_date, title, created · Medium · 15m
- [ ] Add Option 12 to menu: "Sort tasks" · Medium · 10m
- [ ] Implement `_handle_sort()` with 8 sort options · Medium · 25m

### Update Menu Display
- [ ] Create `menu_level_2()` in Display showing options 1-12 in columns · Medium · 20m
- [ ] Update main_loop to handle choices 7-12 · Medium · 15m
- [ ] Update help to include Level 2 commands · Medium · 15m

### Phase 4 Tests
- [ ] Add test_set_priority to TaskService tests · Medium · 10m
- [ ] Add test_add_tag_valid and test_add_tag_invalid · Medium · 15m
- [ ] Add test_remove_tag · Medium · 10m
- [ ] Add test_search_finds_in_title · Medium · 10m
- [ ] Add test_search_case_insensitive · Medium · 10m
- [ ] Add test_filter_by_status_completed · Medium · 10m
- [ ] Run all Phase 4 tests · Medium · 5m

**🎯 Phase 4 Gate:** Options 7-12 work. Tags lowercase, max 10. Search min 2 chars. Filters work.

---

## 🟣 Phase 5 — Advanced Features (Bonus)

### Date Utilities
- [ ] Create `src/utils/date_utils.py` · Bonus · 10m
- [ ] Implement `parse_date(date_str)` returning date object · Bonus · 10m
- [ ] Implement `format_date(d)` returning YYYY-MM-DD string · Bonus · 5m
- [ ] Implement `is_overdue(due_date)` returning bool · Bonus · 10m
- [ ] Implement `is_due_today(due_date)` returning bool · Bonus · 10m
- [ ] Implement `is_due_this_week(due_date)` returning bool · Bonus · 10m
- [ ] Implement `calculate_next_due(current, pattern)` for recurring · Bonus · 20m
- [ ] Implement `format_relative(due_date)` returning Today/Tomorrow/OVERDUE/date · Bonus · 15m

### Due Date Support
- [ ] Add `set_due_date(task_id, due_date)` to TaskService · Bonus · 15m
- [ ] Add `clear_due_date(task_id)` to TaskService (also clears recurring) · Bonus · 15m
- [ ] Add `get_overdue()` to TaskService · Bonus · 15m
- [ ] Add `get_due_today()` to TaskService · Bonus · 10m
- [ ] Add `get_due_this_week()` to TaskService · Bonus · 15m
- [ ] Add Option 13 to menu: "Set due date" · Bonus · 10m
- [ ] Add Option 14 to menu: "Clear due date" · Bonus · 10m
- [ ] Add Option 15 to menu: "Show overdue" · Bonus · 10m
- [ ] Add Option 16 to menu: "Show due today" · Bonus · 10m
- [ ] Add Option 17 to menu: "Show due this week" · Bonus · 10m
- [ ] Implement all 5 due date handlers in Menu · Bonus · 1h
- [ ] Add past date warning with confirmation prompt · Bonus · 15m

### Recurring Tasks
- [ ] Add `set_recurring(task_id, pattern)` to TaskService · Bonus · 20m
- [ ] Validate pattern is daily/weekly/monthly or None · Bonus · 10m
- [ ] Require due_date before setting recurring · Bonus · 10m
- [ ] Add `handle_recurring_completion(task)` to TaskService · Bonus · 30m
- [ ] Update `toggle_complete()` to call handle_recurring_completion · Bonus · 15m
- [ ] Add Option 18 to menu: "Set recurring" · Bonus · 10m
- [ ] Implement `_handle_set_recurring()` with sub-menu · Bonus · 20m

### Startup Reminders
- [ ] Add `_check_reminders()` to TodoApp · Bonus · 15m
- [ ] Display overdue tasks count and list on startup · Bonus · 20m
- [ ] Display due today tasks count and list on startup · Bonus · 15m
- [ ] Add "Press Enter to continue" after reminders · Bonus · 5m
- [ ] Only show reminder panel if there ARE overdue/due-today tasks · Bonus · 10m

### Update Menu Display
- [ ] Create `menu_level_3()` in Display showing options 1-18 in columns · Bonus · 20m
- [ ] Update main_loop to handle choices 13-18 · Bonus · 15m
- [ ] Update help to include Level 3 commands · Bonus · 15m

**🎯 Phase 5 Gate:** Due dates work with validation. Recurring creates new instance. Reminders show on startup.

---

## 🟢 Phase 6 — Final Polish & Testing (High)

### Comprehensive Tests
- [ ] Create `tests/test_validators.py` if validators.py exists · High · 15m
- [ ] Create `tests/test_date_utils.py` for all date functions · High · 30m
- [ ] Create `tests/test_integration.py` · High · 15m
- [ ] Add test_full_crud_workflow (add → list → view → update → complete → delete) · High · 30m
- [ ] Add test_persistence_round_trip (add → exit → restart → verify) · High · 20m
- [ ] Run full test suite: `python -m pytest tests/ -v` · High · 10m
- [ ] Check coverage: `python -m pytest --cov=src tests/` · High · 10m
- [ ] Add tests for any coverage gaps to reach 85%+ · High · 30m

### Code Quality
- [ ] Add docstrings to all public methods missing them · High · 30m
- [ ] Verify all functions have type hints · High · 20m
- [ ] Run PEP 8 check (flake8 or pylint) · High · 15m
- [ ] Fix any PEP 8 violations · High · 20m
- [ ] Remove any debug print statements · High · 10m
- [ ] Verify no hardcoded values (all in constants.py) · High · 15m

### Documentation
- [ ] Create `README.md` with project description · High · 15m
- [ ] Add installation instructions (Python 3.10+ required) · High · 10m
- [ ] Add usage instructions with example commands · High · 20m
- [ ] Add feature list by level · High · 15m
- [ ] Add example session transcript · High · 20m

### Final Verification
- [ ] Fresh clone test: delete data/, run app, verify it creates new file · High · 10m
- [ ] Test all 18 menu options work (if Level 3 implemented) · High · 30m
- [ ] Test Ctrl+C handling (graceful exit) · High · 5m
- [ ] Verify no crashes on any invalid input · High · 15m
- [ ] Run final test suite one more time · High · 5m

**🎯 Phase 6 Gate:** 85%+ test coverage. README complete. All features work. Clean code.

---

## 📊 Summary

| Phase | Tasks | Est. Time | Priority |
|-------|-------|-----------|----------|
| Phase 1 | 40 | ~3h | 🔴 Blocker |
| Phase 2 | 52 | ~4h | 🟠 High |
| Phase 3 | 15 | ~1.5h | 🟡 High |
| Phase 4 | 35 | ~2.5h | 🔵 Medium |
| Phase 5 | 32 | ~3h | 🟣 Bonus |
| Phase 6 | 20 | ~2h | 🟢 High |
| **Total** | **194** | **~16h** | |

---

## 🚀 Quick Start Commands

```bash
# Run the app
python main.py

# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Check PEP 8
python -m flake8 src/ --max-line-length=100
```

---

## ✅ Definition of Done

A task is complete when:
1. Code is written and saved
2. No syntax errors
3. Related tests pass (if applicable)
4. Feature works when manually tested
5. No regressions in existing features

---

**Version:** 1.0.0
**Generated from:** constitution.md v1.0.0, .specify v2.0.0, IMPLEMENTATION_PLAN.md v1.0.0
