"""Shared test fixtures."""

import pytest
from src.models import Task, Priority


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task for testing."""
    return Task.create("Test Task", "Test Description")


@pytest.fixture
def completed_task() -> Task:
    """Create a completed task for testing."""
    task = Task.create("Completed Task")
    task.completed = True
    task.mark_updated()
    return task
