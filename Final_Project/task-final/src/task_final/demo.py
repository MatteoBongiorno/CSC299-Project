"""
Demo script showing task manager usage programmatically.
"""
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from task_final.models import Task, TaskCollection

def demo():
    """Run a demo of the task manager functionality."""
    print("=" * 70)
    print("TASK MANAGER DEMO")
    print("=" * 70)
    
    collection = TaskCollection()
    now = datetime.now()
    
    # Create sample tasks
    print("\n📝 Creating 4 sample tasks...\n")
    
    tasks_data = [
        ("Complete project report", "High", now + timedelta(days=2), ["work", "urgent"]),
        ("Review team proposals", "Medium", now + timedelta(days=4), ["work", "admin"]),
        ("Personal project research", "Low", now + timedelta(days=7), ["personal"]),
        ("Email client communication", "High", now + timedelta(days=1), ["work", "customer"]),
    ]
    
    for name, priority, deadline, tags in tasks_data:
        task = Task(name=name, priority=priority, deadline=deadline, tags=tags)
        collection.add_task(task)
        print(f"✓ Created: {name} (Priority: {priority})")
    
    # Display all tasks
    print(f"\n{'='*70}")
    print("📋 ALL TASKS IN COLLECTION")
    print(f"{'='*70}")
    print(collection.display_all_tasks())
    
    # Search by priority
    print(f"\n{'='*70}")
    print("🔍 SEARCH BY PRIORITY (High)")
    print(f"{'='*70}")
    high_priority = collection.search_by_priority("High")
    print(f"Found {len(high_priority)} High-priority task(s):")
    for task in high_priority:
        print(f"\n{task}")
    
    # Search by tags
    print(f"\n{'='*70}")
    print("🔍 SEARCH BY TAG (work)")
    print(f"{'='*70}")
    work_tasks = collection.search_by_tags(["work"], match_all=False)
    print(f"Found {len(work_tasks)} task(s) tagged with 'work':")
    for task in work_tasks:
        print(f"\n{task}")
    
    # Search by name
    print(f"\n{'='*70}")
    print("🔍 SEARCH BY NAME (partial: 'project')")
    print(f"{'='*70}")
    project_tasks = collection.search_by_name("project", exact=False)
    print(f"Found {len(project_tasks)} task(s) with 'project':")
    for task in project_tasks:
        print(f"\n{task}")
    
    # Sort by priority
    print(f"\n{'='*70}")
    print("📊 SORTED BY PRIORITY (High → Medium → Low)")
    print(f"{'='*70}")
    sorted_priority = collection.sort_by_priority()
    for i, task in enumerate(sorted_priority, 1):
        print(f"\n{i}. {task.name} - Priority: {task.priority}")
    
    # Sort by deadline
    print(f"\n{'='*70}")
    print("📅 SORTED BY DEADLINE (Earliest First)")
    print(f"{'='*70}")
    sorted_deadline = collection.sort_by_deadline()
    for i, task in enumerate(sorted_deadline, 1):
        print(f"\n{i}. {task.name}")
        print(f"   Deadline: {task.deadline.strftime('%Y-%m-%d %H:%M')}")
    
    # Edit a task
    print(f"\n{'='*70}")
    print("✏️  EDITING A TASK")
    print(f"{'='*70}")
    task_to_edit = sorted_priority[0]
    print(f"Original: {task_to_edit.name} (Priority: {task_to_edit.priority})")
    task_to_edit.tags.append("critical")
    print(f"Updated tags: {task_to_edit.tags}")
    
    # Delete a task
    print(f"\n{'='*70}")
    print("🗑️  DELETING A TASK")
    print(f"{'='*70}")
    task_to_delete = collection.get_all_tasks()[2]
    print(f"Deleting: {task_to_delete.name}")
    collection.remove_task(task_to_delete.id)
    print(f"✓ Deleted successfully")
    print(f"Collection now has {len(collection)} tasks")
    
    # Test past date validation
    print(f"\n{'='*70}")
    print("⚠️  PAST DATE VALIDATION")
    print(f"{'='*70}")
    past_date = datetime.now() - timedelta(days=1)
    try:
        invalid_task = Task(
            name="Invalid task",
            priority="High",
            deadline=past_date,
            tags=["test"]
        )
    except ValueError as e:
        print(f"✓ Validation error caught (as expected):")
        print(f"  {e}")
    
    print(f"\n{'='*70}")
    print("✅ DEMO COMPLETE")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    demo()
