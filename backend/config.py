import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Use environment variables with fallbacks
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    
    # Path setup for SQLite DB and Data storage
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    # Ensure data dirs exist
    os.makedirs(os.path.join(DATA_DIR, 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, 'processed'), exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(DATA_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB file size limit
    UPLOAD_FOLDER = os.path.join(DATA_DIR, 'uploads')
    PROCESSED_FOLDER = os.path.join(DATA_DIR, 'processed')
