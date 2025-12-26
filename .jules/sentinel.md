## 2024-05-22 - Path Traversal Protection
**Vulnerability:** Path traversal vulnerability in PDF file handling endpoints where `file_id` was directly used in path construction.
**Learning:** Even when appending extensions (e.g., `.pdf`), path traversal is possible if the base filename is not validated. Users can supply `../../` sequences to traverse directories.
**Prevention:** Strictly validate file identifiers. Since this application uses UUIDs for file IDs, enforcing valid UUID format using `uuid.UUID()` is a strong defense against path traversal for these inputs.
