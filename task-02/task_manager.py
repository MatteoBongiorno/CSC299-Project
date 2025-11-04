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
    
    def add_task(self, description, priority='medium', tags=None, notes=''):
        """Add a new task with optional tags and notes"""
        if priority not in Config.PRIORITY_LEVELS:
            priority = 'medium'
        
        task = {
            'id': len(self.tasks) + 1,
            'description': description,
            'priority': priority,
            'tags': tags or [],
            'notes': notes,
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
        """Search tasks by keyword in description or notes"""
        return [task for task in self.tasks 
                if keyword.lower() in task['description'].lower() or
                keyword.lower() in task.get('notes', '').lower()]
    
    def search_by_tag(self, tag):
        """Search tasks by tag"""
        # Remove # prefix if provided
        tag = tag.lstrip('#').lower()
        return [task for task in self.tasks 
                if any(tag == t.lstrip('#').lower() for t in task.get('tags', []))]
    
    def get_all_tags(self):
        """Get a list of all unique tags used across all tasks"""
        all_tags = set()
        for task in self.tasks:
            all_tags.update(task.get('tags', []))
        return sorted(list(all_tags))
    
    def add_note(self, task_id, note_text):
        """Add or update notes for a task"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['notes'] = note_text
                self.save_tasks()
                return True
        return False
    
    def add_tags(self, task_id, tags):
        """Add tags to a task"""
        for task in self.tasks:
            if task['id'] == task_id:
                existing_tags = task.get('tags', [])
                # Add new tags, avoid duplicates
                for tag in tags:
                    if tag not in existing_tags:
                        existing_tags.append(tag)
                task['tags'] = existing_tags
                self.save_tasks()
                return True
        return False
    
    def remove_tags(self, task_id, tags):
        """Remove tags from a task"""
        for task in self.tasks:
            if task['id'] == task_id:
                existing_tags = task.get('tags', [])
                for tag in tags:
                    if tag in existing_tags:
                        existing_tags.remove(tag)
                task['tags'] = existing_tags
                self.save_tasks()
                return True
        return False
    
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