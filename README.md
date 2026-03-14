# Intelligent Document Processing System

A hyper-local, intelligent document processing engine designed for rural citizens and government officers. Automatically extracts, cross-validates, and scores documents like Aadhaar and PAN using OCR and fuzzy matching.

## Quick Start (5 minutes)

### Prerequisites
- Python 3.9+
- Node.js 16+ 
- Tesseract OCR (`sudo apt-get install tesseract-ocr tesseract-ocr-hin`)
- Docker (optional)

### Setup
```bash
# Clone repo
git clone <repo-url>
cd intelligent-doc-processing

# Run setup script (Mac/Linux)
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or manual setup for Backend:
cd backend
python -m venv venv
source venv/bin/activate # (or venv\Scripts\activate on Windows)
pip install -r requirements.txt
python app.py

# Start Frontend (in a new terminal):
cd frontend
npm install
npm run dev
```

### Usage
1. Open up the frontend application.
2. Upload Aadhaar + PAN documents.
3. Fill out the metadata form.
4. Submit and wait briefly for processing.
5. Officer dashboard is available on the same application with flagged applications.
# GoVerify
# GoVerify
# GoVerify
# GoVerify
