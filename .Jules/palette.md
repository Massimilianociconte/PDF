## 2024-05-22 - Accessibility in Dynamic Components
**Learning:** Adding 'aria-live' regions to status containers is critical for providing feedback to screen reader users during asynchronous operations (like file uploads), where visual cues alone are insufficient.
**Action:** Always wrap status messages (loading, success, error) in a container with 'aria-live="polite"' and 'role="status"' or 'role="alert"'.
