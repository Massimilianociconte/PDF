## 2024-05-23 - String Concatenation in Loops
**Learning:** Python strings are immutable. Using `+=` in a loop to accumulate text (e.g., from PDF pages) creates a new string object for every iteration, resulting in O(n^2) complexity. This becomes a significant bottleneck for large documents.
**Action:** Always use list accumulation `parts.append(chunk)` followed by `"".join(parts)` for O(n) complexity when building strings in loops.
