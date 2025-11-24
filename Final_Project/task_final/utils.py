"""
Utility functions for input validation and date handling.
"""
from datetime import datetime
from typing import Optional, List
from colorama import Fore, Style, init
import readchar

# Initialize colorama for cross-platform color support
init(autoreset=True)


def validate_priority(priority: str) -> bool:
    """Check if priority is valid (case-insensitive)."""
    return priority.lower() in ["low", "medium", "high"]


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse a date string in YYYY-MM-DD or YYYY-MM-DD HH:MM format.

    Args:
        date_str: Date string to parse

    Returns:
        datetime object if valid, None otherwise
    """
    for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            # If only date provided, set time to 23:59 (end of day)
            if fmt == "%Y-%m-%d":
                dt = dt.replace(hour=23, minute=59)
            return dt
        except ValueError:
            continue
    return None


def prompt_valid_deadline() -> datetime:
    """
    Prompt user for a valid future deadline. Re-prompts if date is in past.

    Returns:
        Valid datetime object for a future deadline
    """
    while True:
        date_str = input(
            f"{Fore.CYAN}Enter deadline (YYYY-MM-DD or YYYY-MM-DD HH:MM): {Style.RESET_ALL}"
        ).strip()
        dt = parse_date(date_str)

        if dt is None:
            print(f"{Fore.RED}Invalid date format. Please use YYYY-MM-DD or YYYY-MM-DD HH:MM.{Style.RESET_ALL}")
            continue

        if dt < datetime.now():
            print(
                f"{Fore.RED}Deadline {dt.strftime('%Y-%m-%d %H:%M')} is in the past. "
                f"Please enter a future date.{Style.RESET_ALL}"
            )
            continue

        return dt


def prompt_valid_priority() -> str:
    """
    Prompt user for a valid priority level with color-coded options (case-insensitive).

    Returns:
        Valid priority string (Low, Medium, High)
    """
    while True:
        print(f"\n{Fore.CYAN}Priority levels:{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}Low{Style.RESET_ALL} - Low priority")
        print(f"  {Fore.YELLOW}Medium{Style.RESET_ALL} - Medium priority")
        print(f"  {Fore.RED}High{Style.RESET_ALL} - High priority")
        
        priority = input(f"{Fore.CYAN}Enter priority (Low/Medium/High): {Style.RESET_ALL}").strip().capitalize()
        if validate_priority(priority):
            priority_color = {"Low": Fore.GREEN, "Medium": Fore.YELLOW, "High": Fore.RED}
            print(f"Priority set to: {priority_color[priority]}{priority}{Style.RESET_ALL}")
            return priority
        print(f"{Fore.RED}Invalid priority. Please enter Low, Medium, or High.{Style.RESET_ALL}")


def prompt_tags() -> list:
    """
    Prompt user for task tags.

    Returns:
        List of tags (empty if user provides none)
    """
    tags_input = input(
        f"{Fore.CYAN}Enter tags (comma-separated, or press Enter for none): {Style.RESET_ALL}"
    ).strip()
    if not tags_input:
        return []
    return [tag.strip() for tag in tags_input.split(",") if tag.strip()]


def center_text(text: str, width: int = 60) -> str:
    """
    Center text within a given width, accounting for ANSI color codes.

    Args:
        text: Text to center (may contain ANSI codes)
        width: Total width for centering

    Returns:
        Centered text string
    """
    import re
    # Remove ANSI codes to calculate actual visible width
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    visible_text = ansi_escape.sub('', text)
    
    # Calculate padding needed
    padding = (width - len(visible_text)) // 2
    return " " * padding + text


def select_task_interactive(tasks: List, task_name: str = "Task") -> Optional:
    """
    Allow user to select a task interactively using arrow keys.
    
    Args:
        tasks: List of Task objects to select from
        task_name: Name to display for the tasks (e.g., "Task", "Search Result")
    
    Returns:
        Selected Task object or None if cancelled
    """
    if not tasks:
        return None
    
    if len(tasks) == 1:
        return tasks[0]
    
    selected_index = 0
    
    while True:
        # Clear and display tasks with highlight
        print("\033[2J\033[H")  # Clear screen
        print(f"\n{Fore.CYAN}Select a {task_name} (use UP/DOWN arrows, press ENTER to select):{Style.RESET_ALL}\n")
        
        for i, task in enumerate(tasks):
            if i == selected_index:
                # Highlight selected task
                print(f"{Fore.MAGENTA}>>> {i + 1}. {task}{Style.RESET_ALL}")
            else:
                priority_color = {
                    "Low": Fore.GREEN,
                    "Medium": Fore.YELLOW,
                    "High": Fore.RED,
                }.get(task.priority, "")
                print(f"    {i + 1}. {priority_color}{task}{Style.RESET_ALL}")
        
        try:
            # Read keyboard input
            key = readchar.readchar()
            
            # Arrow keys (in Windows)
            if key == '\x00':  # Extended key indicator
                next_key = readchar.readchar()
                if next_key == 'H':  # Up arrow
                    selected_index = (selected_index - 1) % len(tasks)
                elif next_key == 'P':  # Down arrow
                    selected_index = (selected_index + 1) % len(tasks)
            elif key == '\r':  # Enter key
                return tasks[selected_index]
            elif key.lower() == 'q':  # Quit/Cancel
                return None
        except Exception as e:
            # Fallback for non-Windows systems
            try:
                import sys
                if sys.platform != 'win32':
                    # For Unix-like systems, try to read escape sequences
                    if key == '\x1b':  # Escape key
                        next_key = readchar.readchar()
                        if next_key == '[':
                            direction = readchar.readchar()
                            if direction == 'A':  # Up arrow
                                selected_index = (selected_index - 1) % len(tasks)
                            elif direction == 'B':  # Down arrow
                                selected_index = (selected_index + 1) % len(tasks)
                    elif key == '\r':  # Enter key
                        return tasks[selected_index]
            except:
                pass
