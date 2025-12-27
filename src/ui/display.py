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
    def menu_level_2() -> None:
        """Display Level 2 menu with all features."""
        print(Display.SEPARATOR)
        print(f"{'MAIN MENU':^80}")
        print(Display.SEPARATOR)
        print("  BASIC                ORGANIZE              FIND              DATES")
        print("  1. Add task          7. Set priority       10. Search        13. Set due")
        print("  2. List tasks        8. Add tag            11. Filter        14. Clear due")
        print("  3. View task         9. Remove tag         12. Sort          15. Overdue")
        print("  4. Update task                                               16. Due today")
        print("  5. Delete task       0. Exit | h. Help                       17. Due week")
        print("  6. Toggle complete                                           18. Recurring")
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
    def help_level_2() -> None:
        """Display Level 2 help with all features."""
        print(Display.SEPARATOR)
        print(f"{'HELP':^80}")
        print(Display.SEPARATOR)
        print()
        print("BASIC:                    ORGANIZE:                 FIND:")
        print("  1 - Add task            7 - Set priority          10 - Search")
        print("  2 - List tasks          8 - Add tag               11 - Filter")
        print("  3 - View task           9 - Remove tag            12 - Sort")
        print("  4 - Update task")
        print("  5 - Delete task         0 - Exit | h - Help")
        print("  6 - Toggle complete")
        print()
        print("TIPS:")
        print("  - Task IDs: Enter first 4+ chars if unique")
        print("  - Tags: lowercase letters, numbers, hyphens only (max 10 per task)")
        print("  - Search: min 2 characters, searches title/description/tags")
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
