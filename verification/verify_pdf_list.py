
import os
import time
from playwright.sync_api import sync_playwright, expect
import json

def verify_pdf_list_ux():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        # Mock Auth Token Check
        page.route("**/api/auth/me", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 1, "username": "admin", "is_admin": true}'
        ))

        # Mock Upload Endpoint
        page.route("**/api/pdf/upload", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "file_id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "server-filename.pdf",
                "originalName": "ignored-by-frontend.pdf",
                "size": 2621440, # 2.5 MB
                "pages": 15,
                "created_at": "2023-01-01T12:00:00Z"
            })
        ))

        # 1. Login
        page.goto("http://localhost:3000/login")
        page.evaluate("localStorage.setItem('token', 'fake-token')")
        page.goto("http://localhost:3000/")

        # 2. Upload a fake file
        with open("dummy.pdf", "wb") as f:
            f.write(b"%PDF-1.4 dummy content")

        page.set_input_files('input[type="file"]', "dummy.pdf")

        # Wait for "Upload successful!" message
        try:
            page.wait_for_selector("text=Upload successful!", timeout=10000)
        except:
             print("Upload confirmation not found. Screenshotting.")
             page.screenshot(path="verification/upload_fail.png")

        # Now the file should be in the list
        try:
            page.wait_for_selector("text=Uploaded Files", timeout=10000)
        except:
             print("Uploaded Files list not found. Screenshotting.")
             page.screenshot(path="verification/list_fail.png")
             raise

        # VERIFICATION 1: Check if the list items are accessible buttons

        # Look for the filename directly
        filename_locator = page.get_by_text("dummy.pdf")
        expect(filename_locator).to_be_visible()

        # Now check if it's inside a button
        main_button = page.locator("button").filter(has=page.get_by_text("dummy.pdf")).first

        expect(main_button).to_be_visible()

        class_attr = main_button.get_attribute("class")
        if "focus-visible:ring-2" not in class_attr:
            print("FAILURE: Main row button missing focus ring classes")
        else:
            print("SUCCESS: Main row button has focus ring classes")

        # VERIFICATION 2: Check for accessible Download and Delete buttons
        # The aria-label is constructed from originalName, which is "dummy.pdf" (from file.name)
        download_btn = page.get_by_label("Download dummy.pdf")
        expect(download_btn).to_be_visible()
        print("SUCCESS: Download button found by aria-label")

        delete_btn = page.get_by_label("Delete dummy.pdf")
        expect(delete_btn).to_be_visible()
        print("SUCCESS: Delete button found by aria-label")

        # Take screenshot
        page.screenshot(path="verification/pdf_list_accessibility.png")
        print("Screenshot saved to verification/pdf_list_accessibility.png")

        # Clean up
        if os.path.exists("dummy.pdf"):
            os.remove("dummy.pdf")

        browser.close()

if __name__ == "__main__":
    verify_pdf_list_ux()
