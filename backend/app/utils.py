import uuid
import re
import os
from fastapi import HTTPException

def validate_uuid(value: str) -> str:
    """
    Validates that the provided string is a valid UUID.
    Returns the string if valid, raises ValueError if not.
    """
    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj)
    except ValueError:
        raise ValueError("Invalid UUID format")

def validate_safe_filename(filename: str) -> str:
    """
    Validates that the filename is safe (no path traversal, alphanumeric or simple chars).
    Returns the cleaned filename if valid, raises ValueError if not.
    """
    # Allow alphanumeric, underscore, dash, and dot
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
        raise ValueError("Invalid filename characters")

    # Check for path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ValueError("Path traversal detected")

    return filename
