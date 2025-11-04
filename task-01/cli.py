"""
Command-line interface for the Task Manager application
"""

import sys
from task_manager import TaskManager
from utils import (format_task_table, format_search_results, 
                   parse_add_command, print_success, print_error)
from config import Config


def print_help():
    """Print help message with available commands"""
    help_text = f"""
{Config.APP_NAME} v{Config.APP_VERSION} - Available Commands:
======================================
add <description> [priority]  - Add a new task (priority: low/medium/high)
list                          - List all pending tasks
list all                      - List all tasks including completed
search <keyword>              - Search tasks by keyword
complete <id>                 - Mark task as completed
delete <id>                   - Delete a task
help                          - Show this help message
exit                          - Exit the program

Examples:
  add "Buy groceries" high
  search groceries
  complete 1
  delete 2
"""
    print(help_text)


def handle_add(tm, args):
    """Handle the add command"""
    if len(args) < 1:
        print_error("Usage: add <description> [priority]")
        return
    
    description, priority = parse_add_command(' '.join(args))
    task = tm.add_task(description, priority)
    print_success(f"Task added: {description}")


def handle_list(tm, args):
    """Handle the list command"""
    show_all = len(args) > 0 and args[0].lower() == 'all'
    tasks = tm.list_tasks(show_completed=show_all)
    print(format_task_table(tasks))


def handle_search(tm, args):
    """Handle the search command"""
    if len(args) < 1:
        print_error("Usage: search <keyword>")
        return
    
    keyword = ' '.join(args)
    results = tm.search_tasks(keyword)
    print(format_search_results(results, keyword))


def handle_complete(tm, args):
    """Handle the complete command"""
    if len(args) < 1:
        print_error("Usage: complete <id>")
        return
    
    try:
        task_id = int(args[0])
        if tm.complete_task(task_id):
            print_success(f"Task {task_id} marked as completed")
        else:
            print_error(f"Task {task_id} not found")
    except ValueError:
        print_error("Invalid task ID. Please provide a number.")


def handle_delete(tm, args):
    """Handle the delete command"""
    if len(args) < 1:
        print_error("Usage: delete <id>")
        return
    
    try:
        task_id = int(args[0])
        removed = tm.delete_task(task_id)
        if removed:
            print_success(f"Deleted: {removed['description']}")
        else:
            print_error(f"Task {task_id} not found")
    except ValueError:
        print_error("Invalid task ID. Please provide a number.")


def process_command(tm, command):
    """Process a single command"""
    parts = command.split(maxsplit=1)
    if not parts:
        return True
    
    cmd = parts[0].lower()
    args = parts[1].split() if len(parts) > 1 else []
    
    if cmd in ['exit', 'quit']:
        print("Goodbye!")
        return False
    
    elif cmd == 'help':
        print_help()
    
    elif cmd == 'add':
        handle_add(tm, args)
    
    elif cmd == 'list':
        handle_list(tm, args)
    
    elif cmd == 'search':
        handle_search(tm, args)
    
    elif cmd == 'complete':
        handle_complete(tm, args)
    
    elif cmd == 'delete':
        handle_delete(tm, args)
    
    else:
        print_error(f"Unknown command: {cmd}")
        print("Type 'help' for available commands.")
    
    return True


def main():
    """Main function to run the CLI"""
    tm = TaskManager()
    print(f"Welcome to {Config.APP_NAME}!")
    print("Type 'help' for available commands.\n")
    
    while True:
        try:
            command = input("task> ").strip()
            
            if not command:
                continue
            
            if not process_command(tm, command):
                break
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print_error(str(e))


if __name__ == "__main__":
    main()