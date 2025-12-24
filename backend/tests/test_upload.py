
import os
import pytest
from app.config import settings

@pytest.mark.asyncio
async def test_upload_pdf(client, test_file):
    with open(test_file, 'rb') as f:
        # httpx needs read() to yield bytes, standard file object works
        files = {'file': ('test.pdf', f, 'application/pdf')}
        response = await client.post("/api/pdf/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert data["filename"] == "test.pdf"

    # Verify file exists on disk
    file_path = os.path.join(settings.upload_dir, f"{data['file_id']}.pdf")
    assert os.path.exists(file_path)

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)

@pytest.mark.asyncio
async def test_image_to_pdf_upload(client, test_image):
    with open(test_image, 'rb') as f:
        files = {'file': ('test.png', f, 'image/png')}
        response = await client.post("/api/convert/image-to-pdf", files=files)

    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data

    # Verify file exists on disk
    file_path = os.path.join(settings.upload_dir, f"{data['file_id']}.pdf")
    assert os.path.exists(file_path)

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
