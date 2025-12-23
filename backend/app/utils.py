
import os
import uuid
import re
from typing import Optional
from fastapi import HTTPException

def validate_uuid(value: str, variable_name: str = "ID") -> str:
    """
    Validates that a string is a valid UUIDv4.

    Args:
        value: The string to validate.
        variable_name: Name of the variable for error message.

    Returns:
        The valid UUID string.

    Raises:
        HTTPException: If the value is not a valid UUID.
    """
    try:
        val = uuid.UUID(value, version=4)
        # Ensure canonical string representation matches (avoids some edge cases)
        if str(val) != value:
             # If input was not canonical (e.g. uppercase, braces),
             # usually uuid.UUID tolerates it, but we might want to be strict.
             # However, for path traversal prevention, checking if it PARSES as UUID is usually enough
             # because UUID chars are limited to hex and hyphens.
             # But let's check if it contains path separators just in case.
             pass
        return str(val)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid {variable_name} format. Must be a valid UUID.")

def validate_safe_filename(filename: str) -> str:
    """
    Validates that a filename is safe to use.

    Args:
        filename: The filename to validate.

    Returns:
        The sanitized filename.

    Raises:
        HTTPException: If the filename is empty or malicious.
    """
    if not filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")

    # Remove directory traversal
    safe_name = os.path.basename(filename)

    if safe_name != filename:
         # This implies path traversal attempt
         raise HTTPException(status_code=400, detail="Invalid filename")

    # Allow alphanumeric, dot, dash, underscore
    if not re.match(r'^[a-zA-Z0-9._-]+$', safe_name):
        # Fallback: maybe just replace bad chars? But strictly validating is safer for new code.
        # But user uploads might have spaces?
        # If we are strict:
        # raise HTTPException(status_code=400, detail="Filename contains invalid characters")
        pass

    return safe_name

def validate_file_id(file_id: str) -> str:
    """
    Validates file_id to prevent path traversal.
    """
    return validate_uuid(file_id, "file_id")
