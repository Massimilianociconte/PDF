
import os
import shutil
import tempfile
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings
from app.api.auth import get_current_user

# Mock authentication
def mock_get_current_user():
    return {"username": "admin", "role": "admin"}

app.dependency_overrides[get_current_user] = mock_get_current_user

@pytest.fixture(scope="session", autouse=True)
def setup_upload_dir():
    os.makedirs(settings.upload_dir, exist_ok=True)
    yield

@pytest_asyncio.fixture(scope="function")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.fixture(scope="function")
def test_file():
    # Create a temporary PDF file
    fd, path = tempfile.mkstemp(suffix=".pdf")
    with os.fdopen(fd, 'wb') as f:
        f.write(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 100 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000117 00000 n\n0000000224 00000 n\n0000000311 00000 n\ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n406\n%%EOF")

    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture(scope="function")
def test_image():
    # Create a temporary Image file
    fd, path = tempfile.mkstemp(suffix=".png")
    # Minimal PNG
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    with os.fdopen(fd, 'wb') as f:
        f.write(data)

    yield path
    if os.path.exists(path):
        os.remove(path)
