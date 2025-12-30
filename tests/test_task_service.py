"""Tests for TaskService - Phase I (In-Memory only)."""

import unittest
from src.services.task_service import TaskService
from src.exceptions import ValidationError, TaskNotFoundError, AmbiguousIdError


class TestTaskService(unittest.TestCase):
    """Test TaskService operations."""

    def setUp(self):
        """Create fresh service for each test."""
        self.service = TaskService()

    def test_add_task_returns_task_with_id(self):
        """add_task should return task with generated ID."""
        task = self.service.add_task("Test Task")
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(len(task.id), 36)  # UUID format

    def test_add_task_strips_whitespace(self):
        """add_task should strip whitespace from title."""
        task = self.service.add_task("  Test Task  ")
        self.assertEqual(task.title, "Test Task")

    def test_add_task_empty_title_raises_error(self):
        """add_task should raise ValidationError for empty title."""
        with self.assertRaises(ValidationError):
            self.service.add_task("")

    def test_add_task_whitespace_only_raises_error(self):
        """add_task should raise ValidationError for whitespace-only title."""
        with self.assertRaises(ValidationError):
            self.service.add_task("   ")

    def test_get_all_tasks_empty(self):
        """get_all_tasks should return empty list initially."""
        tasks = self.service.get_all_tasks()
        self.assertEqual(tasks, [])

    def test_get_all_tasks_returns_all(self):
        """get_all_tasks should return all added tasks."""
        self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        
        tasks = self.service.get_all_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_task_by_id(self):
        """get_task should return task by ID."""
        created = self.service.add_task("Test")
        
        found = self.service.get_task(created.id)
        self.assertEqual(found.id, created.id)

    def test_get_task_not_found(self):
        """get_task should raise TaskNotFoundError for invalid ID."""
        with self.assertRaises(TaskNotFoundError):
            self.service.get_task("invalid-id")

    def test_find_by_partial_id(self):
        """find_by_partial_id should find task by prefix."""
        created = self.service.add_task("Test")
        partial = created.id[:8]
        
        found = self.service.find_by_partial_id(partial)
        self.assertEqual(found.id, created.id)

    def test_update_task_title(self):
        """update_task should update title."""
        task = self.service.add_task("Original")
        
        updated = self.service.update_task(task.id, title="Updated")
        self.assertEqual(updated.title, "Updated")

    def test_update_task_description(self):
        """update_task should update description."""
        task = self.service.add_task("Test", "Original desc")
        
        updated = self.service.update_task(task.id, description="New desc")
        self.assertEqual(updated.description, "New desc")

    def test_delete_task(self):
        """delete_task should remove task."""
        task = self.service.add_task("Test")
        
        self.service.delete_task(task.id)
        
        with self.assertRaises(TaskNotFoundError):
            self.service.get_task(task.id)

    def test_toggle_complete(self):
        """toggle_complete should flip completion status."""
        task = self.service.add_task("Test")
        self.assertFalse(task.completed)
        
        toggled = self.service.toggle_complete(task.id)
        self.assertTrue(toggled.completed)
        
        toggled_again = self.service.toggle_complete(task.id)
        self.assertFalse(toggled_again.completed)

    def test_get_task_count(self):
        """get_task_count should return correct counts."""
        self.assertEqual(self.service.get_task_count(), (0, 0))
        
        task1 = self.service.add_task("Task 1")
        self.service.add_task("Task 2")
        self.service.toggle_complete(task1.id)
        
        self.assertEqual(self.service.get_task_count(), (2, 1))


if __name__ == "__main__":
    unittest.main()
