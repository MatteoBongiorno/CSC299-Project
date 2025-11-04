"""
Utility functions for formatting and displaying tasks
"""

from config import Config

def format_task_table(tasks):
    """Format tasks as a table for display"""
    if not tasks:
        return "No tasks found."
    
    lines = []
    lines.append("\n" + "=" * Config.TABLE_WIDTH)
    
    # Header
    header = (f"{'ID':<{Config.COLUMN_WIDTHS['id']}} "
              f"{'Description':<{Config.COLUMN_WIDTHS['description']}} "
              f"{'Priority':<{Config.COLUMN_WIDTHS['priority']}} "
              f"{'Status':<{Config.COLUMN_WIDTHS['status']}}")
    lines.append(header)
    lines.append("=" * Config.TABLE_WIDTH)
    
    # Task rows
    for task in tasks:
        status = Config.STATUS_COMPLETED if task['completed'] else Config.STATUS_PENDING
        description = truncate_text(task['description'], Config.DESCRIPTION_MAX_LENGTH)
        
        row = (f"{task['id']:<{Config.COLUMN_WIDTHS['id']}} "
               f"{description:<{Config.COLUMN_WIDTHS['description']}} "
               f"{task['priority']:<{Config.COLUMN_WIDTHS['priority']}} "
               f"{status:<{Config.COLUMN_WIDTHS['status']}}")
        lines.append(row)
    
    lines.append("=" * Config.TABLE_WIDTH + "\n")
    return "\n".join(lines)


def format_search_results(tasks, keyword):
    """Format search results for display"""
    if not tasks:
        return f"No tasks found matching '{keyword}'"
    
    lines = []
    lines.append(f"\nFound {len(tasks)} task(s) matching '{keyword}':")
    lines.append("=" * Config.TABLE_WIDTH)
    
    for task in tasks:
        status = Config.STATUS_COMPLETED if task['completed'] else Config.STATUS_PENDING
        created_date = task['created_at'][:10]
        
        lines.append(f"ID {task['id']}: {task['description']}")
        lines.append(f"  Priority: {task['priority']} | Status: {status}")
        lines.append(f"  Created: {created_date}")
        lines.append("-" * Config.TABLE_WIDTH)
    
    return "\n".join(lines)


def truncate_text(text, max_length):
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length]


def validate_priority(priority):
    """Validate and normalize priority level"""
    priority = priority.lower()
    if priority in Config.PRIORITY_LEVELS:
        return priority
    return Config.DEFAULT_PRIORITY


def parse_add_command(command_text):
    """Parse the add command to extract description and priority"""
    words = command_text.split()
    priority = Config.DEFAULT_PRIORITY
    description = command_text
    
    # Check if last word is a valid priority
    if len(words) > 1 and words[-1].lower() in Config.PRIORITY_LEVELS:
        priority = words[-1].lower()
        description = ' '.join(words[:-1])
    
    return description, priority


def print_success(message):
    """Print a success message"""
    print(f"{Config.SYMBOL_SUCCESS} {message}")


def print_error(message):
    """Print an error message"""
    print(f"Error: {message}")