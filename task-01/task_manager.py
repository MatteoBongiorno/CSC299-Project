import json
import os
from datetime import datetime
from config import Config

class TaskManager:
    """Main class for managing tasks with JSON storage"""
    
    def __init__(self, filename=None):
        self.filename = filename or Config.DEFAULT_FILENAME
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
            json.dump(self.tasks, f, indent=Config.JSON_INDENT)
    
    def add_task(self, description, priority='medium'):
        """Add a new task"""
        if priority not in Config.PRIORITY_LEVELS:
            priority = 'medium'
        
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'priority': priority,
            'created_at': datetime.now().isoformat(),
            'completed': False
        }
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def list_tasks(self, show_completed=False):
        """List all tasks, optionally filtering by completion status"""
        if not self.tasks:
            return []
        
        if show_completed:
            return self.tasks
        else:
            return [task for task in self.tasks if not task['completed']]
    
    def search_tasks(self, keyword):
        """Search tasks by keyword in description"""
        return [task for task in self.tasks 
                if keyword.lower() in task['description'].lower()]
    
    def complete_task(self, task_id):
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id):
        """Delete a task by ID"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                removed_task = self.tasks.pop(i)
                self.save_tasks()
                return removed_task
        return None
    
    def get_task_by_id(self, task_id):
        """Retrieve a specific task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None