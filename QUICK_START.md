# Phase I Todo CLI - Quick Start Guide

## 🚀 Running the Application

```bash
python main.py
```

## 📋 Interactive Walkthrough

### Step 1: Add Your First Task
```
Enter choice: 1

--- Add New Task ---

Title: Buy groceries
Description (Enter to skip): Milk, bread, eggs

Task added! ID: a1b2c3d4
```

### Step 2: View All Tasks
```
Enter choice: 2

================================================================================
                          TASKS (1 total, 0 completed)
================================================================================
ID        STATUS  TITLE
--------------------------------------------------------------------------------
a1b2c3d4  [ ]     Buy groceries
================================================================================
Legend: [x] = Completed  [ ] = Pending
```

### Step 3: View Task Details
```
Enter choice: 3

--- View Task ---

Enter task ID: a1b2

================================================================================
                              TASK DETAILS
================================================================================
ID:          a1b2c3d4-e5f6-7890-abcd-ef1234567890
Title:       Buy groceries
Description: Milk, bread, eggs
Status:      Pending
Created:     2025-12-29 03:14:27
Updated:     2025-12-29 03:14:27
================================================================================
```

### Step 4: Mark Task as Complete
```
Enter choice: 6

--- Toggle Status ---

Enter task ID: a1b2

"Buy groceries" marked as completed.
```

### Step 5: Update a Task
```
Enter choice: 4

--- Update Task ---

Enter task ID: a1b2

Current title: Buy groceries
New title (Enter to keep): Buy groceries and snacks
Current description: Milk, bread, eggs
New description (Enter to keep, '-' to clear): Milk, bread, eggs, chips

Task updated!
```

### Step 6: Delete a Task
```
Enter choice: 5

--- Delete Task ---

Enter task ID: a1b2

Delete "Buy groceries and snacks"? (y/N): y

Task deleted!
```

### Step 7: Get Help
```
Enter choice: h

================================================================================
                                     HELP
================================================================================

COMMANDS:
  1  - Add a new task
  2  - List all tasks
  3  - View task details (shows all information for one task)
  4  - Update a task (change title or description)
  5  - Delete a task (permanent, requires confirmation)
  6  - Toggle complete/incomplete status

  0  - Exit the application
  h  - Show this help message

TIPS:
  - Task IDs can be entered partially (first 4+ characters if unique)
  - When updating, press Enter to keep current value, or '-' to clear
  - Use option 2 to see all task IDs before other operations

================================================================================
```

### Step 8: Exit
```
Enter choice: 0

Goodbye! Your tasks were stored in memory only and have been discarded.
```

---

## 🎯 Features Available

| Feature | Command | Description |
|---------|---------|-------------|
| **Add Task** | 1 | Create new task with title and optional description |
| **List Tasks** | 2 | View all tasks with ID, status, and title |
| **View Details** | 3 | See full task information (supports partial ID) |
| **Update Task** | 4 | Modify title or description |
| **Delete Task** | 5 | Remove task (requires confirmation) |
| **Toggle Status** | 6 | Mark complete/incomplete |
| **Help** | h | Show command reference |
| **Exit** | 0 | Quit application |

---

## ✅ Phase I Specifications

**Scope:**
- ✅ In-memory storage only (no persistence)
- ✅ Single user
- ✅ Console-based interface
- ✅ Basic CRUD operations
- ✅ Python standard library only

**NOT Included (Phase II+):**
- ❌ File or database persistence
- ❌ Priority levels
- ❌ Tags/categories
- ❌ Due dates
- ❌ Search/filter/sort
- ❌ Recurring tasks

---

## 🧪 Testing Tips

**Try these scenarios:**

1. **Add multiple tasks** - Create 5-10 tasks to test list display
2. **Partial IDs** - Use only first 4-6 characters of task ID
3. **Empty inputs** - Press Enter without typing to cancel operations
4. **Update with '-'** - Clear description by entering '-'
5. **Toggle repeatedly** - Mark task complete, then incomplete, then complete again
6. **Error handling** - Try invalid task IDs, empty titles, etc.

---

## 📊 What's Working

✅ All 6 user stories fully implemented
✅ Error handling for all edge cases
✅ Clean 3-layer architecture
✅ Type-hinted and documented code
✅ Constitutional compliance verified
✅ No Phase II+ contamination

---

## 🎓 Constitutional Compliance

**Constitution v2.0.0:**
- Article 2: Spec-driven (implements spec v1.1.0)
- Article 3: Full traceability (spec → plan → tasks → code)
- Article 4: Phase I scope only
- Article 5: Python stdlib only
- Article 6: Clean architecture

**Ready for:** Phase II (add persistence) when approved
