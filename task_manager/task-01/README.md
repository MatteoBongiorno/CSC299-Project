# Task Manager CLI

A simple command-line task management application that stores tasks in a JSON file. This tool allows you to add, list, search, complete, and delete tasks directly from your terminal.

## Features

- **Add tasks** with customizable priority levels (low, medium, high)
- **List tasks** with filtering options (pending or all tasks)
- **Search tasks** by keyword
- **Complete tasks** to mark them as done
- **Delete tasks** to remove them permanently
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
python task_manager.py
```

### Available Commands

#### Add a Task
```bash
add <description> [priority]
```
**Examples:**
- `add "Buy groceries"`
- `add "Finish project report" high`
- `add "Call dentist" low`

#### List Tasks
```bash
list          # Show pending tasks only
list all      # Show all tasks including completed
```

#### Search Tasks
```bash
search <keyword>
```
**Example:**
- `search groceries`

#### Complete a Task
```bash
complete <id>
```
**Example:**
- `complete 1`

#### Delete a Task
```bash
delete <id>
```
**Example:**
- `delete 2`

#### Help
```bash
help          # Display all available commands
```

#### Exit
```bash
exit          # Exit the application
```

## Data Storage

Tasks are automatically saved to `tasks.json` in the same directory as the script. The JSON file is created automatically on first use.

### Task Structure

Each task contains:
- **id**: Unique identifier
- **description**: Task description
- **priority**: Priority level (low/medium/high)
- **created_at**: Timestamp when task was created
- **completed**: Boolean status (true/false)

## Project Structure

```
task-manager/
├── task_manager.py    # Main application file
├── tasks.json         # Auto-generated task storage
└── README.md          # This file
```
