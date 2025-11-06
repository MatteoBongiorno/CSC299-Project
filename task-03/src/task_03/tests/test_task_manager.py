"""
Tests for the TaskManager class
"""

import pytest
import os
import json
from task_03.task_manager import TaskManager


@pytest.fixture
def temp_task_manager(tmp_path):
    """Create a TaskManager with a temporary file for testing"""
    test_file = tmp_path / "test_tasks.json"
    tm = TaskManager(filename=str(test_file))
    return tm


def test_add_task(temp_task_manager):
    """Test adding a task"""
    tm = temp_task_manager
    task = tm.add_task("Test task", priority="high")
    
    assert task['description'] == "Test task"
    assert task['priority'] == "high"
    assert task['id'] == 1
    assert task['completed'] == False


def test_add_task_with_tags(temp_task_manager):
    """Test adding a task with tags"""
    tm = temp_task_manager
    task = tm.add_task("Test task", priority="medium", tags=["#work", "#urgent"])
    
    assert task['description'] == "Test task"
    assert task['tags'] == ["#work", "#urgent"]
    assert len(tm.tasks) == 1


def test_complete_task(temp_task_manager):
    """Test marking a task as completed"""
    tm = temp_task_manager
    tm.add_task("Test task")
    
    result = tm.complete_task(1)
    assert result == True
    assert tm.tasks[0]['completed'] == True


def test_complete_nonexistent_task(temp_task_manager):
    """Test completing a task that doesn't exist"""
    tm = temp_task_manager
    result = tm.complete_task(999)
    assert result == False


def test_search_tasks(temp_task_manager):
    """Test searching tasks by keyword"""
    tm = temp_task_manager
    tm.add_task("Buy groceries")
    tm.add_task("Write report")
    tm.add_task("Buy milk")
    
    results = tm.search_tasks("buy")
    assert len(results) == 2
    assert all("buy" in task['description'].lower() for task in results)


def test_search_by_tag(temp_task_manager):
    """Test filtering tasks by tag"""
    tm = temp_task_manager
    tm.add_task("Task 1", tags=["#work", "#urgent"])
    tm.add_task("Task 2", tags=["#personal"])
    tm.add_task("Task 3", tags=["#work"])
    
    results = tm.search_by_tag("#work")
    assert len(results) == 2


def test_add_note(temp_task_manager):
    """Test adding a note to a task"""
    tm = temp_task_manager
    tm.add_task("Test task")
    
    result = tm.add_note(1, "This is a test note")
    assert result == True
    assert tm.tasks[0]['notes'] == "This is a test note"


def test_add_tags_to_existing_task(temp_task_manager):
    """Test adding tags to an existing task"""
    tm = temp_task_manager
    tm.add_task("Test task")
    
    result = tm.add_tags(1, ["#new", "#tags"])
    assert result == True
    assert "#new" in tm.tasks[0]['tags']
    assert "#tags" in tm.tasks[0]['tags']


def test_remove_tags(temp_task_manager):
    """Test removing tags from a task"""
    tm = temp_task_manager
    tm.add_task("Test task", tags=["#work", "#urgent", "#important"])
    
    result = tm.remove_tags(1, ["#urgent"])
    assert result == True
    assert "#urgent" not in tm.tasks[0]['tags']
    assert "#work" in tm.tasks[0]['tags']


def test_delete_task(temp_task_manager):
    """Test deleting a task"""
    tm = temp_task_manager
    tm.add_task("Test task")
    
    removed = tm.delete_task(1)
    assert removed is not None
    assert removed['description'] == "Test task"
    assert len(tm.tasks) == 0


def test_list_tasks_filter_completed(temp_task_manager):
    """Test listing only pending tasks"""
    tm = temp_task_manager
    tm.add_task("Task 1")
    tm.add_task("Task 2")
    tm.complete_task(1)
    
    pending = tm.list_tasks(show_completed=False)
    assert len(pending) == 1
    assert pending[0]['description'] == "Task 2"


def test_get_all_tags(temp_task_manager):
    """Test getting all unique tags"""
    tm = temp_task_manager
    tm.add_task("Task 1", tags=["#work", "#urgent"])
    tm.add_task("Task 2", tags=["#personal", "#work"])
    
    all_tags = tm.get_all_tags()
    assert len(all_tags) == 3
    assert "#work" in all_tags
    assert "#urgent" in all_tags
    assert "#personal" in all_tags