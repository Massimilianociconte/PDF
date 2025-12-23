## 2024-05-23 - Streaming File Uploads in FastAPI
**Learning:** Loading large files entirely into memory with `await file.read()` in FastAPI endpoints can cause significant memory pressure and potential OOM errors.
**Action:** Use `aiofiles` to stream file content to disk in chunks (e.g., 1MB) to maintain constant memory usage regardless of file size.
