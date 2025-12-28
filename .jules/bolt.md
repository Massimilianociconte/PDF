## 2024-05-21 - Async File Upload Optimization
**Learning:** Using `await file.read()` inside an async FastAPI endpoint reads the entire file into memory, which is a significant bottleneck and memory risk for large files. Writing it synchronously with `open()` blocks the event loop.
**Action:** Use `aiofiles` to stream the upload in chunks (e.g., 1MB) to keep memory usage constant and ensure the event loop remains unblocked.
