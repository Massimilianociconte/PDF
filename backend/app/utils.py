"""Utility functions for security and validation."""
import re
import uuid
import os
from fastapi import HTTPException, status

def validate_uuid(value: str) -> str:
    """
    Validate that the string is a valid UUID.
    Returns the UUID string if valid, raises HTTPException if invalid.
    """
    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj)
    except (ValueError, TypeError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ID format: {value}"
        )

def validate_safe_filename(filename: str) -> str:
    """
    Validate that a filename is safe (no path traversal, valid characters).
    Returns the sanitized filename.
    """
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename cannot be empty"
        )

    # Remove path traversal characters
    filename = os.path.basename(filename)

    # Allow alphanumeric, underscores, hyphens, and dots
    if not re.match(r'^[a-zA-Z0-9_.-]+$', filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename contains invalid characters"
        )

    return filename
