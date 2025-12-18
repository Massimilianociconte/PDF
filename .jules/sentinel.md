## 2024-05-23 - Path Traversal in File Download
**Vulnerability:** Found a Path Traversal vulnerability where users could supply '..' in 'output_id' or filenames to access arbitrary files on the system via the download endpoints.
**Learning:** Even when using 'os.path.join', if the input components contain '..', it can resolve to parent directories. Always validate that identifiers are UUIDs or safe alphanumeric strings.
**Prevention:** Implemented strict UUID validation for IDs and strict alphanumeric + safe char validation for filenames in all file-handling endpoints.
