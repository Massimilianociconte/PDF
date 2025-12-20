## 2024-05-24 - [CRITICAL] Path Traversal in File ID
**Vulnerability:** The application used user-supplied `file_id` strings directly in file path construction `os.path.join(settings.upload_dir, f"{file_id}.pdf")` without validation. This allowed path traversal (e.g., `file_ids=["../some_file"]`).
**Learning:** Even when appending extensions (like `.pdf`), path traversal is possible if the base variable is not validated. The assumption that `file_id` would always be a UUID because the upload endpoint generates UUIDs is dangerous; other endpoints (merge, split, etc.) accept `file_id` from user input.
**Prevention:** Always validate identifiers that are used in file path construction. Enforce strict formats (like UUID) for IDs. Use utility functions like `validate_uuid` centrally.
