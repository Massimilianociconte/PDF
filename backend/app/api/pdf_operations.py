"""PDF operations API endpoints."""
import os
import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.api.auth import User, get_current_user
from app.config import settings
from app.services.pdf_service import PDFService

router = APIRouter()
pdf_service = PDFService()


class MergeRequest(BaseModel):
    """Request model for merging PDFs."""
    file_ids: List[str]
    output_name: str = "merged.pdf"


class SplitRequest(BaseModel):
    """Request model for splitting PDFs."""
    file_id: str
    pages: List[int]  # Pages to extract (1-indexed)


class EditTextRequest(BaseModel):
    """Request model for editing text in PDF."""
    file_id: str
    page: int
    old_text: str
    new_text: str


class DeletePagesRequest(BaseModel):
    """Request model for deleting pages."""
    file_id: str
    pages: List[int]


class ReorderPagesRequest(BaseModel):
    """Request model for reordering pages."""
    file_id: str
    new_order: List[int]


class EncryptRequest(BaseModel):
    """Request model for encrypting PDF."""
    file_id: str
    user_password: str
    owner_password: Optional[str] = None


class DecryptRequest(BaseModel):
    """Request model for decrypting PDF."""
    file_id: str
    password: str


class WatermarkRequest(BaseModel):
    """Request model for adding watermark."""
    file_id: str
    text: str
    opacity: float = 0.3
    angle: int = 45


class MetadataRequest(BaseModel):
    """Request model for updating metadata."""
    file_id: str
    title: Optional[str] = None
    author: Optional[str] = None
    subject: Optional[str] = None
    keywords: Optional[str] = None


class PageNumbersRequest(BaseModel):
    """Request model for adding page numbers."""
    file_id: str
    position: str = "bottom"  # top, bottom
    alignment: str = "center"  # left, center, right
    start_num: int = 1


class HeaderFooterRequest(BaseModel):
    """Request model for adding header/footer."""
    file_id: str
    header_text: Optional[str] = None
    footer_text: Optional[str] = None


class PDFInfo(BaseModel):
    """PDF information model."""
    file_id: str
    filename: str
    pages: int
    size: int


@router.post("/upload", response_model=PDFInfo)
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload a PDF file."""
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Generate unique file ID
    file_id = str(uuid.uuid4())
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    # Save file
    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")

    with open(file_path, "wb") as f:
        f.write(content)

    # Get PDF info
    try:
        info = await run_in_threadpool(pdf_service.get_pdf_info, file_path)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail=f"Invalid PDF file: {str(e)}")

    return PDFInfo(
        file_id=file_id,
        filename=file.filename,
        pages=info["pages"],
        size=len(content)
    )


@router.get("/info/{file_id}", response_model=PDFInfo)
def get_pdf_info(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get information about an uploaded PDF."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    info = pdf_service.get_pdf_info(file_path)

    return PDFInfo(
        file_id=file_id,
        filename=f"{file_id}.pdf",
        pages=info["pages"],
        size=os.path.getsize(file_path)
    )


@router.post("/merge")
def merge_pdfs(
    request: MergeRequest,
    current_user: User = Depends(get_current_user)
):
    """Merge multiple PDFs into one."""
    file_paths = []
    for file_id in request.file_ids:
        file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File {file_id} not found")
        file_paths.append(file_path)

    # Generate output file
    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.merge_pdfs(file_paths, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Merge failed: {str(e)}")

    return {
        "file_id": output_id,
        "filename": request.output_name,
        "message": "PDFs merged successfully"
    }


@router.post("/split")
def split_pdf(
    request: SplitRequest,
    current_user: User = Depends(get_current_user)
):
    """Split a PDF by extracting specific pages."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Generate output file
    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.split_pdf(file_path, output_path, request.pages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Split failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": f"Extracted pages {request.pages} successfully"
    }


@router.post("/rotate/{file_id}")
def rotate_pdf(
    file_id: str,
    page: int = Form(...),
    angle: int = Form(...),  # 90, 180, or 270
    current_user: User = Depends(get_current_user)
):
    """Rotate a specific page in a PDF."""
    if angle not in [90, 180, 270]:
        raise HTTPException(status_code=400, detail="Angle must be 90, 180, or 270")

    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.rotate_page(file_path, output_path, page, angle)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rotation failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": f"Page {page} rotated {angle} degrees"
    }


