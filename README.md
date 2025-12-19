# PDF Manipulator

A private, self-hosted web application for complete PDF manipulation. Built with React (frontend) and Python/FastAPI (backend).

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Features

### 📄 Core PDF Operations
- **Upload & Download**: Secure file upload and download with authentication
- **Merge**: Combine multiple PDFs into a single document with custom ordering
- **Split**: Extract specific pages from a PDF
- **Rotate**: Rotate individual pages (90°, 180°, 270°)
- **Delete Pages**: Remove unwanted pages from PDFs
- **Reorder Pages**: Rearrange pages in any order

### 🔄 Conversion
- **Image to PDF**: Convert images (JPG, PNG, GIF, BMP, TIFF, WebP) to PDF
- **PDF to Images**: Export PDF pages as images (PNG, JPEG)
- **Text to PDF**: Convert plain text to PDF
- **HTML to PDF**: Convert HTML content to PDF

### 🔍 Text & OCR
- **Text Extraction**: Extract text content from PDFs
- **OCR (Optical Character Recognition)**: Extract text from scanned documents using Tesseract

### 🗜️ Optimization
- **Compress**: Reduce PDF file size while maintaining quality
- **Flatten**: Flatten annotations and form fields

### ✏️ Annotations & Editing
- **Add Text**: Insert text annotations anywhere on pages
- **Highlight**: Add colored highlights to areas
- **Redact**: Permanently black out sensitive information
- **Add Images**: Insert images into PDF pages
- **Watermark**: Add text watermarks to all pages

### 🔐 Security
- **Encrypt**: Password-protect PDFs with AES-256 encryption
- **Decrypt**: Remove password protection from PDFs
- **Single-user authentication (JWT-based)**

### 📝 Document Properties
- **Page Numbers**: Add page numbers with customizable position
- **Headers & Footers**: Add headers and footers to all pages
- **Metadata Editor**: Edit document title, author, subject, keywords

### ✍️ Digital Signatures
- **Sign PDF**: Add signature images to documents
- **Crop Pages**: Crop pages to specific dimensions

## Quick Start with Docker

### Prerequisites
- Docker
- Docker Compose

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-manipulator.git
cd pdf-manipulator
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Edit `.env` with your secure credentials:
```env
SECRET_KEY=your-super-secret-key-minimum-32-characters
ADMIN_USERNAME=your-username
ADMIN_PASSWORD=your-secure-password
```

4. Build and run:
```bash
docker-compose up -d --build
```

5. Access the application at `http://localhost`

## Development Setup

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (system dependency)
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Run the server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Access the app at `http://localhost:3000`

## API Documentation

Once the backend is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

#### Authentication
- `POST /api/auth/token` - Login and get access token
- `GET /api/auth/me` - Get current user info

#### PDF Operations
- `POST /api/pdf/upload` - Upload a PDF file
- `GET /api/pdf/info/{file_id}` - Get PDF information
- `GET /api/pdf/download/{file_id}` - Download a PDF
- `DELETE /api/pdf/{file_id}` - Delete a PDF
- `POST /api/pdf/merge` - Merge multiple PDFs
- `POST /api/pdf/split` - Split/extract pages from a PDF
- `POST /api/pdf/rotate/{file_id}` - Rotate a page
- `GET /api/pdf/text/{file_id}` - Extract text
- `POST /api/pdf/ocr/{file_id}` - Perform OCR

#### Conversion
- `POST /api/convert/image-to-pdf` - Convert image to PDF
- `POST /api/convert/pdf-to-images/{file_id}` - Convert PDF to images
- `POST /api/convert/text-to-pdf` - Convert text to PDF
- `POST /api/convert/html-to-pdf` - Convert HTML to PDF

## Project Structure

```
pdf-manipulator/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── pdf_operations.py # PDF manipulation endpoints
│   │   │   └── conversion.py     # File conversion endpoints
│   │   ├── services/
│   │   │   ├── pdf_service.py    # PDF processing logic
│   │   │   └── conversion_service.py # Conversion logic
│   │   ├── config.py             # App configuration
│   │   └── main.py               # FastAPI application
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── services/             # API services
│   │   ├── hooks/                # Custom React hooks
│   │   └── App.jsx               # Main app component
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyMuPDF (fitz)** - PDF manipulation library
- **Tesseract** - OCR engine
- **Pillow** - Image processing
- **python-jose** - JWT token handling
- **passlib** - Password hashing

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Axios** - HTTP client
- **React Router** - Routing
- **Lucide React** - Icons
- **react-dropzone** - File upload

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | JWT secret key | `change-this-in-production` |
| `ADMIN_USERNAME` | Login username | `admin` |
| `ADMIN_PASSWORD` | Login password | `changeme123` |
| `UPLOAD_DIR` | File storage directory | `/tmp/pdf_uploads` |
| `MAX_FILE_SIZE` | Max upload size (bytes) | `104857600` (100MB) |

## Security Considerations

1. **Change default credentials** before deploying to production
2. **Use a strong SECRET_KEY** (minimum 32 characters)
3. **Use HTTPS** in production (configure reverse proxy)
4. **Limit access** to trusted networks only
5. Files are stored temporarily and should be cleaned periodically

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request