## 2024-03-24 - Async File Streaming
**Learning:** Loading entire files into memory with `await file.read()` in FastAPI/Starlette is a major memory bottleneck for large file uploads. `aiofiles` allows non-blocking streaming to disk.
**Action:** Always implement chunked streaming for file uploads using `aiofiles` or equivalent async I/O patterns to keep memory footprint low.
