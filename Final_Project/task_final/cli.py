"""
Command-line interface for the Task Manager.
"""
from datetime import datetime
from colorama import Fore, Style, init
from task_final.models import Task, TaskCollection
from task_final.utils import (
    prompt_valid_deadline,
    prompt_valid_priority,
    prompt_tags,
    parse_date,
    center_text,
    select_task_interactive,
)
from task_final.summarizer import summarize_task

# Initialize colorama for cross-platform color support
init(autoreset=True)


# Color mapping for priorities
PRIORITY_COLORS = {
    "Low": Fore.GREEN,
    "Medium": Fore.YELLOW,
    "High": Fore.RED,
}

HEADER_COLOR = Fore.CYAN
SUCCESS_COLOR = Fore.MAGENTA
ERROR_COLOR = Fore.RED
INFO_COLOR = Fore.BLUE
MENU_WIDTH = 60


class TaskManagerCLI:
    """Interactive CLI for task management."""

    def __init__(self):
        """Initialize the CLI with an empty task collection."""
        self.collection = TaskCollection()

    def run(self) -> None:
        """Run the main CLI loop."""
        print("\n" + "=" * 60)
        print(f"{HEADER_COLOR}Welcome to Task Manager{Style.RESET_ALL}")
        print("=" * 60)

        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip().lower()

            if choice == "1":
                self.create_task()
            elif choice == "2":
                self.view_all_tasks()
            elif choice == "3":
                self.search_tasks()
            elif choice == "4":
                self.sort_tasks()
            elif choice == "5":
                self.edit_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                self.quit()
            else:
                print(f"{ERROR_COLOR}Invalid choice. Please try again.{Style.RESET_ALL}")

    def display_menu(self) -> None:
        """Display the main menu (centered)."""
        print("\n" + "-" * MENU_WIDTH)
        print(center_text(f"{HEADER_COLOR}Main Menu{Style.RESET_ALL}"))
        print("-" * MENU_WIDTH)
        print(center_text("1. Create a new task"))
        print(center_text("2. View all tasks"))
        print(center_text("3. Search tasks"))
        print(center_text("4. Sort tasks"))
        print(center_text("5. Edit a task"))
        print(center_text("6. Delete a task"))
        print(center_text("7. Exit"))
        print("-" * MENU_WIDTH)

    def create_task(self) -> None:
        """Create a new task with user input."""
        print(f"\n{HEADER_COLOR}--- Create New Task ---{Style.RESET_ALL}")

        name = input("Enter task name: ").strip()
        if not name:
            print(f"{ERROR_COLOR}Task name cannot be empty.{Style.RESET_ALL}")
            return

        priority = prompt_valid_priority()
        deadline = prompt_valid_deadline()
        tags = prompt_tags()

        try:
            task = Task(name=name, priority=priority, deadline=deadline, tags=tags)
            self.collection.add_task(task)
            print(f"\n{SUCCESS_COLOR}[OK] Task created successfully!{Style.RESET_ALL}")
            print(f"{INFO_COLOR}Task ID: {task.id[:12]}...{Style.RESET_ALL}")
        except ValueError as e:
            print(f"{ERROR_COLOR}✗ Error creating task: {e}{Style.RESET_ALL}")

    def view_all_tasks(self) -> None:
        """Display all tasks in the collection."""
        print(f"\n{HEADER_COLOR}--- All Tasks ---{Style.RESET_ALL}")
        if len(self.collection) == 0:
            print("No tasks in the collection.")
            return

        print(self.collection.display_all_tasks_colored())

    def search_tasks(self) -> None:
        """Search tasks by name, priority, deadline, or tags."""
        print(f"\n{HEADER_COLOR}--- Search Tasks ---{Style.RESET_ALL}")
        print("Search by:")
        print("1. Name")
        print("2. Priority")
        print("3. Deadline")
        print("4. Tags")

        choice = input("Enter search type (1-4): ").strip()

        if choice == "1":
            self.search_by_name()
        elif choice == "2":
            self.search_by_priority()
        elif choice == "3":
            self.search_by_deadline()
        elif choice == "4":
            self.search_by_tags()
        else:
            print(f"{ERROR_COLOR}Invalid choice.{Style.RESET_ALL}")

    def search_by_name(self) -> None:
        """Search tasks by name."""
        query = input("Enter name to search for: ").strip()
        results = self.collection.search_by_name(query, exact=False)

        if not results:
            print(f"{ERROR_COLOR}No tasks found matching '{query}'.{Style.RESET_ALL}")
            return

        print(f"\n{INFO_COLOR}Found {len(results)} task(s):{Style.RESET_ALL}")
        for i, task in enumerate(results, 1):
            priority_color = PRIORITY_COLORS.get(task.priority, "")
            print(f"\n{i}. {priority_color}{task}{Style.RESET_ALL}")

    def search_by_priority(self) -> None:
        """Search tasks by priority."""
        priority = prompt_valid_priority()
        results = self.collection.search_by_priority(priority)

        if not results:
            print(f"{ERROR_COLOR}No tasks found with priority '{priority}'.{Style.RESET_ALL}")
            return

        priority_color = PRIORITY_COLORS.get(priority, "")
        print(f"\n{INFO_COLOR}Found {len(results)} task(s) with priority {priority_color}{priority}{Style.RESET_ALL}{INFO_COLOR}:{Style.RESET_ALL}")
        for i, task in enumerate(results, 1):
            print(f"\n{i}. {priority_color}{task}{Style.RESET_ALL}")

    def search_by_deadline(self) -> None:
        """Search tasks by deadline."""
        deadline = prompt_valid_deadline()
        results = self.collection.search_by_deadline(deadline)

        if not results:
            print(f"{ERROR_COLOR}No tasks found with deadline {deadline.strftime('%Y-%m-%d')}.{Style.RESET_ALL}")
            return

        print(f"\n{INFO_COLOR}Found {len(results)} task(s) with deadline {deadline.strftime('%Y-%m-%d')}:{Style.RESET_ALL}")
        for i, task in enumerate(results, 1):
            priority_color = PRIORITY_COLORS.get(task.priority, "")
            print(f"\n{i}. {priority_color}{task}{Style.RESET_ALL}")

    def search_by_tags(self) -> None:
        """Search tasks by tags."""
        tags = prompt_tags()
        if not tags:
            print(f"{ERROR_COLOR}No tags provided.{Style.RESET_ALL}")
            return

        results = self.collection.search_by_tags(tags, match_all=False)

        if not results:
            print(f"{ERROR_COLOR}No tasks found with tags {tags}.{Style.RESET_ALL}")
            return

        print(f"\n{INFO_COLOR}Found {len(results)} task(s) with tags {tags}:{Style.RESET_ALL}")
        for i, task in enumerate(results, 1):
            priority_color = PRIORITY_COLORS.get(task.priority, "")
            print(f"\n{i}. {priority_color}{task}{Style.RESET_ALL}")

    def sort_tasks(self) -> None:
        """Sort and display tasks."""
        print(f"\n{HEADER_COLOR}--- Sort Tasks ---{Style.RESET_ALL}")
        print("Sort by:")
        print("1. Name (alphabetical)")
        print("2. Priority (High to Low)")
        print("3. Deadline (earliest first)")

        choice = input("Enter sort type (1-3): ").strip()

        if choice == "1":
            results = self.collection.sort_by_name()
            print(f"\n{INFO_COLOR}Tasks sorted by name (A-Z):{Style.RESET_ALL}")
        elif choice == "2":
            results = self.collection.sort_by_priority()
            print(f"\n{INFO_COLOR}Tasks sorted by priority (High → Medium → Low):{Style.RESET_ALL}")
        elif choice == "3":
            results = self.collection.sort_by_deadline()
            print(f"\n{INFO_COLOR}Tasks sorted by deadline (earliest first):{Style.RESET_ALL}")
        else:
            print(f"{ERROR_COLOR}Invalid choice.{Style.RESET_ALL}")
            return

        if not results:
            print("No tasks to sort.")
            return

        for i, task in enumerate(results, 1):
            priority_color = PRIORITY_COLORS.get(task.priority, "")
            print(f"\n{i}. {priority_color}{task}{Style.RESET_ALL}")

    def find_task_by_name(self) -> tuple:
        """Find a task by name, prompting for ID if multiple matches.
        
        Returns:
            tuple: (task, found) where task is the Task object or None, found is bool
        """
        task_name = input("Enter task name to edit/delete: ").strip()
        if not task_name:
            print(f"{ERROR_COLOR}Task name cannot be empty.{Style.RESET_ALL}")
            return None, False
        
        # Search for tasks with this name
        results = self.collection.search_by_name(task_name, exact=True)
        
        if not results:
            print(f"{ERROR_COLOR}No task found with name '{task_name}'.{Style.RESET_ALL}")
            return None, False
        
        if len(results) == 1:
            return results[0], True
        
        # Multiple tasks with same name - show them and ask for ID
        print(f"\n{INFO_COLOR}Found {len(results)} task(s) with name '{task_name}':{Style.RESET_ALL}")
        for i, task in enumerate(results, 1):
            priority_color = PRIORITY_COLORS.get(task.priority, "")
            print(f"\n{i}. {priority_color}{task}{Style.RESET_ALL}")
        
        task_id = input("\nEnter the full task ID to select: ").strip()
        task = self.collection.get_task_by_id(task_id)
        
        if not task:
            print(f"{ERROR_COLOR}Task with ID '{task_id}' not found.{Style.RESET_ALL}")
            return None, False
        
        return task, True

    def edit_task(self) -> None:
        """Edit an existing task by name."""
        print(f"\n{HEADER_COLOR}--- Edit Task ---{Style.RESET_ALL}")
        task, found = self.find_task_by_name()
        
        if not found:
            return

        priority_color = PRIORITY_COLORS.get(task.priority, "")
        print(f"\nCurrent task: {priority_color}{task}{Style.RESET_ALL}")
        print("\nWhat would you like to edit?")
        print("1. Name")
        print("2. Priority")
        print("3. Deadline")
        print("4. Tags")
        print("5. Cancel")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            if new_name:
                task.name = new_name
                print(f"{SUCCESS_COLOR}[OK] Name updated.{Style.RESET_ALL}")
        elif choice == "2":
            task.priority = prompt_valid_priority()
            print(f"{SUCCESS_COLOR}[OK] Priority updated.{Style.RESET_ALL}")
        elif choice == "3":
            task.deadline = prompt_valid_deadline()
            print(f"{SUCCESS_COLOR}[OK] Deadline updated.{Style.RESET_ALL}")
        elif choice == "4":
            task.tags = prompt_tags()
            print(f"{SUCCESS_COLOR}[OK] Tags updated.{Style.RESET_ALL}")
        elif choice == "5":
            print("Edit cancelled.")
        else:
            print(f"{ERROR_COLOR}Invalid choice.{Style.RESET_ALL}")

    def delete_task(self) -> None:
        """Delete a task from the collection by name."""
        print(f"\n{HEADER_COLOR}--- Delete Task ---{Style.RESET_ALL}")
        task, found = self.find_task_by_name()
        
        if not found:
            return

        confirmation = input(
            f"Are you sure you want to delete '{task.name}'? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            if self.collection.remove_task(task.id):
                print(f"{SUCCESS_COLOR}[OK] Task deleted successfully.{Style.RESET_ALL}")
            else:
                print(f"{ERROR_COLOR}Failed to delete task.{Style.RESET_ALL}")
        else:
            print("Delete cancelled.")

    def quit(self) -> None:
        """Exit the application."""
        print(f"\n{SUCCESS_COLOR}Thank you for using Task Manager. Goodbye!{Style.RESET_ALL}")
        exit(0)


def main() -> None:
    """Entry point for the task manager CLI."""
    cli = TaskManagerCLI()
    cli.run()


if __name__ == "__main__":
    main()
    """Interactive CLI for task management."""

    def __init__(self):
        """Initialize the CLI with an empty task collection."""
        self.collection = TaskCollection()

    def run(self) -> None:
        """Run the main CLI loop."""
        print("\n" + "=" * 60)
        print("Welcome to Task Manager")
        print("=" * 60)

        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ").strip().lower()

            if choice == "1":
                self.create_task()
            elif choice == "2":
                self.view_all_tasks()
            elif choice == "3":
                self.search_tasks()
            elif choice == "4":
                self.sort_tasks()
            elif choice == "5":
                self.edit_task()
            elif choice == "6":
                self.delete_task()
            elif choice == "7":
                self.quit()
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "-" * 60)
        print("Main Menu")
        print("-" * 60)
        print("1. Create a new task")
        print("2. View all tasks")
        print("3. Search tasks")
        print("4. Sort tasks")
        print("5. Edit a task")
        print("6. Delete a task")
        print("7. Exit")
        print("-" * 60)

    def create_task(self) -> None:
        """Create a new task with user input."""
        print("\n--- Create New Task ---")

        name = input("Enter task name: ").strip()
        if not name:
            print("Task name cannot be empty.")
            return

        priority = prompt_valid_priority()
        deadline = prompt_valid_deadline()
        tags = prompt_tags()

        try:
            task = Task(name=name, priority=priority, deadline=deadline, tags=tags)
            self.collection.add_task(task)
            print(f"\n[OK] Task created successfully!")
            print(f"Task ID: {task.id[:12]}...")
        except ValueError as e:
            print(f"✗ Error creating task: {e}")

    def view_all_tasks(self) -> None:
        """Display all tasks in the collection."""
        print("\n--- All Tasks ---")
        if len(self.collection) == 0:
            print("No tasks in the collection.")
            return

        print(self.collection.display_all_tasks())

    def search_tasks(self) -> None:
        """Search tasks by name, priority, deadline, or tags."""
        print("\n--- Search Tasks ---")
        print("Search by:")
        print("1. Name")
        print("2. Priority")
        print("3. Deadline")
        print("4. Tags")

        choice = input("Enter search type (1-4): ").strip()

        if choice == "1":
            self.search_by_name()
        elif choice == "2":
            self.search_by_priority()
        elif choice == "3":
            self.search_by_deadline()
        elif choice == "4":
            self.search_by_tags()
        else:
            print("Invalid choice.")

    def search_by_name(self) -> None:
        """Search tasks by name."""
        query = input("Enter name to search for: ").strip()
        results = self.collection.search_by_name(query, exact=False)

        if not results:
            print(f"No tasks found matching '{query}'.")
            return

        print(f"\nFound {len(results)} task(s):")
        for i, task in enumerate(results, 1):
            print(f"\n{i}. {task}")

    def search_by_priority(self) -> None:
        """Search tasks by priority."""
        priority = prompt_valid_priority()
        results = self.collection.search_by_priority(priority)

        if not results:
            print(f"No tasks found with priority '{priority}'.")
            return

        print(f"\nFound {len(results)} task(s) with priority '{priority}':")
        for i, task in enumerate(results, 1):
            print(f"\n{i}. {task}")

    def search_by_deadline(self) -> None:
        """Search tasks by deadline."""
        deadline = prompt_valid_deadline()
        results = self.collection.search_by_deadline(deadline)

        if not results:
            print(f"No tasks found with deadline {deadline.strftime('%Y-%m-%d')}.")
            return

        print(f"\nFound {len(results)} task(s) with deadline {deadline.strftime('%Y-%m-%d')}:")
        for i, task in enumerate(results, 1):
            print(f"\n{i}. {task}")

    def search_by_tags(self) -> None:
        """Search tasks by tags."""
        tags = prompt_tags()
        if not tags:
            print("No tags provided.")
            return

        results = self.collection.search_by_tags(tags, match_all=False)

        if not results:
            print(f"No tasks found with tags {tags}.")
            return

        print(f"\nFound {len(results)} task(s) with tags {tags}:")
        for i, task in enumerate(results, 1):
            print(f"\n{i}. {task}")

    def sort_tasks(self) -> None:
        """Sort and display tasks."""
        print("\n--- Sort Tasks ---")
        print("Sort by:")
        print("1. Name (alphabetical)")
        print("2. Priority (High to Low)")
        print("3. Deadline (earliest first)")

        choice = input("Enter sort type (1-3): ").strip()

        if choice == "1":
            results = self.collection.sort_by_name()
            print("\nTasks sorted by name (A-Z):")
        elif choice == "2":
            results = self.collection.sort_by_priority()
            print("\nTasks sorted by priority (High → Medium → Low):")
        elif choice == "3":
            results = self.collection.sort_by_deadline()
            print("\nTasks sorted by deadline (earliest first):")
        else:
            print("Invalid choice.")
            return

        if not results:
            print("No tasks to sort.")
            return

        for i, task in enumerate(results, 1):
            print(f"\n{i}. {task}")

    def find_task_by_name(self) -> tuple:
        """Find a task by name, prompting for ID if multiple matches.
        
        Returns:
            tuple: (task, found) where task is the Task object or None, found is bool
        """
        task_name = input("Enter task name to edit/delete: ").strip()
        if not task_name:
            print("Task name cannot be empty.")
            return None, False
        
        # Search for tasks with this name
        results = self.collection.search_by_name(task_name, exact=True)
        
        if not results:
            print(f"No task found with name '{task_name}'.")
            return None, False
        
        if len(results) == 1:
            return results[0], True
        
        # Multiple tasks with same name - use interactive selection
        task = select_task_interactive(results, "task")
        return task, task is not None

    def show_task_action_menu(self, task: Task) -> None:
        """Display action menu for a selected task.
        
        Args:
            task: The Task object to perform actions on
        """
        while True:
            print(f"\n{HEADER_COLOR}Task Actions:{Style.RESET_ALL}")
            priority_color = PRIORITY_COLORS.get(task.priority, "")
            print(f"\nSelected: {priority_color}{task}{Style.RESET_ALL}")
            print("\nWhat would you like to do?")
            print("1. Edit task")
            print("2. Delete task")
            print("3. View details")
            print("4. Back to menu")

            choice = input("Enter choice (1-4): ").strip()

            if choice == "1":
                self.edit_single_task(task)
            elif choice == "2":
                self.delete_single_task(task)
            elif choice == "3":
                print(f"\n{priority_color}{task}{Style.RESET_ALL}")
            elif choice == "4":
                break
            else:
                print(f"{ERROR_COLOR}Invalid choice.{Style.RESET_ALL}")

    def edit_single_task(self, task: Task) -> None:
        """Edit a specific task.
        
        Args:
            task: The Task object to edit
        """
        print(f"\n{HEADER_COLOR}Edit Task:{Style.RESET_ALL}")
        print("What would you like to edit?")
        print("1. Name")
        print("2. Priority")
        print("3. Deadline")
        print("4. Tags")
        print("5. Cancel")

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            new_name = input("Enter new name: ").strip()
            if new_name:
                task.name = new_name
                print(f"{SUCCESS_COLOR}[OK] Name updated.{Style.RESET_ALL}")
        elif choice == "2":
            task.priority = prompt_valid_priority()
            print(f"{SUCCESS_COLOR}[OK] Priority updated.{Style.RESET_ALL}")
        elif choice == "3":
            task.deadline = prompt_valid_deadline()
            print(f"{SUCCESS_COLOR}[OK] Deadline updated.{Style.RESET_ALL}")
        elif choice == "4":
            task.tags = prompt_tags()
            print(f"{SUCCESS_COLOR}[OK] Tags updated.{Style.RESET_ALL}")
        elif choice == "5":
            print("Edit cancelled.")
        else:
            print(f"{ERROR_COLOR}Invalid choice.{Style.RESET_ALL}")

    def delete_single_task(self, task: Task) -> None:
        """Delete a specific task.
        
        Args:
            task: The Task object to delete
        """
        confirmation = input(
            f"Are you sure you want to delete '{task.name}'? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            if self.collection.remove_task(task.id):
                print(f"{SUCCESS_COLOR}[OK] Task deleted successfully.{Style.RESET_ALL}")
            else:
                print(f"{ERROR_COLOR}Failed to delete task.{Style.RESET_ALL}")
        else:
            print("Delete cancelled.")

    def edit_task(self) -> None:
        """Edit an existing task by name."""
        print(f"\n{HEADER_COLOR}--- Edit Task ---{Style.RESET_ALL}")
        task, found = self.find_task_by_name()
        
        if not found:
            return
        
        self.show_task_action_menu(task)

    def delete_task(self) -> None:
        """Delete a task from the collection by name."""
        print(f"\n{HEADER_COLOR}--- Delete Task ---{Style.RESET_ALL}")
        task, found = self.find_task_by_name()
        
        if not found:
            return
        
        self.delete_single_task(task)

    def quit(self) -> None:
        """Exit the application."""
        print("\nThank you for using Task Manager. Goodbye!")
        exit(0)


def main() -> None:
    """Entry point for the task manager CLI."""
    cli = TaskManagerCLI()
    cli.run()


if __name__ == "__main__":
    main()
