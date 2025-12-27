#!/usr/bin/env python3
"""Console Todo App - Entry Point."""

from src.app import TodoApp


def main() -> None:
    """Initialize and run the application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