@router.post("/ocr/{file_id}")
def ocr_pdf(
    file_id: str,
    page: int = Form(None),  # None means all pages
    current_user: User = Depends(get_current_user)
):
    """Perform OCR on a PDF to extract text."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        text = pdf_service.ocr_pdf(file_path, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR failed: {str(e)}")

    return {"text": text}


@router.get("/text/{file_id}")
def extract_text(
    file_id: str,
    page: int = None,
    current_user: User = Depends(get_current_user)
):
    """Extract text from a PDF."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        text = pdf_service.extract_text(file_path, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {str(e)}")

    return {"text": text}


@router.post("/add-image/{file_id}")
async def add_image_to_pdf(
    file_id: str,
    image: UploadFile = File(...),
    page: int = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    width: float = Form(None),
    height: float = Form(None),
    current_user: User = Depends(get_current_user)
):
    """Add an image to a specific page of a PDF."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Save image temporarily
    image_id = str(uuid.uuid4())
    image_ext = os.path.splitext(image.filename)[1] or ".png"
    image_path = os.path.join(settings.upload_dir, f"{image_id}{image_ext}")

    content = await image.read()
    with open(image_path, "wb") as f:
        f.write(content)

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        await run_in_threadpool(
            pdf_service.add_image,
            file_path,
            output_path,
            image_path,
            page,
            x,
            y,
            width,
            height
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Add image failed: {str(e)}")
    finally:
        # Clean up temp image
        if os.path.exists(image_path):
            os.remove(image_path)

    return {
        "file_id": output_id,
        "message": "Image added successfully"
    }


@router.get("/download/{file_id}")
def download_pdf(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Download a processed PDF."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=f"{file_id}.pdf"
    )


@router.delete("/{file_id}")
def delete_pdf(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete an uploaded PDF."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)

    return {"message": "File deleted successfully"}


@router.get("/preview/{file_id}/{page}")
def get_page_preview(
    file_id: str,
    page: int,
    current_user: User = Depends(get_current_user)
):
    """Get a preview image of a specific page."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    preview_path = os.path.join(settings.upload_dir, f"{file_id}_page_{page}.png")

    try:
        pdf_service.get_page_preview(file_path, preview_path, page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview generation failed: {str(e)}")

    return FileResponse(preview_path, media_type="image/png")


# ============= ADVANCED FEATURES =============

@router.post("/compress/{file_id}")
def compress_pdf(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Compress a PDF to reduce file size."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    original_size = os.path.getsize(file_path)

    try:
        pdf_service.compress_pdf(file_path, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compression failed: {str(e)}")

    new_size = os.path.getsize(output_path)
    reduction = round((1 - new_size / original_size) * 100, 2)

    return {
        "file_id": output_id,
        "original_size": original_size,
        "compressed_size": new_size,
        "reduction_percent": reduction,
        "message": f"PDF compressed by {reduction}%"
    }


@router.post("/watermark")
def add_watermark(
    request: WatermarkRequest,
    current_user: User = Depends(get_current_user)
):
    """Add a text watermark to all pages."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.add_watermark(
            file_path, output_path, request.text, request.opacity, request.angle
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Watermark failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Watermark added successfully"
    }


@router.post("/encrypt")
def encrypt_pdf(
    request: EncryptRequest,
    current_user: User = Depends(get_current_user)
):
    """Encrypt a PDF with password protection."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.encrypt_pdf(
            file_path, output_path, request.user_password, request.owner_password
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "PDF encrypted successfully"
    }


@router.post("/decrypt")
def decrypt_pdf(
    request: DecryptRequest,
    current_user: User = Depends(get_current_user)
):
    """Decrypt a password-protected PDF."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        success = pdf_service.decrypt_pdf(file_path, output_path, request.password)
        if not success:
            raise HTTPException(status_code=400, detail="Invalid password")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "PDF decrypted successfully"
    }


@router.post("/delete-pages")
def delete_pages(
    request: DeletePagesRequest,
    current_user: User = Depends(get_current_user)
):
    """Delete specific pages from a PDF."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.delete_pages(file_path, output_path, request.pages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete pages failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": f"Deleted pages {request.pages}"
    }


@router.post("/reorder-pages")
def reorder_pages(
    request: ReorderPagesRequest,
    current_user: User = Depends(get_current_user)
):
    """Reorder pages in a PDF."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.reorder_pages(file_path, output_path, request.new_order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reorder failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Pages reordered successfully"
    }


@router.post("/add-text/{file_id}")
def add_text_annotation(
    file_id: str,
    text: str = Form(...),
    page: int = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    font_size: int = Form(default=12),
    color: str = Form(default="0,0,0"),  # RGB as comma-separated
    current_user: User = Depends(get_current_user)
):
    """Add text annotation to a page."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    # Parse color
    try:
        color_tuple = tuple(float(c) for c in color.split(","))
    except:
        color_tuple = (0, 0, 0)

    try:
        pdf_service.add_text_annotation(
            file_path, output_path, page, text, x, y, font_size, color_tuple
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Add text failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Text added successfully"
    }


@router.post("/highlight/{file_id}")
def add_highlight(
    file_id: str,
    page: int = Form(...),
    x0: float = Form(...),
    y0: float = Form(...),
    x1: float = Form(...),
    y1: float = Form(...),
    color: str = Form(default="1,1,0"),  # Yellow
    current_user: User = Depends(get_current_user)
):
    """Add highlight annotation to a page."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        color_tuple = tuple(float(c) for c in color.split(","))
    except:
        color_tuple = (1, 1, 0)

    try:
        pdf_service.add_highlight(
            file_path, output_path, page, x0, y0, x1, y1, color_tuple
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Highlight failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Highlight added successfully"
    }


@router.post("/redact/{file_id}")
def redact_area(
    file_id: str,
    page: int = Form(...),
    x0: float = Form(...),
    y0: float = Form(...),
    x1: float = Form(...),
    y1: float = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Redact (black out) an area on a page."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.redact_area(file_path, output_path, page, x0, y0, x1, y1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redaction failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Area redacted successfully"
    }


@router.post("/page-numbers")
def add_page_numbers(
    request: PageNumbersRequest,
    current_user: User = Depends(get_current_user)
):
    """Add page numbers to all pages."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.add_page_numbers(
            file_path, output_path, request.position, request.alignment, request.start_num
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Page numbers failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Page numbers added successfully"
    }


