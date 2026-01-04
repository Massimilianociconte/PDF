## 2024-05-24 - FastAPI Async vs Sync Endpoints for CPU-bound Tasks
**Learning:** In FastAPI, `async def` endpoints run in the main event loop. If they perform blocking CPU-bound operations (like PDF processing using PyMuPDF or OCR), they block the entire server, preventing it from handling other requests.
**Action:** Use `def` (instead of `async def`) for endpoints that perform blocking CPU operations but no async I/O. FastAPI will automatically run these in a threadpool, unblocking the event loop.
