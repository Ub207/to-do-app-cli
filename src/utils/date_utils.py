"""Date parsing and formatting utilities."""

from datetime import date, datetime, timedelta
from typing import Optional
import calendar


def parse_date(date_str: str) -> date:
    """Parse YYYY-MM-DD string to date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def format_date(d: date) -> str:
    """Format date as YYYY-MM-DD string."""
    return d.isoformat()


def get_today() -> date:
    """Get today's date."""
    return date.today()


def is_overdue(due_date: Optional[str]) -> bool:
    """Check if a due date is in the past."""
    if due_date is None:
        return False
    return parse_date(due_date) < get_today()


def is_due_today(due_date: Optional[str]) -> bool:
    """Check if a due date is today."""
    if due_date is None:
        return False
    return parse_date(due_date) == get_today()


def is_due_this_week(due_date: Optional[str]) -> bool:
    """Check if a due date is within the next 7 days."""
    if due_date is None:
        return False
    due = parse_date(due_date)
    today = get_today()
    return today <= due <= today + timedelta(days=7)


def calculate_next_due(current_due: str, pattern: str) -> str:
    """Calculate the next due date based on recurrence pattern."""
    due = parse_date(current_due)

    if pattern == "daily":
        new_due = due + timedelta(days=1)
    elif pattern == "weekly":
        new_due = due + timedelta(weeks=1)
    elif pattern == "monthly":
        year = due.year
        month = due.month + 1
        if month > 12:
            month = 1
            year += 1
        day = min(due.day, calendar.monthrange(year, month)[1])
        new_due = date(year, month, day)
    else:
        new_due = due

    return format_date(new_due)


def format_relative(due_date: Optional[str]) -> str:
    """Format due date as relative string."""
    if due_date is None:
        return "-"

    due = parse_date(due_date)
    today = get_today()
    diff = (due - today).days

    if diff < 0:
        return "OVERDUE"
    elif diff == 0:
        return "Today"
    elif diff == 1:
        return "Tomorrow"
    else:
        return due_date
