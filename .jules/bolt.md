## 2024-03-24 - Streaming File Uploads in FastAPI
**Learning:** `UploadFile.read()` loads the entire file into memory. For large files, this can cause OOM.
**Action:** Use `aiofiles` and `await file.read(chunk_size)` loop to stream file to disk while validating size.
