"""Shared test fixtures - Phase I (In-Memory only)."""

import pytest
from src.models import Task


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task for testing."""
    return Task(title="Test Task", description="Test Description")


@pytest.fixture
def completed_task() -> Task:
    """Create a completed task for testing."""
    return Task(title="Completed Task", completed=True)
