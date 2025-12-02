"""PDF operations API endpoints."""
import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
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
        info = pdf_service.get_pdf_info(file_path)
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
async def get_pdf_info(
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
async def merge_pdfs(
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
async def split_pdf(
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
async def rotate_pdf(
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
async def ocr_pdf(
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
async def extract_text(
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
        pdf_service.add_image(file_path, output_path, image_path, page, x, y, width, height)
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
async def download_pdf(
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
async def delete_pdf(
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
async def get_page_preview(
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
