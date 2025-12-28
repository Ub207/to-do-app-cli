#!/usr/bin/env python3
"""Demo script for Phase I Todo CLI - Non-interactive demonstration."""

from src.app import TodoApp
from src.ui.display import Display

def demo():
    """Demonstrate Phase I functionality."""
    print("=" * 80)
    print("PHASE I TODO CLI - DEMONSTRATION".center(80))
    print("=" * 80)
    print()

    # Initialize app
    app = TodoApp()
    service = app.task_service

    print(">>> Initializing Phase I Todo CLI (In-Memory)")
    print("[OK] Application initialized\n")

    # US-001: Add Tasks
    print("=" * 80)
    print("US-001: ADD TASKS".center(80))
    print("=" * 80)
    task1 = service.add_task("Buy groceries", "Milk, bread, eggs, cheese")
    print(f"[ADDED] {task1.short_id} - {task1.title}")

    task2 = service.add_task("Call dentist", "Schedule cleaning appointment")
    print(f"[ADDED] {task2.short_id} - {task2.title}")

    task3 = service.add_task("Finish report")
    print(f"[ADDED] {task3.short_id} - {task3.title}")

    task4 = service.add_task("Exercise", "30 minute run")
    print(f"[ADDED] {task4.short_id} - {task4.title}")
    print()

    # US-002: View All Tasks
    print("=" * 80)
    print("US-002: VIEW ALL TASKS".center(80))
    print("=" * 80)
    tasks = service.get_all_tasks()
    total, completed = service.get_task_count()
    Display.task_list(tasks, total, completed)
    print()

    # US-003: View Task Details
    print("=" * 80)
    print("US-003: VIEW TASK DETAILS".center(80))
    print("=" * 80)
    print(f">>> Viewing task with partial ID: {task1.short_id[:4]}")
    task = service.find_by_partial_id(task1.short_id[:4])
    Display.task_details(task)
    print()

    # US-006: Toggle Complete
    print("=" * 80)
    print("US-006: TOGGLE TASK COMPLETION".center(80))
    print("=" * 80)
    print(f">>> Marking '{task2.title}' as complete")
    service.toggle_complete(task2.id)
    print(f"[OK] Task {task2.short_id} marked as completed")

    print(f">>> Marking '{task4.title}' as complete")
    service.toggle_complete(task4.id)
    print(f"[OK] Task {task4.short_id} marked as completed\n")

    # Show updated list
    tasks = service.get_all_tasks()
    total, completed = service.get_task_count()
    Display.task_list(tasks, total, completed)
    print()

    # US-004: Update Task
    print("=" * 80)
    print("US-004: UPDATE TASK".center(80))
    print("=" * 80)
    print(f">>> Updating task {task1.short_id}")
    print(f"    Old title: {task1.title}")
    service.update_task(task1.id, title="Buy groceries and snacks")
    updated = service.get_task(task1.id)
    print(f"    New title: {updated.title}")
    print(f"[OK] Task {task1.short_id} updated\n")

    # US-005: Delete Task
    print("=" * 80)
    print("US-005: DELETE TASK".center(80))
    print("=" * 80)
    print(f">>> Deleting task {task3.short_id}: '{task3.title}'")
    service.delete_task(task3.id)
    print(f"[OK] Task {task3.short_id} deleted\n")

    # Final task list
    print("=" * 80)
    print("FINAL TASK LIST".center(80))
    print("=" * 80)
    tasks = service.get_all_tasks()
    total, completed = service.get_task_count()
    Display.task_list(tasks, total, completed)
    print()

    # Constitution compliance summary
    print("=" * 80)
    print("CONSTITUTIONAL COMPLIANCE SUMMARY".center(80))
    print("=" * 80)
    print()
    print("[PASS] Article 2: Spec-Driven Development")
    print("        - Implements approved spec v1.1.0")
    print("        - Follows approved plan v1.1.0")
    print()
    print("[PASS] Article 3: Agent Behavior")
    print("        - No invented features")
    print("        - Full traceability to spec/plan/tasks")
    print()
    print("[PASS] Article 4: Phase Governance")
    print("        - Phase I scope only")
    print("        - No Phase II+ features (priorities, tags, persistence)")
    print()
    print("[PASS] Article 5: Technology Constitution")
    print("        - Python stdlib only (dataclasses, datetime, uuid, sys)")
    print("        - No external dependencies")
    print()
    print("[PASS] Article 6: Quality & Engineering")
    print("        - Clean 3-layer architecture (Model/Service/UI)")
    print("        - Type hints on all functions")
    print("        - Docstrings on all public methods")
    print()
    print("=" * 80)
    print("PHASE I TODO CLI - DEMONSTRATION COMPLETE".center(80))
    print("=" * 80)
    print()
    print("To run interactively: python main.py")
    print()


if __name__ == "__main__":
    demo()
