## 2025-12-24 - Login Form Accessibility Gaps
**Learning:** The login form lacked basic accessibility primitives: labels weren't programmaticly associated with inputs (missing `htmlFor`/`id`), and error messages appeared without `role="alert"`, making them invisible to screen readers.
**Action:** Always add `htmlFor` matching input `id`s, and wrap dynamic error messages in a container with `role="alert"` and `aria-live="polite"`.
