"""Menu controller - Phase I (In-Memory only)."""

import sys
from ..services.task_service import TaskService
from ..exceptions import TodoAppError
from .display import Display
from .input_handler import InputHandler


class Menu:
    """Main menu controller."""

    def __init__(self, task_service: TaskService) -> None:
        """
        Initialize menu with task service.

        Args:
            task_service: TaskService instance for business logic
        """
        self.task_service = task_service

    def main_loop(self) -> None:
        """Run the main menu loop until user exits."""
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
                    Display.error("Invalid choice. Enter 1-6, 0, or 'h' for help.")
            except TodoAppError as e:
                Display.error(str(e))

    def _handle_add(self) -> None:
        """Handle add task operation."""
        print("\n--- Add New Task ---\n")

        title = InputHandler.prompt("Title: ")
        if not title:
            return

        description = InputHandler.prompt("Description (Enter to skip): ")

        task = self.task_service.add_task(title, description)
        print()
        Display.success(f"Task added! ID: {task.short_id}")
        print()

    def _handle_list(self) -> None:
        """Handle list all tasks operation."""
        print()
        tasks = self.task_service.get_all_tasks()
        total, completed = self.task_service.get_task_count()
        Display.task_list(tasks, total, completed)
        print()

    def _handle_view(self) -> None:
        """Handle view task details operation."""
        print("\n--- View Task ---\n")

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return

        task = self.task_service.find_by_partial_id(task_id)
        print()
        Display.task_details(task)
        print()

    def _handle_update(self) -> None:
        """Handle update task operation."""
        print("\n--- Update Task ---\n")

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return

        task = self.task_service.find_by_partial_id(task_id)
        print()
        print(f"Current title: {task.title}")
        new_title = InputHandler.prompt("New title (Enter to keep): ")

        print(f"Current description: {task.description or '(none)'}")
        new_description = InputHandler.prompt("New description (Enter to keep, '-' to clear): ")

        # Handle "keep current" vs "clear" vs "new value"
        title_to_update = new_title if new_title else None
        description_to_update = None
        if new_description == '-':
            description_to_update = ""
        elif new_description:
            description_to_update = new_description

        self.task_service.update_task(task.id, title_to_update, description_to_update)
        print()
        Display.success("Task updated!")
        print()

    def _handle_delete(self) -> None:
        """Handle delete task operation."""
        print("\n--- Delete Task ---\n")

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return

        task = self.task_service.find_by_partial_id(task_id)
        print()

        if InputHandler.confirm(f"Delete \"{task.title}\"? (y/N): "):
            self.task_service.delete_task(task.id)
            print()
            Display.success("Task deleted!")
        else:
            print()
            Display.success("Deletion cancelled.")
        print()

    def _handle_toggle(self) -> None:
        """Handle toggle task completion operation."""
        print("\n--- Toggle Status ---\n")

        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return

        task = self.task_service.find_by_partial_id(task_id)
        updated = self.task_service.toggle_complete(task.id)

        print()
        status = "completed" if updated.completed else "pending"
        Display.success(f"\"{updated.title}\" marked as {status}.")
        print()

    def _handle_help(self) -> None:
        """Handle help display."""
        print()
        Display.help()
        print()

    def _handle_exit(self) -> None:
        """Handle application exit."""
        Display.goodbye()
        sys.exit(0)
