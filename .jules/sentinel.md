## 2025-12-19 - [Input Validation]
**Vulnerability:** Missing input validation for file_id (path traversal risk)
**Learning:** Even with UUIDs, explicit validation is needed to prevent malformed inputs.
**Prevention:** Added `validate_uuid` helper and applied it to all endpoints accepting file_id.
