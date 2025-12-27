"""Application constants and configuration."""

from pathlib import Path

# Version
APP_VERSION = "1.0.0"
DATA_VERSION = "1.0.0"

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_DATA_FILE = DATA_DIR / "tasks.json"
BACKUP_SUFFIX = ".backup"
TEMP_SUFFIX = ".tmp"

# Validation Limits
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000
MAX_TAGS_PER_TASK = 10
MAX_TAG_LENGTH = 50
MIN_SEARCH_LENGTH = 2
MIN_ID_LENGTH = 4

# Display
SHORT_ID_LENGTH = 8
TITLE_DISPLAY_LENGTH = 35
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DISPLAY_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Exit Codes
EXIT_SUCCESS = 0
EXIT_ERROR = 1

# Validation Patterns
TAG_PATTERN = r"^[a-z0-9][a-z0-9-]{0,49}$"

# Menu Options by Level
LEVEL_1_OPTIONS = {0, 1, 2, 3, 4, 5, 6}
LEVEL_2_OPTIONS = LEVEL_1_OPTIONS | {7, 8, 9, 10, 11, 12}
LEVEL_3_OPTIONS = LEVEL_2_OPTIONS | {13, 14, 15, 16, 17, 18}
