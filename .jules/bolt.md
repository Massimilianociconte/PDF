# Performance Optimizations

## 2024-05-22: String Concatenation in Loops

- **Learning**: Using `+=` to concatenate strings inside a loop is inefficient (O(n^2)) because strings are immutable in Python, causing repeated copying.
- **Action**: Replaced `text += part + "\n\n"` with a list accumulation `parts.append(part); parts.append("\n\n")` and a final `"".join(parts)` (O(n)). This was applied to `PDFService.ocr_pdf` and `PDFService.extract_text`.
