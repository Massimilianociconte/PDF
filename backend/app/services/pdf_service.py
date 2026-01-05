"""PDF processing service using PyMuPDF."""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from typing import List, Optional, Dict
import io
import base64


class PDFService:
    """Service for PDF manipulation operations."""

    def get_pdf_info(self, file_path: str) -> Dict:
        """Get information about a PDF file."""
        doc = fitz.open(file_path)
        info = {
            "pages": len(doc),
            "metadata": doc.metadata,
            "is_encrypted": doc.is_encrypted,
        }
        doc.close()
        return info

    def merge_pdfs(self, input_paths: List[str], output_path: str) -> None:
        """Merge multiple PDFs into one."""
        output_doc = fitz.open()

        for path in input_paths:
            doc = fitz.open(path)
            output_doc.insert_pdf(doc)
            doc.close()

        output_doc.save(output_path)
        output_doc.close()

    def split_pdf(self, input_path: str, output_path: str, pages: List[int]) -> None:
        """Extract specific pages from a PDF."""
        doc = fitz.open(input_path)
        output_doc = fitz.open()

        for page_num in pages:
            # Convert to 0-indexed
            idx = page_num - 1
            if 0 <= idx < len(doc):
                output_doc.insert_pdf(doc, from_page=idx, to_page=idx)

        output_doc.save(output_path)
        output_doc.close()
        doc.close()

    def rotate_page(self, input_path: str, output_path: str, page_num: int, angle: int) -> None:
        """Rotate a specific page in a PDF."""
        doc = fitz.open(input_path)

        # Convert to 0-indexed
        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            page.set_rotation(page.rotation + angle)

        doc.save(output_path)
        doc.close()

    def extract_text(self, file_path: str, page_num: Optional[int] = None) -> str:
        """Extract text from a PDF."""
        doc = fitz.open(file_path)
        # OPTIMIZATION: Use list accumulation instead of string concatenation (+=)
        # to avoid O(n^2) performance cost when processing large documents.
        text_parts = []

        if page_num is not None:
            # Extract from specific page (1-indexed)
            idx = page_num - 1
            if 0 <= idx < len(doc):
                text_parts.append(doc[idx].get_text())
        else:
            # Extract from all pages
            for page in doc:
                text_parts.append(page.get_text())
                text_parts.append("\n\n")

        doc.close()
        return "".join(text_parts).strip()

    def ocr_pdf(self, file_path: str, page_num: Optional[int] = None) -> str:
        """Perform OCR on a PDF using Tesseract."""
        doc = fitz.open(file_path)
        # OPTIMIZATION: Use list accumulation instead of string concatenation
        text_parts = []

        pages_to_process = []
        if page_num is not None:
            # Process specific page (1-indexed)
            idx = page_num - 1
            if 0 <= idx < len(doc):
                pages_to_process = [idx]
        else:
            # Process all pages
            pages_to_process = range(len(doc))

        for idx in pages_to_process:
            page = doc[idx]
            # Render page to image
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Perform OCR
            page_text = pytesseract.image_to_string(img)
            text_parts.append(page_text)
            text_parts.append("\n\n")

        doc.close()
        return "".join(text_parts).strip()

    def add_image(
        self,
        input_path: str,
        output_path: str,
        image_path: str,
        page_num: int,
        x: float,
        y: float,
        width: Optional[float] = None,
        height: Optional[float] = None
    ) -> None:
        """Add an image to a specific page of a PDF."""
        doc = fitz.open(input_path)

        # Convert to 0-indexed
        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]

            # Load image
            img = fitz.open(image_path)
            rect = img[0].rect

            # Calculate dimensions
            if width and height:
                target_rect = fitz.Rect(x, y, x + width, y + height)
            elif width:
                ratio = width / rect.width
                target_rect = fitz.Rect(x, y, x + width, y + rect.height * ratio)
            elif height:
                ratio = height / rect.height
                target_rect = fitz.Rect(x, y, x + rect.width * ratio, y + height)
            else:
                target_rect = fitz.Rect(x, y, x + rect.width, y + rect.height)

            # Insert image
            page.insert_image(target_rect, filename=image_path)
            img.close()

        doc.save(output_path)
        doc.close()

    def add_text(
        self,
        input_path: str,
        output_path: str,
        page_num: int,
        text: str,
        x: float,
        y: float,
        font_size: int = 12,
        color: tuple = (0, 0, 0)
    ) -> None:
        """Add text to a specific page of a PDF."""
        doc = fitz.open(input_path)

        # Convert to 0-indexed
        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            page.insert_text(
                (x, y),
                text,
                fontsize=font_size,
                color=color
            )

        doc.save(output_path)
        doc.close()

    def get_page_preview(self, file_path: str, output_path: str, page_num: int, dpi: int = 150) -> None:
        """Generate a preview image of a PDF page."""
        doc = fitz.open(file_path)

        # Convert to 0-indexed
        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            pix = page.get_pixmap(dpi=dpi)
            pix.save(output_path)

        doc.close()

    def compress_pdf(self, input_path: str, output_path: str) -> None:
        """Compress a PDF file."""
        doc = fitz.open(input_path)
        doc.save(output_path, garbage=4, deflate=True, clean=True)
        doc.close()

    def add_watermark(
        self,
        input_path: str,
        output_path: str,
        watermark_text: str,
        opacity: float = 0.3,
        angle: int = 45
    ) -> None:
        """Add a text watermark to all pages of a PDF."""
        doc = fitz.open(input_path)

        for page in doc:
            rect = page.rect
            # Calculate center position
            x = rect.width / 2
            y = rect.height / 2

            # Add watermark
            page.insert_text(
                (x - 100, y),
                watermark_text,
                fontsize=50,
                color=(0.5, 0.5, 0.5),
                rotate=angle,
                overlay=True
            )

        doc.save(output_path)
        doc.close()

    def delete_pages(self, input_path: str, output_path: str, pages: List[int]) -> None:
        """Delete specific pages from a PDF."""
        doc = fitz.open(input_path)

        # Convert to 0-indexed and sort in reverse to maintain indices
        indices = sorted([p - 1 for p in pages if 0 < p <= len(doc)], reverse=True)

        for idx in indices:
            doc.delete_page(idx)

        doc.save(output_path)
        doc.close()

    def reorder_pages(self, input_path: str, output_path: str, new_order: List[int]) -> None:
        """Reorder pages in a PDF."""
        doc = fitz.open(input_path)
        output_doc = fitz.open()

        for page_num in new_order:
            idx = page_num - 1
            if 0 <= idx < len(doc):
                output_doc.insert_pdf(doc, from_page=idx, to_page=idx)

        output_doc.save(output_path)
        output_doc.close()
        doc.close()

    def encrypt_pdf(
        self,
        input_path: str,
        output_path: str,
        user_password: str,
        owner_password: str = None,
        permissions: int = None
    ) -> None:
        """Encrypt a PDF with password protection."""
        doc = fitz.open(input_path)

        # Default permissions: allow printing, copying, modifying
        if permissions is None:
            permissions = (
                fitz.PDF_PERM_PRINT |
                fitz.PDF_PERM_COPY |
                fitz.PDF_PERM_MODIFY |
                fitz.PDF_PERM_ANNOTATE
            )

        owner_pwd = owner_password or user_password

        doc.save(
            output_path,
            encryption=fitz.PDF_ENCRYPT_AES_256,
            user_pw=user_password,
            owner_pw=owner_pwd,
            permissions=permissions
        )
        doc.close()

    def decrypt_pdf(self, input_path: str, output_path: str, password: str) -> bool:
        """Decrypt a PDF file."""
        doc = fitz.open(input_path)

        if doc.is_encrypted:
            if not doc.authenticate(password):
                doc.close()
                return False

        # Save without encryption
        doc.save(output_path)
        doc.close()
        return True

    def add_text_annotation(
        self,
        input_path: str,
        output_path: str,
        page_num: int,
        text: str,
        x: float,
        y: float,
        font_size: int = 12,
        font_color: tuple = (0, 0, 0),
        font_name: str = "helv"
    ) -> None:
        """Add text annotation to a specific page."""
        doc = fitz.open(input_path)

        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            page.insert_text(
                (x, y),
                text,
                fontsize=font_size,
                fontname=font_name,
                color=font_color
            )

        doc.save(output_path)
        doc.close()

    def add_highlight(
        self,
        input_path: str,
        output_path: str,
        page_num: int,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        color: tuple = (1, 1, 0)  # Yellow
    ) -> None:
        """Add highlight annotation to a specific area."""
        doc = fitz.open(input_path)

        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            rect = fitz.Rect(x0, y0, x1, y1)
            annot = page.add_highlight_annot(rect)
            annot.set_colors(stroke=color)
            annot.update()

        doc.save(output_path)
        doc.close()

    def redact_area(
        self,
        input_path: str,
        output_path: str,
        page_num: int,
        x0: float,
        y0: float,
        x1: float,
        y1: float,
        fill_color: tuple = (0, 0, 0)  # Black
    ) -> None:
        """Redact (black out) a specific area of a page."""
        doc = fitz.open(input_path)

        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            rect = fitz.Rect(x0, y0, x1, y1)
            page.add_redact_annot(rect, fill=fill_color)
            page.apply_redactions()

        doc.save(output_path)
        doc.close()

    def add_page_numbers(
        self,
        input_path: str,
        output_path: str,
        position: str = "bottom",  # top, bottom
        alignment: str = "center",  # left, center, right
        start_num: int = 1,
        font_size: int = 10
    ) -> None:
        """Add page numbers to all pages."""
        doc = fitz.open(input_path)

        for i, page in enumerate(doc):
            rect = page.rect
            page_num = i + start_num
            text = str(page_num)

            # Calculate position
            if position == "bottom":
                y = rect.height - 30
            else:
                y = 30

            if alignment == "left":
                x = 50
            elif alignment == "right":
                x = rect.width - 50
            else:
                x = rect.width / 2

            page.insert_text(
                (x, y),
                text,
                fontsize=font_size,
                color=(0, 0, 0)
            )

        doc.save(output_path)
        doc.close()

    def add_header_footer(
        self,
        input_path: str,
        output_path: str,
        header_text: str = None,
        footer_text: str = None,
        font_size: int = 10
    ) -> None:
        """Add header and/or footer to all pages."""
        doc = fitz.open(input_path)

        for page in doc:
            rect = page.rect

            if header_text:
                page.insert_text(
                    (rect.width / 2 - len(header_text) * 3, 25),
                    header_text,
                    fontsize=font_size,
                    color=(0, 0, 0)
                )

            if footer_text:
                page.insert_text(
                    (rect.width / 2 - len(footer_text) * 3, rect.height - 25),
                    footer_text,
                    fontsize=font_size,
                    color=(0, 0, 0)
                )

        doc.save(output_path)
        doc.close()

    def update_metadata(
        self,
        input_path: str,
        output_path: str,
        title: str = None,
        author: str = None,
        subject: str = None,
        keywords: str = None,
        creator: str = None
    ) -> None:
        """Update PDF metadata."""
        doc = fitz.open(input_path)

        metadata = doc.metadata

        if title is not None:
            metadata["title"] = title
        if author is not None:
            metadata["author"] = author
        if subject is not None:
            metadata["subject"] = subject
        if keywords is not None:
            metadata["keywords"] = keywords
        if creator is not None:
            metadata["creator"] = creator

        doc.set_metadata(metadata)
        doc.save(output_path)
        doc.close()

    def get_metadata(self, file_path: str) -> Dict:
        """Get PDF metadata."""
        doc = fitz.open(file_path)
        metadata = doc.metadata.copy()
        doc.close()
        return metadata

    def extract_images(self, file_path: str, output_dir: str) -> List[str]:
        """Extract all images from a PDF."""
        import os
        doc = fitz.open(file_path)
        image_list = []

        for page_num in range(len(doc)):
            page = doc[page_num]
            images = page.get_images()

            for img_idx, img in enumerate(images):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)

                if pix.n - pix.alpha > 3:  # CMYK
                    pix = fitz.Pixmap(fitz.csRGB, pix)

                filename = f"page{page_num + 1}_img{img_idx + 1}.png"
                filepath = os.path.join(output_dir, filename)
                pix.save(filepath)
                image_list.append(filename)
                pix = None

        doc.close()
        return image_list

    def create_blank_pdf(
        self,
        output_path: str,
        num_pages: int = 1,
        width: float = 595,  # A4 width
        height: float = 842  # A4 height
    ) -> None:
        """Create a blank PDF with specified number of pages."""
        doc = fitz.open()

        for _ in range(num_pages):
            doc.new_page(width=width, height=height)

        doc.save(output_path)
        doc.close()

    def sign_pdf(
        self,
        input_path: str,
        output_path: str,
        signature_image_path: str,
        page_num: int,
        x: float,
        y: float,
        width: float = 100,
        height: float = 50
    ) -> None:
        """Add a signature image to a PDF."""
        doc = fitz.open(input_path)

        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            rect = fitz.Rect(x, y, x + width, y + height)
            page.insert_image(rect, filename=signature_image_path)

        doc.save(output_path)
        doc.close()

    def flatten_pdf(self, input_path: str, output_path: str) -> None:
        """Flatten all annotations and form fields in a PDF."""
        doc = fitz.open(input_path)

        for page in doc:
            # Remove all annotations by applying them
            annot = page.first_annot
            while annot:
                annot.set_flags(fitz.ANNOT_XF_Print)
                annot = annot.next

        # Save with deflate to also clean up
        doc.save(output_path, garbage=4, deflate=True)
        doc.close()

    def compare_pdfs(self, file1_path: str, file2_path: str) -> Dict:
        """Compare two PDFs and return differences."""
        doc1 = fitz.open(file1_path)
        doc2 = fitz.open(file2_path)

        result = {
            "page_count_diff": len(doc1) - len(doc2),
            "doc1_pages": len(doc1),
            "doc2_pages": len(doc2),
            "text_differences": []
        }

        # Compare text page by page
        max_pages = max(len(doc1), len(doc2))
        for i in range(max_pages):
            text1 = doc1[i].get_text() if i < len(doc1) else ""
            text2 = doc2[i].get_text() if i < len(doc2) else ""

            if text1 != text2:
                result["text_differences"].append({
                    "page": i + 1,
                    "doc1_text_length": len(text1),
                    "doc2_text_length": len(text2)
                })

        doc1.close()
        doc2.close()
        return result

    def crop_page(
        self,
        input_path: str,
        output_path: str,
        page_num: int,
        x0: float,
        y0: float,
        x1: float,
        y1: float
    ) -> None:
        """Crop a specific page to the given rectangle."""
        doc = fitz.open(input_path)

        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            page.set_cropbox(fitz.Rect(x0, y0, x1, y1))

        doc.save(output_path)
        doc.close()

    def resize_page(
        self,
        input_path: str,
        output_path: str,
        page_num: int,
        width: float,
        height: float
    ) -> None:
        """Resize a specific page."""
        doc = fitz.open(input_path)

        idx = page_num - 1
        if 0 <= idx < len(doc):
            page = doc[idx]
            # Scale the page content
            scale_x = width / page.rect.width
            scale_y = height / page.rect.height
            mat = fitz.Matrix(scale_x, scale_y)

            # Create new document with resized page
            new_doc = fitz.open()
            new_page = new_doc.new_page(width=width, height=height)
            new_page.show_pdf_page(new_page.rect, doc, idx)

            # Copy other pages
            for i in range(len(doc)):
                if i != idx:
                    new_doc.insert_pdf(doc, from_page=i, to_page=i)

            new_doc.save(output_path)
            new_doc.close()

        doc.close()
