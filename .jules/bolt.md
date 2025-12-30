## 2024-05-23 - Async File Streaming
**Learning:** Handling large file uploads in FastAPI with `await file.read()` is memory-intensive and blocking. Using `aiofiles` with chunked reads allows for streaming uploads, keeping memory usage constant regardless of file size.
**Action:** Always prefer `async with aiofiles.open()` and chunked `file.read(size)` for handling file uploads in FastAPI to prevent memory exhaustion and blocking the event loop.
