## 2025-12-20 - Dropzone Keyboard Accessibility
**Learning:** `focus-visible` ring on file dropzones is critical for keyboard users who cannot drag-and-drop, but it often requires explicit `tabIndex={0}` and role management on non-input elements.
**Action:** Always ensure dropzone containers are focusable and have visible focus indicators, not just hover states.
