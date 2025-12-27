"""Tests for Task model."""

import unittest
import time
from src.models import Task, Priority


class TestTask(unittest.TestCase):
    """Test Task dataclass."""

    def test_create_with_title_only(self):
        """Task can be created with just title."""
        task = Task.create("Buy milk")

        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, Priority.NONE)
        self.assertEqual(task.tags, [])
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.recurring)
        self.assertEqual(len(task.id), 36)  # UUID format
        self.assertNotEqual(task.created_at, "")
        self.assertNotEqual(task.updated_at, "")

    def test_create_with_description(self):
        """Task can be created with title and description."""
        task = Task.create("Buy groceries", "Milk, eggs, bread")

        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(task.description, "Milk, eggs, bread")

    def test_create_strips_whitespace(self):
        """Title and description should be stripped of whitespace."""
        task = Task.create("  Buy milk  ", "  Get 2%  ")

        self.assertEqual(task.title, "Buy milk")
        self.assertEqual(task.description, "Get 2%")

    def test_short_id_returns_first_8_chars(self):
        """short_id property returns first 8 characters."""
        task = Task.create("Test")

        self.assertEqual(len(task.short_id), 8)
        self.assertTrue(task.id.startswith(task.short_id))

    def test_mark_updated_changes_timestamp(self):
        """mark_updated() should update the updated_at field."""
        task = Task.create("Test")
        old_updated = task.updated_at

        time.sleep(1.1)  # Delay to ensure different timestamp (second granularity)
        task.mark_updated()

        self.assertGreater(task.updated_at, old_updated)

    def test_to_dict_serialization(self):
        """to_dict() should serialize all fields correctly."""
        task = Task.create("Test", "Description")
        task.priority = Priority.HIGH
        task.tags = ["work", "urgent"]
        task.completed = True

        data = task.to_dict()

        self.assertEqual(data["id"], task.id)
        self.assertEqual(data["title"], "Test")
        self.assertEqual(data["description"], "Description")
        self.assertTrue(data["completed"])
        self.assertEqual(data["priority"], "high")
        self.assertEqual(data["tags"], ["work", "urgent"])

    def test_from_dict_deserialization(self):
        """from_dict() should deserialize all fields correctly."""
        data = {
            "id": "test-uuid-1234",
            "title": "Test Task",
            "description": "Test Description",
            "completed": True,
            "priority": "medium",
            "tags": ["work"],
            "created_at": "2024-01-15T09:00:00",
            "updated_at": "2024-01-15T10:00:00",
            "due_date": "2024-01-20",
            "recurring": "weekly"
        }

        task = Task.from_dict(data)

        self.assertEqual(task.id, "test-uuid-1234")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.priority, Priority.MEDIUM)
        self.assertEqual(task.due_date, "2024-01-20")
        self.assertEqual(task.recurring, "weekly")

    def test_to_dict_from_dict_roundtrip(self):
        """Serialization should be reversible."""
        original = Task.create("Test", "Description")
        original.priority = Priority.HIGH
        original.tags = ["work", "urgent"]

        data = original.to_dict()
        restored = Task.from_dict(data)

        self.assertEqual(restored.id, original.id)
        self.assertEqual(restored.title, original.title)
        self.assertEqual(restored.description, original.description)
        self.assertEqual(restored.priority, original.priority)
        self.assertEqual(restored.tags, original.tags)

    def test_priority_none_serializes_as_null(self):
        """Priority.NONE should serialize as None/null."""
        task = Task.create("Test")
        data = task.to_dict()

        self.assertIsNone(data["priority"])

    def test_from_dict_handles_missing_optional_fields(self):
        """from_dict() should handle missing optional fields gracefully."""
        data = {
            "id": "test-uuid",
            "title": "Test",
            "created_at": "2024-01-15T09:00:00",
            "updated_at": "2024-01-15T09:00:00"
        }

        task = Task.from_dict(data)

        self.assertEqual(task.description, "")
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, Priority.NONE)
        self.assertEqual(task.tags, [])


if __name__ == "__main__":
    unittest.main()
