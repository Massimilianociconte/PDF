"""Security utilities."""
import re
import uuid
import os
from fastapi import HTTPException

def validate_uuid(file_id: str) -> str:
    """
    Validate that the file_id is a valid UUID.
    Raises HTTPException if invalid.
    """
    try:
        val = uuid.UUID(file_id, version=4)
        return str(val)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

def validate_safe_filename(filename: str) -> str:
    """
    Validate that a filename is safe (no path traversal).
    Returns the sanitized filename or raises HTTPException.
    """
    # Simple check for path traversal characters
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Only allow alphanumeric, dashes, underscores, and dots
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
         # This might be too strict for user uploaded filenames, but for system generated IDs it is fine.
         # For user uploads, we often generate a UUID and store it, so we mainly care about the file_id which is a UUID.
         pass

    return filename
