## 2024-02-14 - Blocking CPU Operations in Async Endpoints
**Learning:** Defining CPU-bound endpoints (like PDF manipulation) as `async def` in FastAPI runs them in the main event loop, blocking all other requests.
**Action:** Define CPU-bound endpoints as `def` (sync) to let FastAPI run them in a threadpool. If the endpoint also needs async I/O (like `await file.read()`), keep it `async def` but wrap the blocking CPU call in `fastapi.concurrency.run_in_threadpool`.

## 2024-02-14 - Inefficient String Concatenation
**Learning:** Using `text += page.get_text()` inside a loop is O(N^2) because strings are immutable in Python.
**Action:** Use list accumulation `parts.append(text)` and then `"".join(parts)` for O(N) complexity.
