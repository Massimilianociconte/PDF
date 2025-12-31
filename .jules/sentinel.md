## 2024-05-23 - Path Traversal in File Downloads
**Vulnerability:** The `download-image` endpoint in `backend/app/api/conversion.py` constructed file paths using unsanitized user input (`output_id` and `filename`), allowing attackers to access arbitrary files on the server using `..` sequences.
**Learning:** `os.path.join` does not sanitize `..` sequences, and blindly trusting user input for file paths is dangerous. FastAPI's `TestClient` normalizes paths, masking this issue in simple integration tests.
**Prevention:** Always validate user input used in file paths. Use strict allow-lists (e.g., regex for filenames, UUID validation) or helper functions like `validate_safe_filename` to reject path separators and traversal sequences.
