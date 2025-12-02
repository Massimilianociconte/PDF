"""PDF processing service using PyMuPDF."""
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from typing import List, Optional, Dict


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
        text = ""
        
        if page_num is not None:
            # Extract from specific page (1-indexed)
            idx = page_num - 1
            if 0 <= idx < len(doc):
                text = doc[idx].get_text()
        else:
            # Extract from all pages
            for page in doc:
                text += page.get_text() + "\n\n"
        
        doc.close()
        return text.strip()
    
    def ocr_pdf(self, file_path: str, page_num: Optional[int] = None) -> str:
        """Perform OCR on a PDF using Tesseract."""
        doc = fitz.open(file_path)
        text = ""
        
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
            text += page_text + "\n\n"
        
        doc.close()
        return text.strip()
    
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
