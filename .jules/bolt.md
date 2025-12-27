## 2024-05-23 - FastAPI Async Blocking
**Learning:** Defining CPU-bound endpoints (like those using `fitz`/PyMuPDF) as `async def` in FastAPI blocks the main event loop, causing the entire application to hang during processing. FastAPI only automatically offloads `def` (sync) endpoints to a thread pool.
**Action:** Define CPU-bound endpoints as `def` (sync) to leverage FastAPI's automatic thread pool, or explicitly use `run_in_threadpool` for mixed I/O and CPU tasks.
