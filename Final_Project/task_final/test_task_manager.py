"""
Unit tests for the Task Manager application.
"""
import pytest
from datetime import datetime, timedelta
from task_final.models import Task, TaskCollection


class TestTask:
    """Tests for Task model."""

    def test_task_creation_valid(self):
        """Test creating a valid task."""
        future_date = datetime.now() + timedelta(days=1)
        task = Task(
            name="Complete report",
            priority="High",
            deadline=future_date,
            tags=["work", "urgent"],
        )
        assert task.name == "Complete report"
        assert task.priority == "High"
        assert task.deadline == future_date
        assert task.tags == ["work", "urgent"]
        assert task.id is not None

    def test_task_creation_empty_name(self):
        """Test that empty task name raises error."""
        future_date = datetime.now() + timedelta(days=1)
        with pytest.raises(ValueError, match="Task name cannot be empty"):
            Task(name="", priority="Low", deadline=future_date)

    def test_task_creation_invalid_priority(self):
        """Test that invalid priority raises error."""
        future_date = datetime.now() + timedelta(days=1)
        with pytest.raises(ValueError, match="Priority must be one of"):
            Task(name="Test task", priority="Critical", deadline=future_date)

    def test_task_creation_past_deadline(self):
        """Test that past deadline raises error."""
        past_date = datetime.now() - timedelta(days=1)
        with pytest.raises(ValueError, match="Deadline .* is in the past"):
            Task(name="Old task", priority="Low", deadline=past_date)

    def test_task_creation_no_tags(self):
        """Test creating a task without tags."""
        future_date = datetime.now() + timedelta(days=1)
        task = Task(name="Simple task", priority="Medium", deadline=future_date)
        assert task.tags == []

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        future_date = datetime.now() + timedelta(days=1)
        task = Task(
            name="Test task", priority="High", deadline=future_date, tags=["test"]
        )
        task_dict = task.to_dict()
        assert task_dict["name"] == "Test task"
        assert task_dict["priority"] == "High"
        assert task_dict["tags"] == ["test"]

    def test_task_from_dict(self):
        """Test creating task from dictionary."""
        future_date = datetime.now() + timedelta(days=1)
        task_dict = {
            "id": "test-id-123",
            "name": "Dict task",
            "priority": "Low",
            "deadline": future_date.isoformat(),
            "tags": ["dict"],
        }
        task = Task.from_dict(task_dict)
        assert task.id == "test-id-123"
        assert task.name == "Dict task"
        assert task.priority == "Low"


