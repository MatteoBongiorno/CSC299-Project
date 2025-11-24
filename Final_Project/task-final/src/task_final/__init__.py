"""Task Manager - A simple task management application."""

from task_05.models import Task, TaskCollection
from task_05.cli import TaskManagerCLI

__version__ = "1.0.0"
__all__ = ["Task", "TaskCollection", "TaskManagerCLI"]


def main() -> None:
    """Entry point for the task manager CLI."""
    cli = TaskManagerCLI()
    cli.run()
