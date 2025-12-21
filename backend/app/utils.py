import uuid
import re
import os
from fastapi import HTTPException

def validate_uuid(value: str) -> str:
    """
    Validates that the input string is a valid UUID.
    Returns the string if valid, raises HTTPException(400) otherwise.
    """
    try:
        uuid_obj = uuid.UUID(value)
        # Verify strict format to prevent any bypasses
        if str(uuid_obj) != value:
            # Enforce strict canonical format
            raise HTTPException(status_code=400, detail="Invalid file ID format")
        return str(uuid_obj)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

def validate_safe_filename(filename: str) -> str:
    """
    Validates that the filename is safe and does not contain path traversal characters.
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")

    # Check for null bytes
    if '\0' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Check for path traversal attempts
    if '..' in filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Optional: Allow only specific characters (alphanumeric, dot, underscore, dash)
    if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
         raise HTTPException(status_code=400, detail="Invalid filename characters")

    return filename
