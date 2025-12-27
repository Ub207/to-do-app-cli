"""Main application class."""

from src_phase1.services import TaskService
from src_phase1.ui import Menu, Display


class TodoApp:
    """Main application class for Todo CLI."""

    def __init__(self) -> None:
        """Initialize the application."""
        self.task_service = TaskService()
        self.menu = Menu(self.task_service)

    def run(self) -> None:
        """Run the application."""
        Display.welcome()
        self.menu.main_loop()