class TestTaskCollection:
    """Tests for TaskCollection model."""

    @pytest.fixture
    def collection(self):
        """Create an empty task collection for testing."""
        return TaskCollection()

    @pytest.fixture
    def sample_tasks(self):
        """Create sample tasks for testing."""
        now = datetime.now()
        tasks = [
            Task(
                name="Email client",
                priority="High",
                deadline=now + timedelta(days=1),
                tags=["work", "urgent"],
            ),
            Task(
                name="Email invoice",
                priority="Medium",
                deadline=now + timedelta(days=2),
                tags=["work", "accounting"],
            ),
            Task(
                name="Call customer",
                priority="High",
                deadline=now + timedelta(days=1),
                tags=["work", "customer"],
            ),
            Task(
                name="Personal project",
                priority="Low",
                deadline=now + timedelta(days=7),
                tags=["personal"],
            ),
        ]
        return tasks

    def test_add_task(self, collection, sample_tasks):
        """Test adding tasks to collection."""
        collection.add_task(sample_tasks[0])
        assert len(collection) == 1
        assert sample_tasks[0] in collection.get_all_tasks()

    def test_remove_task(self, collection, sample_tasks):
        """Test removing a task by ID."""
        task = sample_tasks[0]
        collection.add_task(task)
        assert len(collection) == 1

        success = collection.remove_task(task.id)
        assert success is True
        assert len(collection) == 0

    def test_remove_nonexistent_task(self, collection):
        """Test removing a task that doesn't exist."""
        success = collection.remove_task("nonexistent-id")
        assert success is False

    def test_get_task_by_id(self, collection, sample_tasks):
        """Test retrieving a task by ID."""
        task = sample_tasks[0]
        collection.add_task(task)

        retrieved = collection.get_task_by_id(task.id)
        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.name == task.name

    def test_get_nonexistent_task(self, collection):
        """Test retrieving a task that doesn't exist."""
        retrieved = collection.get_task_by_id("nonexistent-id")
        assert retrieved is None

    def test_search_by_name_partial(self, collection, sample_tasks):
        """Test searching by name with partial matching."""
        for task in sample_tasks:
            collection.add_task(task)

        results = collection.search_by_name("Email", exact=False)
        assert len(results) == 2
        assert any(t.name == "Email client" for t in results)
        assert any(t.name == "Email invoice" for t in results)

    def test_search_by_name_exact(self, collection, sample_tasks):
        """Test searching by name with exact matching."""
        for task in sample_tasks:
            collection.add_task(task)

        results = collection.search_by_name("Email client", exact=True)
        assert len(results) == 1
        assert results[0].name == "Email client"

    def test_search_by_name_case_insensitive(self, collection, sample_tasks):
        """Test that name search is case-insensitive."""
        for task in sample_tasks:
            collection.add_task(task)

        results = collection.search_by_name("email", exact=False)
        assert len(results) == 2

    def test_search_by_priority(self, collection, sample_tasks):
        """Test searching by priority."""
        for task in sample_tasks:
            collection.add_task(task)

        high_priority = collection.search_by_priority("High")
        assert len(high_priority) == 2

        low_priority = collection.search_by_priority("Low")
        assert len(low_priority) == 1

    def test_search_by_invalid_priority(self, collection, sample_tasks):
        """Test searching by invalid priority returns empty list."""
        for task in sample_tasks:
            collection.add_task(task)

        results = collection.search_by_priority("Critical")
        assert len(results) == 0

    def test_search_by_deadline(self, collection, sample_tasks):
        """Test searching by deadline."""
        for task in sample_tasks:
            collection.add_task(task)

        tomorrow = (datetime.now() + timedelta(days=1)).date()
        results = collection.search_by_deadline(datetime.combine(tomorrow, datetime.min.time()))
        assert len(results) == 2  # Email client and Call customer

    def test_search_by_tags_any(self, collection, sample_tasks):
        """Test searching by tags (any match)."""
        for task in sample_tasks:
            collection.add_task(task)

        results = collection.search_by_tags(["urgent"], match_all=False)
        assert len(results) == 1
        assert results[0].name == "Email client"

        results = collection.search_by_tags(["work"], match_all=False)
        assert len(results) == 3  # All work-tagged tasks

    def test_search_by_tags_all(self, collection, sample_tasks):
        """Test searching by tags (all must match)."""
        for task in sample_tasks:
            collection.add_task(task)

        results = collection.search_by_tags(["work", "urgent"], match_all=True)
        assert len(results) == 1
        assert results[0].name == "Email client"

    def test_sort_by_name(self, collection, sample_tasks):
        """Test sorting by name."""
        for task in sample_tasks:
            collection.add_task(task)

        sorted_tasks = collection.sort_by_name()
        names = [t.name for t in sorted_tasks]
        assert names == sorted(names)

    def test_sort_by_priority(self, collection, sample_tasks):
        """Test sorting by priority (High > Medium > Low)."""
        for task in sample_tasks:
            collection.add_task(task)

        sorted_tasks = collection.sort_by_priority()
        priorities = [t.priority for t in sorted_tasks]

        # High priority should come first, then Medium, then Low
        assert priorities.index("High") < priorities.index("Medium")
        assert priorities.index("Medium") < priorities.index("Low")

    def test_sort_by_deadline(self, collection, sample_tasks):
        """Test sorting by deadline (earliest first)."""
        for task in sample_tasks:
            collection.add_task(task)

        sorted_tasks = collection.sort_by_deadline()
        deadlines = [t.deadline for t in sorted_tasks]

        # Deadlines should be in ascending order
        for i in range(len(deadlines) - 1):
            assert deadlines[i] <= deadlines[i + 1]

    def test_get_all_tasks(self, collection, sample_tasks):
        """Test retrieving all tasks."""
        for task in sample_tasks:
            collection.add_task(task)

        all_tasks = collection.get_all_tasks()
        assert len(all_tasks) == len(sample_tasks)

    def test_empty_collection(self, collection):
        """Test operations on empty collection."""
        assert len(collection) == 0
        assert collection.get_all_tasks() == []
        assert collection.search_by_name("anything") == []
        assert collection.sort_by_priority() == []

    def test_collection_len(self, collection, sample_tasks):
        """Test getting collection length."""
        for i, task in enumerate(sample_tasks, 1):
            collection.add_task(task)
            assert len(collection) == i


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
