## 2024-05-24 - Accessibility Patterns for Composite Components
**Learning:** Icon-only buttons (like those in `MergePanel.jsx` and `ConvertPanel.jsx`) are frequent accessibility offenders. Simply adding `aria-label` provides a massive usability boost for screen readers with minimal code.
**Action:** Always check `aria-label` or `aria-pressed` for icon-only toggles and buttons during reviews.
