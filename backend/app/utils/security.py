import re
import uuid
import os
from fastapi import HTTPException

def validate_uuid(value: str) -> str:
    """
    Validate that the string is a valid UUID.
    Returns the UUID string if valid, raises HTTPException if not.
    """
    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file ID format")

def validate_safe_filename(filename: str) -> str:
    """
    Validate that the filename is safe (alphanumeric, dots, dashes, underscores).
    Prevents path traversal and shell injection in filenames.
    """
    # Allow alphanumeric, underscore, dash, and dot
    # Reject if it contains path separators or parent directory references
    if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
        raise HTTPException(status_code=400, detail="Invalid filename format")

    if '..' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename format")

    return filename

def get_safe_path(directory: str, filename: str) -> str:
    """
    Join directory and filename, ensuring the result is within the directory.
    """
    # First validate the filename
    validate_safe_filename(filename)

    # Resolve the full path
    full_path = os.path.join(directory, filename)
    normalized_path = os.path.normpath(full_path)

    # Check that normalized path starts with the directory
    # We resolve directory too just in case
    normalized_dir = os.path.normpath(directory)

    if not normalized_path.startswith(normalized_dir):
        raise HTTPException(status_code=400, detail="Invalid path")

    return full_path
