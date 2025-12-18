import re
import uuid
from fastapi import HTTPException

def validate_uuid(value: str, name: str = "ID") -> str:
    """
    Validate that the given string is a valid UUID.
    Raises HTTPException(400) if invalid.
    """
    try:
        uuid.UUID(str(value))
        return value
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid {name} format: must be a valid UUID")

def validate_safe_filename(filename: str) -> str:
    """
    Validate that the filename is safe (no path traversal, no dangerous characters).
    Allows alphanumeric, underscores, dashes, and dots.
    Raises HTTPException(400) if invalid.
    """
    if not filename or ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename: path traversal detected")

    # strictly allow only safe characters: a-z A-Z 0-9 . - _
    # This prevents any other funny business
    if not re.match(r"^[a-zA-Z0-9\._-]+$", filename):
        raise HTTPException(status_code=400, detail="Invalid filename: contains illegal characters")

    return filename
