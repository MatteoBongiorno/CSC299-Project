"""
Task and TaskCollection models for the Task Manager.
"""
from datetime import datetime
from typing import List, Optional
import uuid


class Task:
    """
    Represents a single task with name, priority, deadline, and tags.
    """

    PRIORITY_LEVELS = ["Low", "Medium", "High"]

    def __init__(
        self,
        name: str,
        priority: str,
        deadline: datetime,
        tags: Optional[List[str]] = None,
        task_id: Optional[str] = None,
    ):
        """
        Initialize a Task.

        Args:
            name: Task name (required, non-empty)
            priority: Priority level (Low, Medium, High)
            deadline: Task deadline as datetime object
            tags: List of descriptive tags (optional)
            task_id: Unique task identifier (auto-generated if not provided)

        Raises:
            ValueError: If name is empty, priority is invalid, or deadline is in the past
        """
        if not name or not name.strip():
            raise ValueError("Task name cannot be empty.")

        if priority not in self.PRIORITY_LEVELS:
            raise ValueError(
                f"Priority must be one of {self.PRIORITY_LEVELS}, got '{priority}'."
            )

        # Check for past deadline
        if deadline < datetime.now():
            raise ValueError(
                f"Deadline {deadline.strftime('%Y-%m-%d %H:%M')} is in the past."
            )

        self.id = task_id or str(uuid.uuid4())
        self.name = name.strip()
        self.priority = priority
        self.deadline = deadline
        self.tags = [tag.strip() for tag in tags] if tags else []
        self.created_at = datetime.now()

    def __repr__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "None"
        return (
            f"Task(id={self.id[:8]}..., name='{self.name}', "
            f"priority='{self.priority}', deadline='{self.deadline.strftime('%Y-%m-%d')}', "
            f"tags=[{tags_str}])"
        )

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "None"
        return (
            f"[{self.priority[0]}] {self.name}\n"
            f"   Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M')}\n"
            f"   Tags: {tags_str}\n"
            f"   ID: {self.id}"
        )

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "deadline": self.deadline.isoformat(),
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Create a Task from dictionary representation."""
        return Task(
            name=data["name"],
            priority=data["priority"],
            deadline=datetime.fromisoformat(data["deadline"]),
            tags=data.get("tags", []),
            task_id=data.get("id"),
        )


class TaskCollection:
    """
    Manages a collection of tasks with search, sort, and display capabilities.
    """

    def __init__(self):
        """Initialize an empty task collection."""
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """
        Add a task to the collection.

        Args:
            task: Task object to add
        """
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> bool:
        """
        Remove a task by ID.

        Args:
            task_id: ID of the task to remove

        Returns:
            True if task was removed, False if not found
        """
        original_length = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < original_length

    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def search_by_name(self, name_query: str, exact: bool = False) -> List[Task]:
        """
        Search tasks by name.

        Args:
            name_query: Name string to search for
            exact: If True, search for exact match; if False, case-insensitive partial match

        Returns:
            List of matching tasks
        """
        query = name_query.strip().lower()
        if exact:
            return [t for t in self.tasks if t.name.lower() == query]
        return [t for t in self.tasks if query in t.name.lower()]

    def search_by_priority(self, priority: str) -> List[Task]:
        """
        Search tasks by priority level.

        Args:
            priority: Priority level to search for (Low, Medium, High)

        Returns:
            List of matching tasks
        """
        if priority not in Task.PRIORITY_LEVELS:
            return []
        return [t for t in self.tasks if t.priority == priority]

    def search_by_deadline(self, deadline: datetime) -> List[Task]:
        """
        Search tasks by deadline (exact date match).

        Args:
            deadline: Deadline datetime to search for

        Returns:
            List of tasks with matching deadline date
        """
        target_date = deadline.date()
        return [t for t in self.tasks if t.deadline.date() == target_date]

    def search_by_tags(self, tags: List[str], match_all: bool = False) -> List[Task]:
        """
        Search tasks by tags.

        Args:
            tags: List of tags to search for
            match_all: If True, task must have ALL tags; if False, task must have ANY tag

        Returns:
            List of matching tasks
        """
        query_tags = [tag.strip().lower() for tag in tags]
        if match_all:
            return [
                t
                for t in self.tasks
                if all(any(tag.lower() == q for q in query_tags) for tag in t.tags)
            ]
        return [
            t
            for t in self.tasks
            if any(any(tag.lower() == q for q in query_tags) for tag in t.tags)
        ]

    def sort_by_name(self, reverse: bool = False) -> List[Task]:
        """
        Sort tasks by name alphabetically.

        Args:
            reverse: If True, sort descending

        Returns:
            Sorted list of tasks
        """
        return sorted(self.tasks, key=lambda t: t.name.lower(), reverse=reverse)

    def sort_by_priority(self, reverse: bool = False) -> List[Task]:
        """
        Sort tasks by priority (High > Medium > Low).

        Args:
            reverse: If True, sort ascending (Low > Medium > High)

        Returns:
            Sorted list of tasks
        """
        priority_order = {"Low": 1, "Medium": 2, "High": 3}
        return sorted(
            self.tasks, key=lambda t: priority_order[t.priority], reverse=not reverse
        )

    def sort_by_deadline(self, reverse: bool = False) -> List[Task]:
        """
        Sort tasks by deadline (earliest first by default).

        Args:
            reverse: If True, sort latest first

        Returns:
            Sorted list of tasks
        """
        return sorted(self.tasks, key=lambda t: t.deadline, reverse=reverse)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the collection.

        Returns:
            List of all tasks
        """
        return self.tasks.copy()

    def display_all_tasks(self) -> str:
        """
        Generate a formatted string representation of all tasks.

        Returns:
            Formatted string of all tasks
        """
        if not self.tasks:
            return "No tasks in collection."

        result = f"Tasks in collection ({len(self.tasks)} total):\n"
        result += "=" * 60 + "\n"
        for i, task in enumerate(self.tasks, 1):
            result += f"\n{i}. {task}\n"
        result += "=" * 60
        return result

    def display_all_tasks_colored(self) -> str:
        """
        Generate a formatted string representation of all tasks with priority colors.

        Returns:
            Formatted string of all tasks with ANSI color codes
        """
        from colorama import Fore, Style
        
        PRIORITY_COLORS = {
            "Low": Fore.GREEN,
            "Medium": Fore.YELLOW,
            "High": Fore.RED,
        }
        
        if not self.tasks:
            return "No tasks in collection."

        result = f"Tasks in collection ({len(self.tasks)} total):\n"
        result += "=" * 60 + "\n"
        for i, task in enumerate(self.tasks, 1):
            priority_color = PRIORITY_COLORS.get(task.priority, "")
            result += f"\n{i}. {priority_color}{task}{Style.RESET_ALL}\n"
        result += "=" * 60
        return result

    def __len__(self) -> int:
        """Return the number of tasks in the collection."""
        return len(self.tasks)
