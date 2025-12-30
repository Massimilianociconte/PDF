## 2024-05-24 - Enforcing Bcrypt Password Hashing
**Vulnerability:** The authentication system fell back to plaintext password comparison if the password hash check failed. This allowed administrators to configure plaintext passwords, and also potentially allowed login if the password hash itself was leaked and used as the password input.
**Learning:** Supporting backward compatibility for security features (like plaintext passwords) often undermines the security of the entire system. `if password == settings.admin_password` is dangerous even if `settings.admin_password` is intended to be a hash.
**Prevention:** Strictly enforce hashing. Ensure default configurations use valid hashes, not plaintext placeholders. Remove all code paths that perform direct string comparison for credentials.
