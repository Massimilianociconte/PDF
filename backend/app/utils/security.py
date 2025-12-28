"""Security utilities."""
import re
import uuid
from typing import Optional

def validate_uuid(value: str) -> bool:
    """Validate that a string is a valid UUID."""
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

def validate_safe_filename(filename: str) -> bool:
    """Validate that a filename is safe (alphanumeric, dots, dashes, underscores)."""
    # Allow alphanumeric, hyphen, underscore, dot
    # Reject if contains directory separators or is empty
    if not filename or '/' in filename or '\\' in filename:
        return False

    # Check for path traversal attempts like ..
    if '..' in filename:
        return False

    return True
