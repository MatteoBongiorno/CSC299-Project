"""
Utility functions for input validation and date handling.
"""
from datetime import datetime
from typing import Optional, List
from colorama import Fore, Style, init
import sys
import os

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
    Allow user to select a task interactively using arrow keys or number selection.
    
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
    
    # Try to enable raw input mode for arrow keys
    try:
        import tty
        import termios
        return _select_task_arrows_unix(tasks, task_name)
    except ImportError:
        # Fallback to number selection on Windows
        return _select_task_numbers(tasks, task_name)


def _select_task_arrows_unix(tasks: List, task_name: str) -> Optional:
    """
    Arrow key selection for Unix-like terminals (Git Bash, Linux, macOS).
    
    Args:
        tasks: List of Task objects to select from
        task_name: Name to display for the tasks
    
    Returns:
        Selected Task object or None if cancelled
    """
    import tty
    import termios
    
    selected_index = 0
    
    print(f"\n{Fore.CYAN}Use UP/DOWN arrow keys or 1-{len(tasks)} to navigate, ENTER to select, Q to cancel:{Style.RESET_ALL}\n")
    
    # Save terminal settings
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        # Set terminal to raw mode
        tty.setraw(fd)
        
        while True:
            # Move cursor to beginning and clear
            sys.stdout.write(f"\r\033[2K")
            sys.stdout.write(f"\n{Fore.CYAN}Select a {task_name}:{Style.RESET_ALL}\n")
            
            # Display all tasks
            line_count = 0
            for i, task in enumerate(tasks):
                priority_color = {
                    "Low": Fore.GREEN,
                    "Medium": Fore.YELLOW,
                    "High": Fore.RED,
                }.get(task.priority, "")
                
                if i == selected_index:
                    sys.stdout.write(f"{Fore.MAGENTA}>>> {i + 1}. {priority_color}{task}{Style.RESET_ALL}\n")
                else:
                    sys.stdout.write(f"    {i + 1}. {priority_color}{task}{Style.RESET_ALL}\n")
                line_count += 1
            
            sys.stdout.write(f"\n{Fore.CYAN}[Selection: {selected_index + 1}/{len(tasks)}]{Style.RESET_ALL}\n")
            sys.stdout.flush()
            
            # Read input character by character
            char = sys.stdin.read(1)
            
            if char == '\r' or char == '\n':  # Enter
                return tasks[selected_index]
            elif char.lower() == 'q':  # Quit
                return None
            elif char.isdigit():  # Number input
                digit = int(char)
                if 1 <= digit <= len(tasks):
                    selected_index = digit - 1
                    # Clear previous lines
                    sys.stdout.write(f"\033[{line_count + 4}A\033[J")
                else:
                    continue
            elif char == '\x1b':  # Escape sequence
                # Read the next two characters
                try:
                    next_char1 = sys.stdin.read(1)
                    if next_char1 == '[':
                        next_char2 = sys.stdin.read(1)
                        if next_char2 == 'A':  # Up arrow
                            selected_index = (selected_index - 1) % len(tasks)
                            # Clear previous lines
                            sys.stdout.write(f"\033[{line_count + 4}A\033[J")
                        elif next_char2 == 'B':  # Down arrow
                            selected_index = (selected_index + 1) % len(tasks)
                            # Clear previous lines
                            sys.stdout.write(f"\033[{line_count + 4}A\033[J")
                except:
                    pass
    
    finally:
        # Restore terminal settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        print()  # New line after selection


def _select_task_arrows(tasks: List, task_name: str) -> Optional:
    """
    Windows-specific arrow key selection using msvcrt.
    
    Args:
        tasks: List of Task objects to select from
        task_name: Name to display for the tasks
    
    Returns:
        Selected Task object or None if cancelled
    """
    try:
        import msvcrt
    except ImportError:
        return _select_task_numbers(tasks, task_name)
    
    selected_index = 0
    
    print(f"\n{Fore.CYAN}Use UP/DOWN arrow keys to navigate, ENTER to select, Q to cancel:{Style.RESET_ALL}\n")
    
    while True:
        # Clear previous output
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"\n{Fore.CYAN}Select a {task_name} (UP/DOWN arrows, ENTER to select):{Style.RESET_ALL}\n")
        
        # Display all tasks
        for i, task in enumerate(tasks):
            if i == selected_index:
                # Highlight selected task
                priority_color = {
                    "Low": Fore.GREEN,
                    "Medium": Fore.YELLOW,
                    "High": Fore.RED,
                }.get(task.priority, "")
                print(f"{Fore.MAGENTA}>>> {i + 1}. {priority_color}{task}{Style.RESET_ALL}")
            else:
                priority_color = {
                    "Low": Fore.GREEN,
                    "Medium": Fore.YELLOW,
                    "High": Fore.RED,
                }.get(task.priority, "")
                print(f"    {i + 1}. {priority_color}{task}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}[Selection: {selected_index + 1}/{len(tasks)}]{Style.RESET_ALL}")
        
        # Get keyboard input
        if msvcrt.kbhit():
            key = msvcrt.getch()
            
            # Check for escape sequence (arrow keys)
            if key == b'\xe0':  # Arrow key prefix
                direction = msvcrt.getch()
                if direction == b'H':  # Up arrow
                    selected_index = (selected_index - 1) % len(tasks)
                elif direction == b'P':  # Down arrow
                    selected_index = (selected_index + 1) % len(tasks)
            elif key == b'\r':  # Enter
                return tasks[selected_index]
            elif key.lower() == b'q':  # Quit
                return None


def _select_task_numbers(tasks: List, task_name: str) -> Optional:
    """
    Fallback number-based selection for all platforms.
    
    Args:
        tasks: List of Task objects to select from
        task_name: Name to display for the tasks
    
    Returns:
        Selected Task object or None if cancelled
    """
    # Display tasks with numbers
    print(f"\n{Fore.CYAN}Select a {task_name}:{Style.RESET_ALL}\n")
    
    for i, task in enumerate(tasks):
        priority_color = {
            "Low": Fore.GREEN,
            "Medium": Fore.YELLOW,
            "High": Fore.RED,
        }.get(task.priority, "")
        print(f"{i + 1}. {priority_color}{task}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Enter the number of the task to select (1-{len(tasks)}) or 'q' to cancel:{Style.RESET_ALL}")
    
    while True:
        selection = input("Your choice: ").strip().lower()
        
        if selection == 'q':
            return None
        
        try:
            index = int(selection) - 1
            if 0 <= index < len(tasks):
                return tasks[index]
            else:
                print(f"{Fore.RED}Invalid selection. Please enter a number between 1 and {len(tasks)}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter a number or 'q' to cancel.{Style.RESET_ALL}")
