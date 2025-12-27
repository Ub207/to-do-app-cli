"""Priority enumeration for tasks."""

from enum import Enum


class Priority(Enum):
    """
    Task priority levels.

    Ordered for comparison: NONE < LOW < MEDIUM < HIGH
    """
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def display_short(self) -> str:
        """Return short display string for list view."""
        mapping = {
            Priority.NONE: "-",
            Priority.LOW: "LOW",
            Priority.MEDIUM: "MED",
            Priority.HIGH: "HIGH"
        }
        return mapping[self]

    def display_full(self) -> str:
        """Return full display string for detail view."""
        mapping = {
            Priority.NONE: "None",
            Priority.LOW: "Low",
            Priority.MEDIUM: "Medium",
            Priority.HIGH: "High"
        }
        return mapping[self]
