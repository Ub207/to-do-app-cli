"""Custom exceptions for Todo CLI application."""


class TodoAppError(Exception):
    """Base exception for all application errors."""

    pass


class TaskNotFoundError(TodoAppError):
    """Raised when task ID doesn't match any task."""

    pass


class AmbiguousIdError(TodoAppError):
    """Raised when partial ID matches multiple tasks."""

    pass


class ValidationError(TodoAppError):
    """Raised when input fails validation."""

    pass
