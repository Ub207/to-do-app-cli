"""Menu controller for CLI interface."""

import sys

from src_phase1.services import TaskService
from src_phase1.exceptions import TodoAppError
from src_phase1.ui.display import Display
from src_phase1.ui.input_handler import InputHandler


class Menu:
    """Main menu controller."""

    def __init__(self, task_service: TaskService) -> None:
        """Initialize menu with task service.

        Args:
            task_service: Service for task operations.
        """
        self.task_service = task_service

    def main_loop(self) -> None:
        """Run the main menu loop until exit."""
        while True:
            Display.menu()
            choice = InputHandler.menu_choice()

            try:
                if choice in ["0", "q", "quit", "exit"]:
                    self._handle_exit()
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

            print()

    def _handle_exit(self) -> None:
        """Handle exit command."""
        Display.goodbye()
        sys.exit(0)

    def _handle_help(self) -> None:
        """Handle help command."""
        Display.help()

    def _handle_add(self) -> None:
        """Handle add task command."""
        print("--- Add New Task ---\n")
        title = InputHandler.prompt("Title: ")
        if not title:
            Display.error("Title cannot be empty.")
            return
        description = InputHandler.prompt("Description (Enter to skip): ")
        task = self.task_service.add_task(title, description)
        Display.success(f"\nTask added! ID: {task.short_id}")

    def _handle_list(self) -> None:
        """Handle list tasks command."""
        tasks = self.task_service.get_all_tasks()
        total, completed = self.task_service.get_task_count()
        Display.task_list(tasks, total, completed)

    def _handle_view(self) -> None:
        """Handle view task details command."""
        print("--- View Task ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            Display.error("Task ID cannot be empty.")
            return
        task = self.task_service.find_by_partial_id(task_id)
        Display.task_details(task)

    def _handle_update(self) -> None:
        """Handle update task command."""
        print("--- Update Task ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)

        print(f"\nCurrent title: {task.title}")
        new_title = InputHandler.prompt("New title (Enter to keep): ")

        print(f"Current description: {task.description or '(none)'}")
        new_desc = InputHandler.prompt("New description (Enter to keep, '-' to clear): ")

        title_to_set = new_title if new_title else None
        desc_to_set = "" if new_desc == "-" else (new_desc if new_desc else None)

        self.task_service.update_task(task.id, title_to_set, desc_to_set)
        Display.success("\nTask updated!")

    def _handle_delete(self) -> None:
        """Handle delete task command."""
        print("--- Delete Task ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)

        if not InputHandler.confirm(f'\nDelete "{task.title}"? (y/N): '):
            print("Cancelled.")
            return

        self.task_service.delete_task(task.id)
        Display.success("\nTask deleted!")

    def _handle_toggle(self) -> None:
        """Handle toggle complete command."""
        print("--- Toggle Status ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.toggle_complete(
            self.task_service.find_by_partial_id(task_id).id
        )
        status = "completed" if task.completed else "pending"
        Display.success(f'\n"{task.title}" marked as {status}.')
