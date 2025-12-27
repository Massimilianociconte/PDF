## 2024-02-14 - Plaintext Password Storage
**Vulnerability:** The application was comparing the administrative password in plaintext against the configured value. It also allowed the configured value to be a plaintext password, which encourages insecure storage of credentials.
**Learning:** Even if the code supports hashing, if it *also* supports plaintext fallback or doesn't enforce hashing for the stored credential, it is insecure. Developers might take the path of least resistance (plaintext) if allowed.
**Prevention:** Strictly enforce password hashing for stored credentials. Do not allow plaintext comparison. Fail securely if the stored credential is not a valid hash. Provide clear defaults that are hashed.
