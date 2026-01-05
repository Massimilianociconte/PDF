## 2024-01-05 - Critical Path Traversal in File Downloads
**Vulnerability:** Unsafe file path construction using user-controlled `output_id` and `filename` parameters in `download_converted_image` endpoint allowed arbitrary file read via directory traversal (e.g., `../`).
**Learning:** `os.path.join` does not prevent directory traversal if components contain `..`. Input validation for filesystem operations must be strict (allowlists) rather than loose (blocklists).
**Prevention:** Always validate file path parameters against a strict allowlist (e.g., UUIDs for IDs, alphanumeric for filenames) before using them in filesystem operations. Use utility functions like `validate_safe_filename` and `validate_uuid` centrally.
