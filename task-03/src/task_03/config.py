"""
Configuration settings for the Task Manager CLI application
"""

class Config:
    """Configuration class containing application settings"""
    
    # File settings
    DEFAULT_FILENAME = 'tasks.json'
    JSON_INDENT = 2
    
    # Priority levels
    PRIORITY_LEVELS = ['low', 'medium', 'high']
    DEFAULT_PRIORITY = 'medium'
    
    # Display settings
    TABLE_WIDTH = 60
    DESCRIPTION_MAX_LENGTH = 30
    DETAIL_WIDTH = 70
    
    # Column widths for task listing
    COLUMN_WIDTHS = {
        'id': 5,
        'description': 30,
        'priority': 10,
        'status': 10
    }
    
    # Status symbols
    STATUS_COMPLETED = "✓ Done"
    STATUS_PENDING = "Pending"
    SYMBOL_SUCCESS = "✓"
    SYMBOL_TAG = "#"
    
    # Date format
    DATE_FORMAT = "%Y-%m-%d"
    
    # Tag settings
    TAG_PREFIX = "#"
    MAX_TAGS_DISPLAY = 5
    
    # Application info
    APP_NAME = "Task Manager CLI"
    APP_VERSION = "2.0.0"