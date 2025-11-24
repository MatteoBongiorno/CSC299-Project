#!/usr/bin/env python3
"""
Simple launcher for Task Manager - Run from project root
"""
import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from task_05 import main

if __name__ == "__main__":
    main()
