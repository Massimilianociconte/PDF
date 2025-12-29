import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure backend/app can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.pdf_service import PDFService

class TestPDFService:
    @pytest.fixture
    def pdf_service(self):
        return PDFService()

    def test_extract_text_all_pages(self, pdf_service):
        with patch('fitz.open') as mock_open:
            mock_doc = MagicMock()
            # Make the doc iterable
            page1 = MagicMock()
            page1.get_text.return_value = "Page 1 Text"
            page2 = MagicMock()
            page2.get_text.return_value = "Page 2 Text"

            mock_doc.__iter__.return_value = [page1, page2]
            mock_doc.__len__.return_value = 2
            mock_open.return_value = mock_doc

            result = pdf_service.extract_text("dummy.pdf")

            # Expected: "Page 1 Text\n\nPage 2 Text\n\n".strip() -> "Page 1 Text\n\nPage 2 Text"
            expected = "Page 1 Text\n\nPage 2 Text"
            assert result == expected

    def test_ocr_pdf_all_pages(self, pdf_service):
        with patch('fitz.open') as mock_open, \
             patch('pytesseract.image_to_string') as mock_ocr, \
             patch('PIL.Image.frombytes') as mock_image:

            mock_doc = MagicMock()
            page1 = MagicMock()
            page2 = MagicMock()

            # Setup pages for OCR
            mock_doc.__len__.return_value = 2
            mock_doc.__getitem__.side_effect = [page1, page2]

            # Mock get_pixmap
            pix1 = MagicMock()
            pix1.width = 100
            pix1.height = 100
            pix1.samples = b'data'
            page1.get_pixmap.return_value = pix1

            pix2 = MagicMock()
            pix2.width = 100
            pix2.height = 100
            pix2.samples = b'data'
            page2.get_pixmap.return_value = pix2

            mock_open.return_value = mock_doc

            # Mock OCR results
            mock_ocr.side_effect = ["OCR Text 1", "OCR Text 2"]

            result = pdf_service.ocr_pdf("dummy.pdf")

            expected = "OCR Text 1\n\nOCR Text 2"
            assert result == expected
