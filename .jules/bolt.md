## 2024-02-14 - Blocking Event Loops in FastAPI
**Learning:** `async def` endpoints in FastAPI run on the main event loop. If they perform blocking CPU-bound operations (like heavy PDF processing with `fitz`), they block the entire server, preventing it from handling other requests concurrently.
**Action:** Use `def` (instead of `async def`) for endpoints that primarily perform blocking operations and do not strictly require `await` for input/output. For endpoints that *must* be `async` (e.g., those using `await file.read()`), wrap the blocking logic in `fastapi.concurrency.run_in_threadpool`.

## 2024-02-14 - TestClient Compatibility
**Learning:** `fastapi==0.104.1` and `starlette==0.27.0` are incompatible with `httpx>=0.28.0` when using `TestClient(app)` because `httpx` removed the `app` argument in version 0.28.0.
**Action:** Pin `httpx<0.28.0` in test dependencies when working with these versions of FastAPI/Starlette.
