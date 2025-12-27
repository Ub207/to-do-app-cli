"""Tests for Priority enum."""

import unittest
from src.models import Priority


class TestPriority(unittest.TestCase):
    """Test Priority enumeration."""

    def test_priority_values_ordered(self):
        """Priority values should be ordered NONE < LOW < MEDIUM < HIGH."""
        self.assertLess(Priority.NONE.value, Priority.LOW.value)
        self.assertLess(Priority.LOW.value, Priority.MEDIUM.value)
        self.assertLess(Priority.MEDIUM.value, Priority.HIGH.value)

    def test_display_short(self):
        """Short display strings should be correct."""
        self.assertEqual(Priority.NONE.display_short(), "-")
        self.assertEqual(Priority.LOW.display_short(), "LOW")
        self.assertEqual(Priority.MEDIUM.display_short(), "MED")
        self.assertEqual(Priority.HIGH.display_short(), "HIGH")

    def test_display_full(self):
        """Full display strings should be correct."""
        self.assertEqual(Priority.NONE.display_full(), "None")
        self.assertEqual(Priority.LOW.display_full(), "Low")
        self.assertEqual(Priority.MEDIUM.display_full(), "Medium")
        self.assertEqual(Priority.HIGH.display_full(), "High")


if __name__ == "__main__":
    unittest.main()
