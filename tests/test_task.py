"""Tests for Task model - Phase I (In-Memory only)."""

import unittest
import time
from src.models import Task


class TestTask(unittest.TestCase):
    """Test Task dataclass."""

    def test_create_task_with_title(self):
        """Task can be created with just title."""
        task = Task(title="Buy milk")

        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertEqual(len(task.id), 36)  # UUID format
        self.assertNotEqual(task.created_at, "")
        self.assertNotEqual(task.updated_at, "")

    def test_create_task_with_description(self):
        """Task can be created with title and description."""
        task = Task(title="Buy groceries", description="Milk, eggs, bread")

        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, eggs, bread")

    def test_short_id_returns_first_8_chars(self):
        """short_id property returns first 8 characters."""
        task = Task(title="Test")

        self.assertEqual(len(task.short_id), 8)
        self.assertTrue(task.id.startswith(task.short_id))

    def test_task_defaults_to_not_completed(self):
        """New tasks should default to not completed."""
        task = Task(title="Test")
        self.assertFalse(task.completed)

    def test_task_can_be_marked_completed(self):
        """Task can be marked as completed."""
        task = Task(title="Test", completed=True)
        self.assertTrue(task.completed)

    def test_unique_ids_for_each_task(self):
        """Each task should have a unique ID."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        self.assertNotEqual(task1.id, task2.id)

    def test_task_timestamps_set_automatically(self):
        """Task should have timestamps set on creation."""
        task = Task(title="Test")
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)


if __name__ == "__main__":
    unittest.main()
