"""Application configuration settings."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    app_name: str = "PDF Manipulator"
    debug: bool = False

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "change-this-in-production-use-strong-key")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    # Single user authentication
    admin_username: str = os.getenv("ADMIN_USERNAME", "admin")
    # Default password is "changeme123" (hashed)
    admin_password: str = os.getenv("ADMIN_PASSWORD", "$2b$12$EtQAPOPHcM1Dd62twvoigeXDpfyKeUHwGZ/ZhkpXbmmyUxtEUnzCm")

    # File storage
    upload_dir: str = os.getenv("UPLOAD_DIR", "/tmp/pdf_uploads")
    max_file_size: int = 100 * 1024 * 1024  # 100MB

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"


settings = Settings()
