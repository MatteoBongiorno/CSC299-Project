"""
Command-line interface for the Task Manager.
"""
from datetime import datetime
from task_final.models import Task, TaskCollection
from task_final.utils import prompt_valid_deadline, prompt_valid_priority, prompt_tags, parse_date
from task_final.summarizer import summarize_task


class TaskManagerCLI:
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
        
        # Multiple tasks with same name - show them and ask for ID
        print(f"\nFound {len(results)} task(s) with name '{task_name}':")
        for i, task in enumerate(results, 1):
            print(f"\n{i}. {task}")
        
        task_id = input("\nEnter the full task ID to select: ").strip()
        task = self.collection.get_task_by_id(task_id)
        
        if not task:
            print(f"Task with ID '{task_id}' not found.")
            return None, False
        
        return task, True

    def edit_task(self) -> None:
        """Edit an existing task by name."""
        print("\n--- Edit Task ---")
        task, found = self.find_task_by_name()
        
        if not found:
            return

        print(f"\nCurrent task: {task}")
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
                print("[OK] Name updated.")
        elif choice == "2":
            task.priority = prompt_valid_priority()
            print("[OK] Priority updated.")
        elif choice == "3":
            task.deadline = prompt_valid_deadline()
            print("[OK] Deadline updated.")
        elif choice == "4":
            task.tags = prompt_tags()
            print("[OK] Tags updated.")
        elif choice == "5":
            print("Edit cancelled.")
        else:
            print("Invalid choice.")

    def delete_task(self) -> None:
        """Delete a task from the collection by name."""
        print("\n--- Delete Task ---")
        task, found = self.find_task_by_name()
        
        if not found:
            return

        confirmation = input(
            f"Are you sure you want to delete '{task.name}'? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            if self.collection.remove_task(task.id):
                print("[OK] Task deleted successfully.")
            else:
                print(f"Failed to delete task.")
        else:
            print("Delete cancelled.")

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
