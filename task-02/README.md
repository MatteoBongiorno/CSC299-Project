# Task Manager CLI

A PKMS-inspired command-line task management application that stores tasks in a JSON file. This tool allows you to add, list, search, complete, and delete tasks with support for tags and detailed notes - similar to popular knowledge management systems like Notion and Obsidian.

## Features

- **Add tasks** with customizable priority levels (low, medium, high)
- **Tag support** - Organize tasks with multiple tags (e.g., #work #urgent)
- **Notes** - Add detailed notes and context to any task
- **List tasks** with filtering options (pending or all tasks)
- **Search tasks** by keyword in description or notes
- **Filter by tags** - Find all tasks with a specific tag
- **Complete tasks** to mark them as done
- **Delete tasks** to remove them permanently
- **View full details** - See complete task information including notes
- **Persistent storage** using JSON format
- **Clean command-line interface** with easy-to-use commands

## Installation

1. Clone or download this repository
2. Ensure you have Python 3.6+ installed
3. No additional dependencies required - uses only Python standard library

## Usage

### Starting the Application

Run the program from your terminal:

```bash
python cli.py
```

## Data Storage

Tasks are automatically saved to `tasks.json` in the same directory as the script. The JSON file is created automatically on first use.

### Task Structure

Each task contains:
- **id**: Unique identifier
- **description**: Task description
- **priority**: Priority level (low/medium/high)
- **tags**: List of tags (e.g., ["#work", "#urgent"])
- **notes**: Detailed notes or context
- **created_at**: Timestamp when task was created
- **completed**: Boolean status (true/false)

## PKMS Features

This task manager incorporates features inspired by popular Personal Knowledge Management Systems:

### Tags (Obsidian/Notion-style)
- Add multiple tags to tasks for flexible organization
- Filter and search by tags
- View all tags across your task system

### Notes (Notion-style)
- Add detailed context and information to any task
- Search through notes content
- View full task details with formatted notes

## Requirements

- Python 3.6 or higher
- No external libraries required

## Project Structure

```
tasks-02/
├── cli.py              # Command-line interface (main program)
├── task_manager.py     # TaskManager class (business logic)
├── utils.py            # Utility functions for formatting and validation
├── config.py           # Configuration settings
├── tasks.json          # Auto-generated task storage
└── README.md           # This file
```

### File Descriptions

- **cli.py**: The main entry point - handles user input and command processing
- **task_manager.py**: Contains the TaskManager class with methods for managing tasks
- **utils.py**: Helper functions for formatting output, parsing commands, and validation
- **config.py**: Centralized configuration for settings like file names, priority levels, and display options
- **tasks.json**: Automatically generated JSON file that stores all task data

## Version History

- **v2.0.0**: Added PKMS-inspired features (tags and notes)
- **v1.0.0**: Initial release with basic task management