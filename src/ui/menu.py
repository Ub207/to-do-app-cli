"""Menu display and command routing."""

import sys

from src.models import Priority
from src.services import TaskService
from src.exceptions import TodoAppError
from src.ui.display import Display
from src.ui.input_handler import InputHandler


class Menu:
    """Main menu controller."""

    def __init__(self, task_service: TaskService) -> None:
        self.task_service = task_service

    def main_loop(self) -> None:
        """Run the main menu loop."""
        while True:
            Display.menu_level_2()
            choice = InputHandler.menu_choice()

            try:
                if choice in ["0", "q", "quit", "exit"]:
                    self._handle_exit()
                elif choice in ["h", "help"]:
                    self._handle_help()
                elif choice == "1":
                    self._handle_add()
                elif choice == "2":
                    self._handle_list()
                elif choice == "3":
                    self._handle_view()
                elif choice == "4":
                    self._handle_update()
                elif choice == "5":
                    self._handle_delete()
                elif choice == "6":
                    self._handle_toggle()
                elif choice == "7":
                    self._handle_set_priority()
                elif choice == "8":
                    self._handle_add_tag()
                elif choice == "9":
                    self._handle_remove_tag()
                elif choice == "10":
                    self._handle_search()
                elif choice == "11":
                    self._handle_filter()
                elif choice == "12":
                    self._handle_sort()
                elif choice == "13":
                    self._handle_set_due()
                elif choice == "14":
                    self._handle_clear_due()
                elif choice == "15":
                    self._handle_overdue()
                elif choice == "16":
                    self._handle_due_today()
                elif choice == "17":
                    self._handle_due_week()
                elif choice == "18":
                    self._handle_set_recurring()
                else:
                    print("Invalid choice. Enter 0-18 or 'h' for help.")
            except TodoAppError as e:
                Display.error(str(e))

            print()

    def _handle_exit(self) -> None:
        Display.goodbye()
        sys.exit(0)

    def _handle_help(self) -> None:
        Display.help_level_2()
        InputHandler.wait_for_enter()

    def _handle_add(self) -> None:
        print("--- Add New Task ---\n")
        title = InputHandler.prompt("Title: ")
        if not title:
            Display.error("Title cannot be empty.")
            return
        description = InputHandler.prompt("Description (Enter to skip): ")
        task = self.task_service.add_task(title, description)
        Display.success(f"\nTask added! ID: {task.short_id}")

    def _handle_list(self) -> None:
        tasks = self.task_service.get_all_tasks()
        total, completed = self.task_service.get_task_count()
        Display.task_list(tasks, total, completed)

    def _handle_view(self) -> None:
        print("--- View Task ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            Display.error("Task ID cannot be empty.")
            return
        task = self.task_service.find_by_partial_id(task_id)
        Display.task_details(task)

    def _handle_update(self) -> None:
        print("--- Update Task ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        print(f"\nCurrent title: {task.title}")
        new_title = InputHandler.prompt("New title (Enter to keep): ")
        print(f"Current description: {task.description or '(none)'}")
        new_desc = InputHandler.prompt("New description (Enter to keep, '-' to clear): ")

        title_to_set = new_title if new_title else None
        desc_to_set = "" if new_desc == "-" else (new_desc if new_desc else None)
        self.task_service.update_task(task.id, title_to_set, desc_to_set)
        Display.success("\nTask updated!")

    def _handle_delete(self) -> None:
        print("--- Delete Task ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        if not InputHandler.confirm(f'\nDelete "{task.title}"? (y/N): '):
            print("Cancelled.")
            return
        self.task_service.delete_task(task.id)
        Display.success("\nTask deleted!")

    def _handle_toggle(self) -> None:
        print("--- Toggle Status ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task, new_task = self.task_service.toggle_complete(task_id)
        status = "completed" if task.completed else "pending"
        Display.success(f'\n"{task.title}" marked as {status}.')
        if new_task:
            print(f"Recurring: New task created with ID {new_task.short_id}")

    def _handle_set_priority(self) -> None:
        print("--- Set Priority ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        print(f"\nCurrent: {task.priority.display_full()}")
        print("1. High  2. Medium  3. Low  4. None")
        choice = InputHandler.prompt("Choice (1-4): ")
        priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW, "4": Priority.NONE}
        if choice not in priority_map:
            Display.error("Invalid choice.")
            return
        self.task_service.set_priority(task.id, priority_map[choice])
        Display.success(f"\nPriority set to {priority_map[choice].display_full()}.")

    def _handle_add_tag(self) -> None:
        print("--- Add Tag ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        print(f"Current tags: {', '.join(task.tags) if task.tags else '(none)'}")
        tag = InputHandler.prompt("Enter tag: ")
        if not tag:
            return
        self.task_service.add_tag(task.id, tag)
        Display.success(f"\nTag '{tag}' added!")

    def _handle_remove_tag(self) -> None:
        print("--- Remove Tag ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        if not task.tags:
            Display.error("This task has no tags.")
            return
        print("Tags:")
        for i, tag in enumerate(task.tags, 1):
            print(f"  {i}. {tag}")
        choice = InputHandler.prompt("Enter tag name or number: ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(task.tags):
                tag = task.tags[idx]
            else:
                Display.error("Invalid number.")
                return
        else:
            tag = choice
        self.task_service.remove_tag(task.id, tag)
        Display.success(f"\nTag '{tag}' removed!")

    def _handle_search(self) -> None:
        print("--- Search ---\n")
        query = InputHandler.prompt("Search query (min 2 chars): ")
        if not query:
            return
        results = self.task_service.search(query)
        if not results:
            print(f"\nNo tasks found matching '{query}'.")
        else:
            print(f"\nFound {len(results)} task(s):")
            Display.task_list(results, len(results), sum(1 for t in results if t.completed))

    def _handle_filter(self) -> None:
        print("--- Filter ---")
        print("1. By Status  2. By Priority  3. By Tag  4. Show All")
        choice = InputHandler.prompt("Choice: ")

        if choice == "1":
            print("1. Pending  2. Completed")
            sub = InputHandler.prompt("Choice: ")
            completed = sub == "2"
            results = self.task_service.filter_by_status(completed)
            label = "Completed" if completed else "Pending"
        elif choice == "2":
            print("1. High  2. Medium  3. Low  4. None")
            sub = InputHandler.prompt("Choice: ")
            pmap = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW, "4": Priority.NONE}
            if sub not in pmap:
                return
            results = self.task_service.filter_by_priority(pmap[sub])
            label = pmap[sub].display_full()
        elif choice == "3":
            all_tags = self.task_service.get_all_tags()
            if not all_tags:
                print("No tags found.")
                return
            print("Tags:", ", ".join(all_tags))
            tag = InputHandler.prompt("Enter tag: ")
            results = self.task_service.filter_by_tag(tag)
            label = f"Tag '{tag}'"
        elif choice == "4":
            results = self.task_service.get_all_tasks()
            label = "All"
        else:
            return

        print(f"\n{label} tasks ({len(results)}):")
        Display.task_list(results, len(results), sum(1 for t in results if t.completed))

    def _handle_sort(self) -> None:
        print("--- Sort ---")
        print("1. Priority (high→low)  2. Priority (low→high)")
        print("3. Due date  4. Title A-Z  5. Created (newest)")
        choice = InputHandler.prompt("Choice: ")

        sort_map = {
            "1": ("priority", False),
            "2": ("priority_asc", False),
            "3": ("due_date", False),
            "4": ("title", False),
            "5": ("created", True),
        }
        if choice not in sort_map:
            return

        key, rev = sort_map[choice]
        tasks = self.task_service.get_all_tasks()
        sorted_tasks = self.task_service.sort_tasks(tasks, key, rev)
        Display.task_list(sorted_tasks, len(sorted_tasks), sum(1 for t in sorted_tasks if t.completed))

    # ==================== Due Date Handlers ====================

    def _handle_set_due(self) -> None:
        print("--- Set Due Date ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        print(f"Current due: {task.due_date or 'Not set'}")
        date_str = InputHandler.prompt("Enter due date (YYYY-MM-DD): ")
        if not date_str:
            return
        self.task_service.set_due_date(task.id, date_str)
        Display.success(f"\nDue date set to {date_str}.")

    def _handle_clear_due(self) -> None:
        print("--- Clear Due Date ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        if not task.due_date:
            print("This task has no due date.")
            return
        self.task_service.clear_due_date(task.id)
        Display.success("\nDue date cleared.")

    def _handle_overdue(self) -> None:
        tasks = self.task_service.get_overdue()
        if not tasks:
            print("\nNo overdue tasks!")
        else:
            print(f"\nOVERDUE ({len(tasks)}):")
            Display.task_list(tasks, len(tasks), 0)

    def _handle_due_today(self) -> None:
        tasks = self.task_service.get_due_today()
        if not tasks:
            print("\nNo tasks due today.")
        else:
            print(f"\nDUE TODAY ({len(tasks)}):")
            Display.task_list(tasks, len(tasks), 0)

    def _handle_due_week(self) -> None:
        tasks = self.task_service.get_due_this_week()
        if not tasks:
            print("\nNo tasks due this week.")
        else:
            print(f"\nDUE THIS WEEK ({len(tasks)}):")
            Display.task_list(tasks, len(tasks), 0)

    def _handle_set_recurring(self) -> None:
        print("--- Set Recurring ---\n")
        task_id = InputHandler.prompt("Enter task ID: ")
        if not task_id:
            return
        task = self.task_service.find_by_partial_id(task_id)
        if not task.due_date:
            Display.error("Task must have a due date first. Use option 13.")
            return
        print(f"Current: {task.recurring or 'Not set'}")
        print("1. Daily  2. Weekly  3. Monthly  4. Remove")
        choice = InputHandler.prompt("Choice: ")
        rmap = {"1": "daily", "2": "weekly", "3": "monthly", "4": None}
        if choice not in rmap:
            return
        self.task_service.set_recurring(task.id, rmap[choice])
        if rmap[choice]:
            Display.success(f"\nTask will recur {rmap[choice]}.")
        else:
            Display.success("\nRecurrence removed.")
