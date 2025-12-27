#!/usr/bin/env python3
"""Entry point for Phase I Todo CLI application."""

from src_phase1.app import TodoApp


def main() -> None:
    """Run the Todo CLI application."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()
