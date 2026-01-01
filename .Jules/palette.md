# Palette's Journal - Critical UX/A11y Learnings

## 2024-05-22 - Nested Interactive Elements in Lists
**Learning:** Placing delete/action buttons inside a clickable list item card creates "nesting interactive controls" accessibility violations and event bubbling issues.
**Action:** Use a flat structure where the main content is one button and actions are sibling buttons, styled to look like a cohesive unit, rather than nesting them.

## 2024-05-22 - Form Label Associations
**Learning:** Many form inputs were missing explicit `htmlFor`/`id` connections or `aria-label`s, making them invisible to screen readers.
**Action:** Audit all new forms to ensure every `<input>` has a matching `<label htmlFor="...">` or `aria-label` if a visual label isn't desired.

## 2024-05-22 - Icon-Only Button Accessibility
**Learning:** Icon-only buttons (using Lucide icons) often lack accessible names, making them unusable for screen reader users.
**Action:** Always add `aria-label` and `title` attributes to icon-only buttons to provide context for both screen readers and visual tooltips.

## 2024-05-22 - Login Form Accessibility
**Learning:** The login form lacked explicit label associations and error message roles, making it difficult for assistive technology users to navigate and understand errors.
**Action:** Ensure all form fields have explicit labels and use `role="alert"` for error containers to announce validation issues immediately.
