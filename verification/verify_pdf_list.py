from playwright.sync_api import sync_playwright

def verify_pdf_list_accessibility():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        # Mock API responses
        page.route("**/api/auth/token", lambda route: route.fulfill(
            status=200,
            body='{"access_token": "mock-token", "token_type": "bearer"}',
            headers={"content-type": "application/json"}
        ))

        page.route("**/api/auth/me", lambda route: route.fulfill(
            status=200,
            body='{"username": "admin", "id": 1}',
            headers={"content-type": "application/json"}
        ))

        # NOTE: DashboardPage fetches files differently?
        # It calls `useAuth` which likely sets the user.
        # But `DashboardPage` has `const [files, setFiles] = useState([])`.
        # It does NOT fetch files on mount! It expects files to be added via upload.
        # WAIT! If the file list is empty initially, "Uploaded Files" text won't show.
        # PDFList says: if (files.length === 0) return "No files uploaded yet".

        # So I need to mock an upload OR set the state somehow.
        # Or, I can check if PDFList is populated from an API.
        # Looking at DashboardPage, `files` state is local and starts empty.
        # It seems `files` are not persisted across reloads in this version of the app?
        # Or maybe I missed a `useEffect` in DashboardPage.

        # Let's check DashboardPage content again in the thought process.
        # Yes: `const [files, setFiles] = useState([])`. No `useEffect` to fetch files.
        # So the list is indeed empty on load.

        # To verify the list item accessibility, I need to simulate a file being there.
        # Since I cannot easily inject state into React from Playwright without devtools,
        # I should simulate an upload.

        # Mock the upload endpoint
        page.route("**/api/pdf/upload", lambda route: route.fulfill(
            status=200,
            body='{"file_id": "123", "filename": "test.pdf", "originalName": "Test Document.pdf", "size": 10240, "pages": 5}',
            headers={"content-type": "application/json"}
        ))

        page.goto("http://localhost:3000/login")
        page.get_by_placeholder("Enter username").fill("admin")
        page.get_by_placeholder("Enter password").fill("changeme123")
        page.get_by_role("button", name="Sign In").click()
        page.wait_for_url("**/")

        # Now on dashboard.
        # I need to "upload" a file to populate the list.
        # I can use setInputFiles on the file input.

        # Create a dummy PDF file in memory is hard, but I can point to a real one.
        # Or I can just trigger the dropzone.

        # Let's create a dummy file
        with open("dummy.pdf", "wb") as f:
            f.write(b"%PDF-1.4 empty pdf")

        # Upload the file
        # The dropzone input is usually hidden but we can find it.
        # FileUploader has <input {...getInputProps()} />

        page.set_input_files('input[type="file"]', "dummy.pdf")

        # Wait for "Uploaded Files" to appear
        page.wait_for_selector("text=Uploaded Files")

        # Now I can verify the list item
        page.get_by_label("Select dummy.pdf").focus()
        page.screenshot(path="verification/focus_select.png")

        browser.close()

if __name__ == "__main__":
    verify_pdf_list_accessibility()
