"""Output formatting functions - Phase I (In-Memory only)."""

from ..models.task import Task


class Display:
    """Static methods for all output formatting."""

    SEPARATOR = "=" * 80
    LINE = "-" * 80

    @staticmethod
    def welcome() -> None:
        """Display application banner."""
        print(Display.SEPARATOR)
        print(f"{'CONSOLE TODO APP v1.0.0':^80}")
        print(Display.SEPARATOR)
        print()

    @staticmethod
    def menu() -> None:
        """Display main menu options."""
        print(Display.SEPARATOR)
        print(f"{'MAIN MENU':^80}")
        print(Display.SEPARATOR)
        print("  1. Add task              4. Update task")
        print("  2. List all tasks        5. Delete task")
        print("  3. View task details     6. Mark complete/incomplete")
        print()
        print("                           0. Exit")
        print("                           h. Help")
        print(Display.LINE)

    @staticmethod
    def task_list(tasks: list[Task], total: int, completed: int) -> None:
        """
        Display formatted task list.

        Args:
            tasks: List of tasks to display
            total: Total task count
            completed: Completed task count
        """
        print(Display.SEPARATOR)
        print(f"TASKS ({total} total, {completed} completed)".center(80))
        print(Display.SEPARATOR)

        if not tasks:
            print()
            print("  No tasks yet! Use option 1 to add your first task.")
            print()
        else:
            print(f"{'ID':<10}{'STATUS':<8}{'TITLE'}")
            print(Display.LINE)

            for task in tasks:
                status = "[x]" if task.completed else "[ ]"
                title = task.title[:60]
                if len(task.title) > 60:
                    title = title[:57] + "..."

                print(f"{task.short_id:<10}{status:<8}{title}")

        print(Display.SEPARATOR)
        print("Legend: [x] = Completed  [ ] = Pending")

    @staticmethod
    def task_details(task: Task) -> None:
        """
        Display full task details.

        Args:
            task: Task to display
        """
        print(Display.SEPARATOR)
        print(f"{'TASK DETAILS':^80}")
        print(Display.SEPARATOR)
        print(f"ID:          {task.id}")
        print(f"Title:       {task.title}")
        print(f"Description: {task.description or '(no description)'}")
        print(f"Status:      {'Completed' if task.completed else 'Pending'}")
        print(f"Created:     {task.created_at.replace('T', ' ')}")
        print(f"Updated:     {task.updated_at.replace('T', ' ')}")
        print(Display.SEPARATOR)

    @staticmethod
    def help() -> None:
        """Display help information."""
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
        print("  - Use option 2 to see all task IDs before other operations")
        print()
        print(Display.SEPARATOR)

    @staticmethod
    def success(message: str) -> None:
        """
        Display success message.

        Args:
            message: Success message to display
        """
        print(message)

    @staticmethod
    def error(message: str) -> None:
        """
        Display error message with 'Error: ' prefix.

        Args:
            message: Error message to display
        """
        print(f"Error: {message}")

    @staticmethod
    def goodbye() -> None:
        """Display exit message."""
        print()
        print("Goodbye! Your tasks were stored in memory only and have been discarded.")
        print()
