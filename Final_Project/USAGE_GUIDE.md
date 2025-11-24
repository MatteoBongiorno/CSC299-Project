# Task Manager - Usage Guide & Examples

## Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Running the Application](#running-the-application)
3. [Menu Operations](#menu-operations)
4. [Example Workflows](#example-workflows)
5. [Troubleshooting](#troubleshooting)

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\potat\CSC299-Project\Final_Project
```

### Step 2: Activate Virtual Environment (if not already active)
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install pytest colorama openai python-dotenv
```

### Step 4: Set up OpenAI API Key (Optional, for task summarization)
```bash
# Create a .env file in the project directory with:
OPENAI_API_KEY=your_api_key_here
```
Get your API key from: https://platform.openai.com/api-keys

---

## Running the Application

### Option 1: Run Interactive CLI (Recommended)
```bash
python -m task_final
```

### Option 2: Run via __main__.py
```bash
python task_final/__main__.py
```

### Option 3: Run Demo (Non-interactive)
```bash
python task_final/demo.py
```

### Option 4: Run Tests
```bash
python -m pytest task_final/test_task_manager.py -v
```

---

## Menu Operations

### Main Menu
```
============================================================
Main Menu
============================================================
1. Create a new task
2. View all tasks
3. Search tasks
4. Sort tasks
5. Edit a task
6. Delete a task
7. Summarize a task
8. Exit
```

---

## Example Workflows

### Workflow 1: Basic Task Management

#### Step 1: Start Application
```bash
$ python -m task_05

============================================================
Welcome to Task Manager
============================================================
```

#### Step 2: Create First Task
```
Enter your choice: 1

--- Create New Task ---
Enter task name: Complete quarterly report
Enter priority (Low/Medium/High): High
Enter deadline (YYYY-MM-DD or YYYY-MM-DD HH:MM): 2025-11-25
Enter tags (comma-separated, or press Enter for none): work, urgent, quarterly

✓ Task created successfully!
Task ID: a1b2c3d4-e5f6...
```

#### Step 3: Create Second Task
```
Enter your choice: 1

--- Create New Task ---
Enter task name: Review team documentation
Enter priority (Low/Medium/High): Medium
Enter deadline (YYYY-MM-DD or YYYY-MM-DD HH:MM): 2025-11-30
Enter tags (comma-separated, or press Enter for none): work, documentation

✓ Task created successfully!
Task ID: f7g8h9i0-j1k2...
```

#### Step 4: View All Tasks
```
Enter your choice: 2

--- All Tasks ---
Tasks in collection (2 total):
============================================================

1. [H] Complete quarterly report
   Deadline: 2025-11-25 23:59
   Tags: work, urgent, quarterly
   ID: a1b2c3d4-e5f...

2. [M] Review team documentation
   Deadline: 2025-11-30 23:59
   Tags: work, documentation
   ID: f7g8h9i0-j1k...
============================================================
```

---

### Workflow 2: Searching Tasks

#### Search by Name
```
Enter your choice: 3

--- Search Tasks ---
Search by:
1. Name
2. Priority
3. Deadline
4. Tags

Enter search type (1-4): 1
Enter name to search for: report

Found 1 task(s):

1. [H] Complete quarterly report
   Deadline: 2025-11-25 23:59
   Tags: work, urgent, quarterly
   ID: a1b2c3d4-e5f...
```

#### Search by Priority
```
Enter your choice: 3

--- Search Tasks ---
Search by:
1. Name
2. Priority
3. Deadline
4. Tags

Enter search type (1-4): 2
Enter priority (Low/Medium/High): High

Found 1 task(s) with priority 'High':

1. [H] Complete quarterly report
   Deadline: 2025-11-25 23:59
   Tags: work, urgent, quarterly
   ID: a1b2c3d4-e5f...
```

#### Search by Tags
```
Enter your choice: 3

--- Search Tasks ---
Search by:
1. Name
2. Priority
3. Deadline
4. Tags

Enter search type (1-4): 4
Enter tags (comma-separated, or press Enter for none): work

Found 2 task(s) with tags ['work']:

1. [H] Complete quarterly report
   Deadline: 2025-11-25 23:59
   Tags: work, urgent, quarterly
   ID: a1b2c3d4-e5f...

2. [M] Review team documentation
   Deadline: 2025-11-30 23:59
   Tags: work, documentation
   ID: f7g8h9i0-j1k...
```

---

### Workflow 3: Sorting Tasks

#### Sort by Priority
```
Enter your choice: 4

--- Sort Tasks ---
Sort by:
1. Name (alphabetical)
2. Priority (High to Low)
3. Deadline (earliest first)

Enter sort type (1-3): 2

Tasks sorted by priority (High → Medium → Low):

1. [H] Complete quarterly report
   Deadline: 2025-11-25 23:59
   Tags: work, urgent, quarterly

2. [M] Review team documentation
   Deadline: 2025-11-30 23:59
   Tags: work, documentation
```

#### Sort by Deadline
```
Enter your choice: 4

--- Sort Tasks ---
Sort by:
1. Name (alphabetical)
2. Priority (High to Low)
3. Deadline (earliest first)

Enter sort type (1-3): 3

Tasks sorted by deadline (earliest first):

1. [H] Complete quarterly report
   Deadline: 2025-11-25 23:59

2. [M] Review team documentation
   Deadline: 2025-11-30 23:59
```

---

### Workflow 4: Editing Tasks

#### Get Task ID First
```
Enter your choice: 2  # View all tasks to get ID
```

#### Edit a Task
```
Enter your choice: 5

--- Edit Task ---
Enter task ID to edit: a1b2c3d4-e5f6

Current task: [H] Complete quarterly report
   Deadline: 2025-11-25 23:59
   Tags: work, urgent, quarterly

What would you like to edit?
1. Name
2. Priority
3. Deadline
4. Tags
5. Cancel

Enter choice (1-5): 2
Enter priority (Low/Medium/High): Critical  # Invalid!
Invalid priority. Please enter Low, Medium, or High.
Enter priority (Low/Medium/High): High

✓ Priority updated.
```

#### Update Tags
```
Enter choice (1-5): 4
Enter tags (comma-separated, or press Enter for none): work, urgent, quarterly, critical

✓ Tags updated.
```

---

### Workflow 5: Deleting Tasks

#### Delete a Task
```
Enter your choice: 6

--- Delete Task ---
Enter task ID to delete: a1b2c3d4-e5f6
Are you sure you want to delete task a1b2c3d4-e5f...? (yes/no): yes

✓ Task deleted successfully.
```

#### Cancel Deletion
```
Enter your choice: 6

--- Delete Task ---
Enter task ID to delete: f7g8h9i0-j1k2
Are you sure you want to delete task f7g8h9i0-j1k...? (yes/no): no

Delete cancelled.
```

---

### Workflow 6: Past Date Validation

#### Try to Create Task with Past Date
```
Enter your choice: 1

--- Create New Task ---
Enter task name: Finish old project
Enter priority (Low/Medium/High): Low
Enter deadline (YYYY-MM-DD or YYYY-MM-DD HH:MM): 2025-11-15

Deadline 2025-11-15 23:59 is in the past. Please enter a future date.
Enter deadline (YYYY-MM-DD or YYYY-MM-DD HH:MM): 2025-12-01

✓ Task created successfully!
Task ID: x1y2z3a4-b5c6...
```

---

## Common Task Scenarios

### Scenario 1: Project Manager Creating Sprint Tasks

```python
# Create multiple tasks for sprint
Tasks:
1. "Design system architecture" - High - 2025-11-20 - [sprint, design, backend]
2. "Implement API endpoints" - High - 2025-11-25 - [sprint, backend, api]
3. "Write API documentation" - Medium - 2025-11-27 - [sprint, documentation]
4. "Code review team PRs" - Medium - 2025-11-28 - [sprint, review]
5. "Release notes and testing" - High - 2025-11-30 - [sprint, testing, release]

# View by priority
Sort by Priority → Shows tasks in order of urgency

# Search by tag
Search "sprint" → Shows all sprint tasks

# Sort by deadline
Sort by Deadline → Shows what's due first
```

### Scenario 2: Personal Productivity

```python
# Tasks:
1. "Gym - Cardio session" - Low - 2025-11-20 - [personal, health]
2. "Grocery shopping" - Medium - 2025-11-19 - [personal, errands]
3. "Learn Python" - Low - 2025-11-25 - [personal, learning]
4. "Call Mom" - High - 2025-11-20 - [personal, important]

# Get urgent items
Search "personal", then Search "High" → Shows high-priority personal tasks

# Plan today
Sort by Deadline → See what's due today

# After completing groceries
Delete task → Removes "Grocery shopping"
```

### Scenario 3: Work Deadline Management

```python
# Create tasks with approaching deadlines
1. "Submit proposal" - High - 2025-11-19 - [deadline, urgent]
2. "Client presentation" - High - 2025-11-21 - [deadline, client]
3. "Budget review" - Medium - 2025-11-23 - [deadline, admin]

# Monitor priorities
Sort by Priority → Identifies most critical work

# Track by deadline
Sort by Deadline → See what's due soonest

# Adjust on progress
Edit task → Update priority as you work through items
```

---

## Troubleshooting

### Issue: "No module named 'task_05'"

**Solution:**
```bash
# Make sure you're in the correct directory
cd c:\Users\potat\CSC299-task-05\task-05

# Ensure virtual environment is activated
.venv\Scripts\activate

# Try running with full path
python -m task_05
```

### Issue: Virtual environment not activated

**Windows Solution:**
```bash
.venv\Scripts\activate
```

**macOS/Linux Solution:**
```bash
source .venv/bin/activate
```

### Issue: Past date error loop

**Expected behavior:**
```
Enter deadline: 2025-11-15  # Past date
Error: Deadline is in the past. Please enter a future date.
Enter deadline: 2025-12-15  # Future date - Accepted!
```

### Issue: Task not found when editing/deleting

**Solution:**
1. View all tasks first (Menu Option 2) to get exact ID
2. Copy the full ID or beginning portion
3. Paste when prompted

### Issue: No tags showing in search

**Solution:**
- Make sure you created tasks with tags
- Use exact tag names (case-insensitive)
- Use "View all tasks" to verify tags

### Issue: Tests not running

**Solution:**
```bash
# Install pytest if not installed
pip install pytest

# Run tests with verbose output
pytest src/task_05/test_task_manager.py -v

# Run specific test
pytest src/task_05/test_task_manager.py::TestTask::test_task_creation_valid -v
```

---

## Performance Tips

1. **Fast Task Creation**: Have info ready before starting
2. **Efficient Searching**: Use more specific tags/names
3. **Batch Operations**: Edit/sort multiple tasks before navigating
4. **Large Collections**: Sort is very fast even with 1000+ tasks

---

## Data Persistence Note

**Current Implementation:**
- Tasks stored in memory during session
- Data lost when application closes

**Future Enhancement:**
- Could add JSON/SQLite persistence
- Auto-save feature
- Data export/import

---

## Quick Reference

| Operation | Menu # | Time | Notes |
|-----------|--------|------|-------|
| Create task | 1 | ~30s | All fields required |
| View all | 2 | <1s | Shows all tasks |
| Search | 3 | <1s | 4 search types |
| Sort | 4 | <1s | 3 sort options |
| Edit | 5 | ~20s | Modify existing |
| Delete | 6 | ~10s | Needs confirmation |
| Exit | 7 | <1s | Closes app |

---

## Success Indicators

✅ You're using it successfully when:
- Tasks are created with all attributes
- Searches return accurate results
- Sorting reorganizes tasks correctly
- Editing updates task details
- Deleting removes tasks
- Past dates are rejected with re-prompt
- No errors appear in normal usage

---

**Need Help?** Refer to README.md or check test_task_manager.py for implementation examples.
