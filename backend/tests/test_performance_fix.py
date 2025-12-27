
import pytest
import os
import fitz
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
import httpx

# Fix scope mismatch by making client and auth_token function scoped (default)

@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

# Helper to create a dummy PDF
def create_dummy_pdf(filename="test.pdf"):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Test PDF Content")
    path = os.path.join(settings.upload_dir, filename)
    doc.save(path)
    doc.close()
    return path

@pytest.fixture
async def auth_token(client):
    # Login as admin
    response = await client.post("/api/auth/token", data={
        "username": settings.admin_username,
        "password": settings.admin_password
    })
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.mark.anyio
async def test_blocking_endpoints(client, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    # Create dummy PDF
    filename = "test_blocking.pdf"
    path = create_dummy_pdf(filename)
    file_id = filename.replace(".pdf", "")

    try:
        # Check info (was async)
        response = await client.get(f"/api/pdf/info/{file_id}", headers=headers)
        assert response.status_code == 200

        # Check text extraction (was async, CPU bound)
        response = await client.get(f"/api/pdf/text/{file_id}", headers=headers)
        assert response.status_code == 200
        assert "Test PDF Content" in response.json()["text"]
    finally:
        # Clean up
        if os.path.exists(path):
            os.remove(path)
