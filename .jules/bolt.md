## 2024-05-23 - [Stream File Uploads]
**Learning:** Reading entire file uploads into memory (`await file.read()`) in FastAPI is a significant bottleneck for large files and can lead to OOM errors. `UploadFile` is spooled, but calling `read()` without arguments loads it all.
**Action:** Use `aiofiles` to stream the file content from `UploadFile` to the destination on disk in chunks (e.g., 1MB) to keep memory usage constant regardless of file size.