@router.post("/header-footer")
def add_header_footer(
    request: HeaderFooterRequest,
    current_user: User = Depends(get_current_user)
):
    """Add header and/or footer to all pages."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    if not request.header_text and not request.footer_text:
        raise HTTPException(status_code=400, detail="Provide header_text or footer_text")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.add_header_footer(
            file_path, output_path, request.header_text, request.footer_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Header/Footer failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Header/Footer added successfully"
    }


@router.get("/metadata/{file_id}")
def get_metadata(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get PDF metadata."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        metadata = pdf_service.get_metadata(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Get metadata failed: {str(e)}")

    return metadata


@router.post("/metadata")
def update_metadata(
    request: MetadataRequest,
    current_user: User = Depends(get_current_user)
):
    """Update PDF metadata."""
    file_path = os.path.join(settings.upload_dir, f"{request.file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.update_metadata(
            file_path, output_path,
            request.title, request.author, request.subject, request.keywords
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update metadata failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Metadata updated successfully"
    }


@router.post("/extract-images/{file_id}")
def extract_images(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Extract all images from a PDF."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_dir = os.path.join(settings.upload_dir, output_id)
    os.makedirs(output_dir, exist_ok=True)

    try:
        images = pdf_service.extract_images(file_path, output_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extract images failed: {str(e)}")

    return {
        "output_id": output_id,
        "images": images,
        "message": f"Extracted {len(images)} images"
    }


@router.post("/sign/{file_id}")
async def sign_pdf(
    file_id: str,
    signature: UploadFile = File(...),
    page: int = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    width: float = Form(default=100),
    height: float = Form(default=50),
    current_user: User = Depends(get_current_user)
):
    """Add signature image to a PDF."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Save signature temporarily
    sig_id = str(uuid.uuid4())
    sig_ext = os.path.splitext(signature.filename)[1] or ".png"
    sig_path = os.path.join(settings.upload_dir, f"{sig_id}{sig_ext}")

    content = await signature.read()
    with open(sig_path, "wb") as f:
        f.write(content)

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        await run_in_threadpool(
            pdf_service.sign_pdf,
            file_path,
            output_path,
            sig_path,
            page,
            x,
            y,
            width,
            height
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sign PDF failed: {str(e)}")
    finally:
        if os.path.exists(sig_path):
            os.remove(sig_path)

    return {
        "file_id": output_id,
        "message": "Signature added successfully"
    }


@router.post("/flatten/{file_id}")
def flatten_pdf(
    file_id: str,
    current_user: User = Depends(get_current_user)
):
    """Flatten PDF annotations and forms."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.flatten_pdf(file_path, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flatten failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "PDF flattened successfully"
    }


@router.post("/crop/{file_id}")
def crop_page(
    file_id: str,
    page: int = Form(...),
    x0: float = Form(...),
    y0: float = Form(...),
    x1: float = Form(...),
    y1: float = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Crop a specific page."""
    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        pdf_service.crop_page(file_path, output_path, page, x0, y0, x1, y1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Page cropped successfully"
    }
