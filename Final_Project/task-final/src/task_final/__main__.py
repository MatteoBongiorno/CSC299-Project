#!/usr/bin/env python3
"""
Entry point for the Task Manager CLI application.
"""
import sys
from pathlib import Path

# Add src directory to path so imports work
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from task_05 import main

if __name__ == "__main__":
    main()
