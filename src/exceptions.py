"""Custom exception classes for the Todo App - Phase I."""


class TodoAppError(Exception):
    """Base exception for all application errors."""
    pass


class ValidationError(TodoAppError):
    """Raised when user input fails validation."""
    pass


class TaskNotFoundError(TodoAppError):
    """Raised when a task ID doesn't match any task."""
    pass


class AmbiguousIdError(TodoAppError):
    """Raised when a partial task ID matches multiple tasks."""
    pass
