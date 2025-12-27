"""JSON file storage service."""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.models import Task
from src.exceptions import StorageError
from src.utils.constants import (
    DATA_DIR, DEFAULT_DATA_FILE, BACKUP_SUFFIX, TEMP_SUFFIX, DATA_VERSION
)


class StorageService:
    """Handles JSON file persistence for tasks."""

    def __init__(self, file_path: Optional[Path] = None) -> None:
        """
        Initialize storage service.

        Args:
            file_path: Path to JSON file. Defaults to data/tasks.json
        """
        self.file_path = file_path or DEFAULT_DATA_FILE
        self.backup_path = Path(str(self.file_path) + BACKUP_SUFFIX)
        self.temp_path = Path(str(self.file_path) + TEMP_SUFFIX)
        self._memory_only_mode = False

    def load(self) -> list[Task]:
        """
        Load tasks from JSON file.

        Returns:
            List of Task objects
        """
        # Ensure data directory exists
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents=True)
            print("Created data directory.")

        # If file doesn't exist, create empty
        if not self.file_path.exists():
            self._create_empty_file()
            print("Created new task list.")
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validate structure
            if "tasks" not in data:
                raise KeyError("Missing 'tasks' key")

            tasks = [Task.from_dict(t) for t in data["tasks"]]
            return tasks

        except (json.JSONDecodeError, KeyError) as e:
            # Backup corrupted file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            corrupted_path = Path(f"{self.file_path}.corrupted.{timestamp}")
            shutil.copy2(self.file_path, corrupted_path)

            print(f"Warning: Task file was corrupted. Starting fresh.")
            print(f"Corrupted file backed up to: {corrupted_path.name}")

            self._create_empty_file()
            return []

        except PermissionError:
            print("Error: Cannot read task file. Check file permissions.")
            print("Running in memory-only mode. Changes will not be saved.")
            self._memory_only_mode = True
            return []

    def save(self, tasks: list[Task]) -> bool:
        """
        Save tasks to JSON file atomically.

        Args:
            tasks: List of Task objects to save

        Returns:
            True if save successful, False otherwise
        """
        if self._memory_only_mode:
            return True  # Pretend success

        data = {
            "version": DATA_VERSION,
            "last_modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "tasks": [task.to_dict() for task in tasks]
        }

        try:
            # Write to temp file
            with open(self.temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

            # Backup existing file
            if self.file_path.exists():
                shutil.copy2(self.file_path, self.backup_path)

            # Atomic rename
            self.temp_path.replace(self.file_path)
            return True

        except Exception as e:
            print(f"Warning: Could not save tasks. Your changes may be lost.")
            # Clean up temp file
            if self.temp_path.exists():
                self.temp_path.unlink()
            return False

    def _create_empty_file(self) -> None:
        """Create an empty tasks file."""
        data = {
            "version": DATA_VERSION,
            "last_modified": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "tasks": []
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def restore_from_backup(self) -> list[Task]:
        """
        Attempt to restore from backup file.

        Returns:
            List of tasks from backup, or empty list
        """
        if not self.backup_path.exists():
            return []

        try:
            with open(self.backup_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [Task.from_dict(t) for t in data.get("tasks", [])]
        except Exception:
            return []
