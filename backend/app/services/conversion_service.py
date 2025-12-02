"""Conversion service for various file formats."""
import os
import fitz  # PyMuPDF
from PIL import Image
from typing import List
import img2pdf


class ConversionService:
    """Service for file format conversions."""
    
    def image_to_pdf(self, image_path: str, output_path: str) -> None:
        """Convert an image to PDF."""
        # Using img2pdf for better quality
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_path))
    
    def images_to_pdf(self, image_paths: List[str], output_path: str) -> None:
        """Convert multiple images to a single PDF."""
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))
    
    def pdf_to_images(
        self, 
        pdf_path: str, 
        output_dir: str, 
        format: str = "png",
        dpi: int = 150
    ) -> List[str]:
        """Convert PDF pages to images."""
        doc = fitz.open(pdf_path)
        image_paths = []
        
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=dpi)
            
            output_filename = f"page_{i + 1}.{format}"
            output_path = os.path.join(output_dir, output_filename)
            
            if format in ["jpg", "jpeg"]:
                # Convert to PIL Image for JPEG
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.save(output_path, "JPEG", quality=90)
            else:
                pix.save(output_path)
            
            image_paths.append(output_filename)
        
        doc.close()
        return image_paths
    
    def text_to_pdf(self, text: str, output_path: str, font_size: int = 12) -> None:
        """Convert plain text to PDF."""
        doc = fitz.open()
        
        # A4 page size
        page_width = 595
        page_height = 842
        margin = 50
        line_height = font_size * 1.5
        
        lines = text.split('\n')
        current_y = margin
        page = doc.new_page(width=page_width, height=page_height)
        
        for line in lines:
            if current_y + line_height > page_height - margin:
                # New page
                page = doc.new_page(width=page_width, height=page_height)
                current_y = margin
            
            page.insert_text(
                (margin, current_y + font_size),
                line,
                fontsize=font_size,
                color=(0, 0, 0)
            )
            current_y += line_height
        
        doc.save(output_path)
        doc.close()
    
    def html_to_pdf(self, html: str, output_path: str) -> None:
        """Convert HTML to PDF using PyMuPDF's story feature."""
        doc = fitz.open()
        
        # Create a story from HTML
        story = fitz.Story(html=html)
        
        # A4 page dimensions
        page_width = 595
        page_height = 842
        margin = 50
        
        # Content area
        content_rect = fitz.Rect(margin, margin, page_width - margin, page_height - margin)
        
        # Place the story content
        while True:
            page = doc.new_page(width=page_width, height=page_height)
            more, _ = story.place(content_rect)
            story.draw(page)
            if not more:
                break
        
        doc.save(output_path)
        doc.close()
