"""
Command-line interface for the Task Manager application
"""

import sys
from task_03.task_manager import TaskManager
from utils import (format_task_table, format_search_results, format_task_detail,
                   format_tags_list, parse_add_command, parse_tags,
                   print_success, print_error)
from config import Config


def print_help():
    """Print help message with available commands"""
    help_text = f"""
{Config.APP_NAME} v{Config.APP_VERSION} - Available Commands:
======================================
BASIC COMMANDS:
  add <description> [priority] [#tags]  - Add a new task (priority: low/medium/high)
  list                                  - List all pending tasks
  list all                              - List all tasks including completed
  search <keyword>                      - Search tasks by keyword
  complete <id>                         - Mark task as completed
  delete <id>                           - Delete a task

TAG COMMANDS:
  tag <id> #tag1 #tag2                 - Add tags to a task
  untag <id> #tag1 #tag2               - Remove tags from a task
  tags                                  - List all tags in use
  filter #tag                           - Show tasks with specific tag

NOTE COMMANDS:
  note <id> <note text>                - Add/update note for a task
  view <id>                             - View full task details with notes

OTHER:
  help                                  - Show this help message
  exit                                  - Exit the program

Examples:
  add "Buy groceries" high #shopping #urgent
  tag 1 #important #work
  note 1 Remember to buy milk and eggs
  filter #shopping
  view 1
"""
    print(help_text)


def handle_add(tm, args):
    """Handle the add command"""
    if len(args) < 1:
        print_error("Usage: add <description> [priority] [#tags]")
        return
    
    description, priority, tags = parse_add_command(' '.join(args))
    
    if not description:
        print_error("Task description cannot be empty")
        return
    
    task = tm.add_task(description, priority, tags)
    msg = f"Task added: {description}"
    if tags:
        msg += f" (Tags: {' '.join(tags)})"
    print_success(msg)


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


def handle_tag(tm, args):
    """Handle the tag command - add tags to a task"""
    if len(args) < 2:
        print_error("Usage: tag <id> #tag1 #tag2 ...")
        return
    
    try:
        task_id = int(args[0])
        tags = [arg for arg in args[1:] if arg.startswith('#')]
        
        if not tags:
            print_error("Please provide at least one tag (starting with #)")
            return
        
        if tm.add_tags(task_id, tags):
            print_success(f"Added tags {' '.join(tags)} to task {task_id}")
        else:
            print_error(f"Task {task_id} not found")
    except ValueError:
        print_error("Invalid task ID. Please provide a number.")


def handle_untag(tm, args):
    """Handle the untag command - remove tags from a task"""
    if len(args) < 2:
        print_error("Usage: untag <id> #tag1 #tag2 ...")
        return
    
    try:
        task_id = int(args[0])
        tags = [arg for arg in args[1:] if arg.startswith('#')]
        
        if not tags:
            print_error("Please provide at least one tag (starting with #)")
            return
        
        if tm.remove_tags(task_id, tags):
            print_success(f"Removed tags {' '.join(tags)} from task {task_id}")
        else:
            print_error(f"Task {task_id} not found")
    except ValueError:
        print_error("Invalid task ID. Please provide a number.")


def handle_tags(tm, args):
    """Handle the tags command - list all tags"""
    all_tags = tm.get_all_tags()
    print(format_tags_list(all_tags))


def handle_filter(tm, args):
    """Handle the filter command - show tasks with specific tag"""
    if len(args) < 1:
        print_error("Usage: filter #tag")
        return
    
    tag = args[0]
    results = tm.search_by_tag(tag)
    print(format_search_results(results, tag))


def handle_note(tm, args):
    """Handle the note command - add/update note for a task"""
    if len(args) < 2:
        print_error("Usage: note <id> <note text>")
        return
    
    try:
        task_id = int(args[0])
        note_text = ' '.join(args[1:])
        
        if tm.add_note(task_id, note_text):
            print_success(f"Note added to task {task_id}")
        else:
            print_error(f"Task {task_id} not found")
    except ValueError:
        print_error("Invalid task ID. Please provide a number.")


def handle_view(tm, args):
    """Handle the view command - show full task details"""
    if len(args) < 1:
        print_error("Usage: view <id>")
        return
    
    try:
        task_id = int(args[0])
        task = tm.get_task_by_id(task_id)
        print(format_task_detail(task))
    except ValueError:
        print_error("Invalid task ID. Please provide a number.")


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
    
    elif cmd == 'tag':
        handle_tag(tm, args)
    
    elif cmd == 'untag':
        handle_untag(tm, args)
    
    elif cmd == 'tags':
        handle_tags(tm, args)
    
    elif cmd == 'filter':
        handle_filter(tm, args)
    
    elif cmd == 'note':
        handle_note(tm, args)
    
    elif cmd == 'view':
        handle_view(tm, args)
    
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