## 2024-05-24 - File List Keyboard Accessibility
**Learning:** Nested interactive elements (buttons inside clickable divs) create severe keyboard navigation traps. Refactoring the main clickable area into a semantic `<button>` while keeping actions as sibling buttons ensures full keyboard accessibility without compromising visual design.
**Action:** Always verify "clickable cards" with actions are implemented as separate, semantic interactive elements rather than nested click handlers.
