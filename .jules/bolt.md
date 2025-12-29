## 2024-05-23 - Streaming File Uploads in FastAPI
**Learning:** Reading entire file contents into memory with `await file.read()` in FastAPI endpoints is a major scalability bottleneck and OOM risk.
**Action:** Always use `aiofiles` to stream file uploads to disk in chunks (e.g., 1MB) using `async with aiofiles.open(...)` and `await file.read(chunk_size)`.
