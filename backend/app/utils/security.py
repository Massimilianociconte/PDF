"""Security utilities."""
import os
import re
from fastapi import HTTPException

def validate_uuid(value: str) -> str:
    """Validate that the value is a valid UUID."""
    uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    if not uuid_pattern.match(value):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return value

def validate_safe_filename(filename: str) -> str:
    """
    Validate that a filename is safe to use in paths.
    Prevents path traversal and unsafe characters.
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")

    # Check for path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Allow only alphanumeric, dots, hyphens, and underscores
    # This is restrictive but safe.
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        raise HTTPException(status_code=400, detail="Invalid characters in filename")

    return filename
