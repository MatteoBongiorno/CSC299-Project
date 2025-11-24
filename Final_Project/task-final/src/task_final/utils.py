"""
Utility functions for input validation and date handling.
"""
from datetime import datetime
from typing import Optional


def validate_priority(priority: str) -> bool:
    """Check if priority is valid."""
    return priority in ["Low", "Medium", "High"]


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse a date string in YYYY-MM-DD or YYYY-MM-DD HH:MM format.

    Args:
        date_str: Date string to parse

    Returns:
        datetime object if valid, None otherwise
    """
    for fmt in ["%Y-%m-%d %H:%M", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            # If only date provided, set time to 23:59 (end of day)
            if fmt == "%Y-%m-%d":
                dt = dt.replace(hour=23, minute=59)
            return dt
        except ValueError:
            continue
    return None


def prompt_valid_deadline() -> datetime:
    """
    Prompt user for a valid future deadline. Re-prompts if date is in past.

    Returns:
        Valid datetime object for a future deadline
    """
    while True:
        date_str = input(
            "Enter deadline (YYYY-MM-DD or YYYY-MM-DD HH:MM): "
        ).strip()
        dt = parse_date(date_str)

        if dt is None:
            print("Invalid date format. Please use YYYY-MM-DD or YYYY-MM-DD HH:MM.")
            continue

        if dt < datetime.now():
            print(
                f"Deadline {dt.strftime('%Y-%m-%d %H:%M')} is in the past. "
                "Please enter a future date."
            )
            continue

        return dt


def prompt_valid_priority() -> str:
    """
    Prompt user for a valid priority level.

    Returns:
        Valid priority string (Low, Medium, High)
    """
    while True:
        priority = input("Enter priority (Low/Medium/High): ").strip()
        if validate_priority(priority):
            return priority
        print("Invalid priority. Please enter Low, Medium, or High.")


def prompt_tags() -> list:
    """
    Prompt user for task tags.

    Returns:
        List of tags (empty if user provides none)
    """
    tags_input = input(
        "Enter tags (comma-separated, or press Enter for none): "
    ).strip()
    if not tags_input:
        return []
    return [tag.strip() for tag in tags_input.split(",") if tag.strip()]
