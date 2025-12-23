
import pytest
import os
import uuid
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.utils import validate_uuid
from fastapi import HTTPException

client = TestClient(app)

@pytest.fixture
def clean_upload_dir():
    # Setup
    if not os.path.exists(settings.upload_dir):
        os.makedirs(settings.upload_dir)
    yield
    # Teardown
    pass

def test_validate_uuid_valid():
    uid = str(uuid.uuid4())
    assert validate_uuid(uid) == uid

def test_validate_uuid_invalid():
    with pytest.raises(HTTPException) as excinfo:
        validate_uuid("invalid-uuid")
    assert excinfo.value.status_code == 400

def test_validate_uuid_path_traversal():
    with pytest.raises(HTTPException) as excinfo:
        validate_uuid("../../etc/passwd")
    assert excinfo.value.status_code == 400

def test_pdf_info_path_traversal_attempt(clean_upload_dir):
    # Attempt to access a file using path traversal in file_id
    # We expect 400 Bad Request due to invalid UUID format, NOT 404 or 500.

    # We bypass authentication for this test or need to mock it.
    # Since get_current_user depends on OAuth2, we should probably override it or obtain a token.
    # For simplicity, let's override the dependency.

    from app.api.auth import get_current_user, User

    app.dependency_overrides[get_current_user] = lambda: User(username="admin")

    response = client.get("/api/pdf/info/../../etc/passwd")

    # Check if it was blocked by UUID validation (400) or something else.
    # Since FastAPI path parameters might handle slashes differently,
    # if we use "info/{file_id}", and file_id contains slashes, it might not match the route
    # unless file_id is defined as path.
    # However, for query params or body it's easier.

    # Let's try a split request which takes file_id in body
    response = client.post("/api/pdf/split", json={
        "file_id": "../../etc/passwd",
        "pages": [1]
    })

    assert response.status_code == 400
    assert "Invalid ID format" in response.json()["detail"] or "Invalid file_id format" in response.json()["detail"]

    app.dependency_overrides = {}
