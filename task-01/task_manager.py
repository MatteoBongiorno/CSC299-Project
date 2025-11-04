import json
import os
import sys
from datetime import datetime

class TaskManager:
    def __init__(self, filename='tasks.json'):
        self.filename = filename
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=2)
    
    def add_task(self, description, priority='medium'):
        """Add a new task"""
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'priority': priority,
            'created_at': datetime.now().isoformat(),
            'completed': False
        }
        self.tasks.append(task)
        self.save_tasks()
        print(f"✓ Task added: {description}")
    
    def list_tasks(self, show_completed=False):
        """List all tasks"""
        if not self.tasks:
            print("No tasks found.")
            return
        
        print("\n" + "="*60)
        print(f"{'ID':<5} {'Description':<30} {'Priority':<10} {'Status':<10}")
        print("="*60)
        
        for task in self.tasks:
            if not show_completed and task['completed']:
                continue
            
            status = "✓ Done" if task['completed'] else "Pending"
            print(f"{task['id']:<5} {task['description'][:30]:<30} {task['priority']:<10} {status:<10}")
        
        print("="*60 + "\n")
    
    def search_tasks(self, keyword):
        """Search tasks by keyword"""
        results = [task for task in self.tasks 
                  if keyword.lower() in task['description'].lower()]
        
        if not results:
            print(f"No tasks found matching '{keyword}'")
            return
        
        print(f"\nFound {len(results)} task(s) matching '{keyword}':")
        print("="*60)
        
        for task in results:
            status = "✓ Done" if task['completed'] else "Pending"
            print(f"ID {task['id']}: {task['description']}")
            print(f"  Priority: {task['priority']} | Status: {status}")
            print(f"  Created: {task['created_at'][:10]}")
            print("-"*60)
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                print(f"✓ Task {task_id} marked as completed")
                return
        print(f"Task {task_id} not found")
    
    def delete_task(self, task_id):
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                removed = self.tasks.pop(i)
                self.save_tasks()
                print(f"✓ Deleted: {removed['description']}")
                return
        print(f"Task {task_id} not found")


def print_help():
    """Print help message"""
    help_text = """
Task Manager CLI - Available Commands:
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


def main():
    """Main function to run the CLI"""
    tm = TaskManager()
    print("Welcome to Task Manager CLI!")
    print("Type 'help' for available commands.\n")
    
    while True:
        try:
            command = input("task> ").strip()
            
            if not command:
                continue
            
            parts = command.split(maxsplit=2)
            cmd = parts[0].lower()
            
            if cmd == 'exit' or cmd == 'quit':
                print("Goodbye!")
                break
            
            elif cmd == 'help':
                print_help()
            
            elif cmd == 'add':
                if len(parts) < 2:
                    print("Usage: add <description> [priority]")
                    continue
                
                # Check if last word is a priority level
                words = parts[1].split()
                priority = 'medium'
                description = parts[1]
                
                if len(words) > 1 and words[-1].lower() in ['low', 'medium', 'high']:
                    priority = words[-1].lower()
                    description = ' '.join(words[:-1])
                
                tm.add_task(description, priority)
            
            elif cmd == 'list':
                show_all = len(parts) > 1 and parts[1].lower() == 'all'
                tm.list_tasks(show_completed=show_all)
            
            elif cmd == 'search':
                if len(parts) < 2:
                    print("Usage: search <keyword>")
                    continue
                tm.search_tasks(parts[1])
            
            elif cmd == 'complete':
                if len(parts) < 2:
                    print("Usage: complete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    tm.complete_task(task_id)
                except ValueError:
                    print("Invalid task ID. Please provide a number.")
            
            elif cmd == 'delete':
                if len(parts) < 2:
                    print("Usage: delete <id>")
                    continue
                try:
                    task_id = int(parts[1])
                    tm.delete_task(task_id)
                except ValueError:
                    print("Invalid task ID. Please provide a number.")
            
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()