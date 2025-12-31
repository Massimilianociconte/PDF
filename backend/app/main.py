"""Main FastAPI application entry point."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.api import auth, pdf_operations, conversion

# Create upload directory if it doesn't exist
os.makedirs(settings.upload_dir, exist_ok=True)

app = FastAPI(
    title=settings.app_name,
    description="Private PDF manipulation web application",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(pdf_operations.router, prefix="/api/pdf", tags=["PDF Operations"])
app.include_router(conversion.router, prefix="/api/convert", tags=["Conversion"])


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.app_name}


@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    print(f"Starting {settings.app_name}...")
    print(f"Upload directory: {settings.upload_dir}")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    print(f"Shutting down {settings.app_name}...")
