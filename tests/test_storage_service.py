"""Tests for StorageService."""

import unittest
import json
import tempfile
from pathlib import Path

from src.services import StorageService
from src.models import Task


class TestStorageService(unittest.TestCase):
    """Test StorageService persistence."""

    def setUp(self):
        """Create temporary directory for test files."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / "test_tasks.json"

    def test_save_and_load_roundtrip(self):
        """Tasks should persist correctly."""
        storage = StorageService(self.test_file)
        tasks = [Task.create("Task 1"), Task.create("Task 2")]
        storage.save(tasks)
        loaded = storage.load()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Task 1")

    def test_load_nonexistent_file_creates_empty(self):
        """Loading nonexistent file should create empty list."""
        storage = StorageService(self.test_file)
        tasks = storage.load()
        self.assertEqual(tasks, [])

    def test_load_corrupted_file_recovers(self):
        """Loading corrupted file should recover gracefully."""
        with open(self.test_file, 'w') as f:
            f.write("not valid json {{{")
        storage = StorageService(self.test_file)
        tasks = storage.load()
        self.assertEqual(tasks, [])


if __name__ == "__main__":
    unittest.main()
