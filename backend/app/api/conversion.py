"""Conversion API endpoints."""
import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from fastapi.responses import FileResponse

from app.api.auth import User, get_current_user
from app.config import settings
from app.services.conversion_service import ConversionService
from app.utils import validate_uuid, validate_safe_filename

router = APIRouter()
conversion_service = ConversionService()


@router.post("/image-to-pdf")
async def convert_image_to_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Convert an image to PDF."""
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image format. Allowed: {', '.join(allowed_extensions)}"
        )

    # Save image temporarily
    image_id = str(uuid.uuid4())
    image_path = os.path.join(settings.upload_dir, f"{image_id}{ext}")

    content = await file.read()
    with open(image_path, "wb") as f:
        f.write(content)

    # Convert to PDF
    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        conversion_service.image_to_pdf(image_path, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    finally:
        # Clean up temp image
        if os.path.exists(image_path):
            os.remove(image_path)

    return {
        "file_id": output_id,
        "message": "Image converted to PDF successfully"
    }


@router.post("/pdf-to-images/{file_id}")
async def convert_pdf_to_images(
    file_id: str,
    format: str = Form(default="png"),
    dpi: int = Form(default=150),
    current_user: User = Depends(get_current_user)
):
    """Convert PDF pages to images."""
    validate_uuid(file_id)
    if format not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=400, detail="Format must be png or jpg")

    file_path = os.path.join(settings.upload_dir, f"{file_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    output_id = str(uuid.uuid4())
    output_dir = os.path.join(settings.upload_dir, output_id)
    os.makedirs(output_dir, exist_ok=True)

    try:
        images = conversion_service.pdf_to_images(file_path, output_dir, format, dpi)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

    return {
        "output_id": output_id,
        "images": images,
        "message": f"PDF converted to {len(images)} images"
    }


@router.post("/text-to-pdf")
async def convert_text_to_pdf(
    text: str = Form(...),
    font_size: int = Form(default=12),
    current_user: User = Depends(get_current_user)
):
    """Convert plain text to PDF."""
    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        conversion_service.text_to_pdf(text, output_path, font_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "Text converted to PDF successfully"
    }


@router.post("/html-to-pdf")
async def convert_html_to_pdf(
    html: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Convert HTML to PDF."""
    output_id = str(uuid.uuid4())
    output_path = os.path.join(settings.upload_dir, f"{output_id}.pdf")

    try:
        conversion_service.html_to_pdf(html, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

    return {
        "file_id": output_id,
        "message": "HTML converted to PDF successfully"
    }


@router.get("/download-image/{output_id}/{filename}")
async def download_converted_image(
    output_id: str,
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """Download a converted image."""
    validate_uuid(output_id)
    validate_safe_filename(filename)

    file_path = os.path.join(settings.upload_dir, output_id, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    media_type = "image/png" if filename.endswith(".png") else "image/jpeg"

    return FileResponse(file_path, media_type=media_type, filename=filename)
