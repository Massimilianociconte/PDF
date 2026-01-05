
import os
import re
import time
from playwright.sync_api import Page, expect, sync_playwright

def test_file_uploader_ux(page: Page):
    # Navigate to the dashboard (assuming local dev server)
    page.goto("http://localhost:3000/")

    # Mocking /api/auth/me to return a valid user
    page.route("**/api/auth/me", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='{"id": 1, "email": "test@example.com", "full_name": "Test User"}'
    ))

    # Mocking /api/files to return empty list (Dashboard fetches files)
    page.route("**/api/files", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body='[]'
    ))

    # Set a fake token in localStorage to bypass the client-side check
    page.add_init_script("""
        localStorage.setItem('token', 'fake-token');
    """)

    # Reload to apply token
    page.goto("http://localhost:3000/dashboard")

    # Verify we are on dashboard
    # The header has "PDF Manipulator"
    expect(page.get_by_text("PDF Manipulator")).to_be_visible()

    # Locate the FileUploader area
    # It has text "Upload PDF"
    expect(page.get_by_role("heading", name="Upload PDF")).to_be_visible()

    # Mock the upload endpoint to delay so we can see the progress bar
    def handle_upload(route):
        time.sleep(2)
        route.fulfill(
            status=200,
            body='{"id": "new-file", "filename": "test.pdf", "original_name": "test.pdf", "size": 1024}',
            headers={"Content-Type": "application/json"}
        )

    page.route("**/api/pdf/upload", handle_upload)

    # Create a dummy PDF file
    if not os.path.exists("test.pdf"):
        with open("test.pdf", "wb") as f:
            f.write(b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Resources <<\n/Font <<\n/F1 4 0 R\n>>\n>>\n/Contents 5 0 R\n>>\nendobj\n4 0 obj\n<<\n/Type /Font\n/Subtype /Type1\n/BaseFont /Helvetica\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello World) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f\n0000000010 00000 n\n0000000060 00000 n\n0000000157 00000 n\n0000000307 00000 n\n0000000395 00000 n\ntrailer\n<<\n/Size 6\n/Root 1 0 R\n>>\nstartxref\n490\n%%EOF")

    # Upload the file
    with page.expect_file_chooser() as fc_info:
        page.get_by_text("Drag & drop a PDF file here").click()
    file_chooser = fc_info.value
    file_chooser.set_files("test.pdf")

    # Check for progress bar
    expect(page.get_by_role("progressbar")).to_be_visible()

    # Take screenshot of the progress state
    page.screenshot(path="verification/verification.png")

    # Wait for completion to ensure no errors
    expect(page.get_by_text("Upload successful!")).to_be_visible(timeout=5000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_file_uploader_ux(page)
            print("Verification script finished successfully.")
        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="verification/error.png")
            raise
        finally:
            browser.close()
