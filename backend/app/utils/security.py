"""Security utilities."""
import re
import uuid
from typing import Optional

from fastapi import HTTPException


def validate_uuid(value: str) -> str:
    """
    Validate that the string is a valid UUID.
    Returns the value if valid, otherwise raises HTTPException.
    """
    try:
        uuid.UUID(value)
        return value
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")


def validate_safe_filename(filename: str) -> str:
    """
    Validate that the filename is safe.
    Returns the filename if valid, otherwise raises HTTPException.
    """
    # Check for path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Check for null bytes
    if "\0" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    return filename
