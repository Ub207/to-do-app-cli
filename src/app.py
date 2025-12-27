"""Main application class."""

import signal
import sys

from src.services import TaskService, StorageService
from src.ui import Menu, Display


class TodoApp:
    """Main application orchestrator."""

    def __init__(self, data_file: str = None) -> None:
        """Initialize the application."""
        self.storage = StorageService(data_file)
        self.task_service = TaskService(self.storage)
        self.menu = Menu(self.task_service)
        signal.signal(signal.SIGINT, self._handle_interrupt)

    def run(self) -> None:
        """Start the application."""
        Display.welcome()
        self.menu.main_loop()

    def _handle_interrupt(self, signum, frame) -> None:
        """Handle Ctrl+C gracefully."""
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
