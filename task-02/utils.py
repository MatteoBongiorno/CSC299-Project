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
        
        # Show tags if present
        if task.get('tags'):
            tags_str = ' '.join(task['tags'][:Config.MAX_TAGS_DISPLAY])
            lines.append(f"      Tags: {tags_str}")
    
    lines.append("=" * Config.TABLE_WIDTH + "\n")
    return "\n".join(lines)


def format_task_detail(task):
    """Format a single task with full details"""
    if not task:
        return "Task not found."
    
    lines = []
    lines.append("\n" + "=" * Config.DETAIL_WIDTH)
    lines.append(f"Task ID: {task['id']}")
    lines.append(f"Description: {task['description']}")
    lines.append(f"Priority: {task['priority']}")
    
    status = Config.STATUS_COMPLETED if task['completed'] else Config.STATUS_PENDING
    lines.append(f"Status: {status}")
    
    lines.append(f"Created: {task['created_at'][:10]}")
    
    # Display tags
    if task.get('tags'):
        lines.append(f"Tags: {' '.join(task['tags'])}")
    else:
        lines.append("Tags: None")
    
    # Display notes
    lines.append("\nNotes:")
    if task.get('notes'):
        lines.append(task['notes'])
    else:
        lines.append("  (No notes)")
    
    lines.append("=" * Config.DETAIL_WIDTH + "\n")
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
        
        if task.get('tags'):
            lines.append(f"  Tags: {' '.join(task['tags'])}")
        
        lines.append(f"  Created: {created_date}")
        lines.append("-" * Config.TABLE_WIDTH)
    
    return "\n".join(lines)


def format_tags_list(tags):
    """Format list of all tags"""
    if not tags:
        return "No tags found."
    
    lines = []
    lines.append(f"\nAll tags ({len(tags)}):")
    lines.append("=" * Config.TABLE_WIDTH)
    
    for tag in tags:
        lines.append(f"  {tag}")
    
    lines.append("=" * Config.TABLE_WIDTH + "\n")
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


def parse_tags(text):
    """Extract tags from text (words starting with #)"""
    words = text.split()
    tags = [word for word in words if word.startswith('#')]
    # Remove tags from description
    description = ' '.join([word for word in words if not word.startswith('#')])
    return description, tags


def parse_add_command(command_text):
    """Parse the add command to extract description, priority, and tags"""
    words = command_text.split()
    priority = Config.DEFAULT_PRIORITY
    
    # Extract tags
    tags = [word for word in words if word.startswith('#')]
    remaining_words = [word for word in words if not word.startswith('#')]
    
    # Check if last remaining word is a priority
    if len(remaining_words) > 1 and remaining_words[-1].lower() in Config.PRIORITY_LEVELS:
        priority = remaining_words[-1].lower()
        description = ' '.join(remaining_words[:-1])
    else:
        description = ' '.join(remaining_words)
    
    return description, priority, tags


def print_success(message):
    """Print a success message"""
    print(f"{Config.SYMBOL_SUCCESS} {message}")


def print_error(message):
    """Print an error message"""
    print(f"Error: {message}")