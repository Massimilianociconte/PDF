2024-05-23: Async OCR Blocking Fix
**Title:** Blocking CPU/IO Operation in Async OCR Endpoint
**Learning:** Calling synchronous, CPU-intensive functions (like `pytesseract.image_to_string` or `fitz` operations) directly within an `async def` endpoint blocks the FastAPI event loop, degrading performance for all concurrent users.
**Action:** Wrap such blocking calls in `fastapi.concurrency.run_in_threadpool` to offload execution to a separate thread while awaiting the result, or define the endpoint as a standard `def` (synchronous) if no other async I/O is performed.

2024-05-23: String Concatenation Optimization
**Title:** String Accumulation Anti-Pattern
**Learning:** Using `+=` to accumulate strings in a loop (e.g., aggregating OCR text page by page) has O(n^2) complexity due to repeated string copying.
**Action:** Use a list to collect string parts and join them once with `"".join()` or `"\n".join()` for O(n) complexity.
