## 2024-05-23 - Hardcoded Credentials in Config
**Vulnerability:** The application stored the default admin password (`changeme123`) in plaintext within `backend/app/config.py` and supported plaintext comparison in `backend/app/api/auth.py`.
**Learning:** Default credentials should never be stored in plaintext. Even "changeme" passwords should be hashed to enforce security best practices and prevent accidental exposure if the config is leaked.
**Prevention:** Store default credentials as hashes. Remove any code logic that performs plaintext string comparison for passwords. Use `passlib` or similar libraries to verify passwords against stored hashes.
