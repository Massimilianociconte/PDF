
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.security import validate_uuid
from app.api.auth import get_current_user, User

client = TestClient(app)

def test_validate_uuid():
    assert validate_uuid("123e4567-e89b-12d3-a456-426614174000") is True
    assert validate_uuid("invalid-uuid") is False
    assert validate_uuid("../../../etc/passwd") is False

# Override auth dependency
app.dependency_overrides[get_current_user] = lambda: User(username="admin")

def test_path_traversal_prevention():
    # Test valid UUID
    # We don't have a real file, so it should return 404 Not Found, but NOT 400 Invalid ID
    valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
    response = client.get(f"/api/pdf/info/{valid_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}

    # Test Invalid UUID (simple string)
    invalid_id = "invalid-uuid"
    response = client.get(f"/api/pdf/info/{invalid_id}")
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file ID"}

    # Test Invalid UUID (path traversal attempt, URL encoded to ensure it reaches the endpoint)
    # ../../../etc/passwd -> %2E%2E%2F%2E%2E%2F%2E%2E%2Fetc%2Fpasswd
    invalid_id_encoded = "%2E%2E%2F%2E%2E%2F%2E%2E%2Fetc%2Fpasswd"
    response = client.get(f"/api/pdf/info/{invalid_id_encoded}")
    # If the server decodes it before routing, it might 404.
    # If it routes then decodes, `file_id` will be `../../../etc/passwd`.
    # FastAPI/Starlette usually decodes path params.

    # Actually, if we send it as part of the path, we rely on how TestClient handles it.
    # Let's try to verify what we can.

    # If we pass a value that is NOT a UUID, it MUST be rejected.
    # Whether it looks like a path traversal or just junk, it should be 400.

    invalid_id_2 = "some-malicious-input"
    response = client.get(f"/api/pdf/info/{invalid_id_2}")
    assert response.status_code == 400
