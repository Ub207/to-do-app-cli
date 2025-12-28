"""Application bootstrap - Phase I (In-Memory only)."""

from .services.task_service import TaskService
from .ui.menu import Menu
from .ui.display import Display


class TodoApp:
    """Main application class for Todo CLI."""

    def __init__(self) -> None:
        """Initialize application with task service and menu."""
        self.task_service = TaskService()
        self.menu = Menu(self.task_service)

    def run(self) -> None:
        """Run the application."""
        Display.welcome()
        self.menu.main_loop()
