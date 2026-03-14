import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_file(file, filename=None):
    """
    Validates a single file object.
    Returns (True, None) if valid, or (False, error_message).
    """
    if not file or not (filename or file.filename):
        return False, "No file provided"
    
    name = filename or file.filename
    if not allowed_file(name):
        return False, "File type not allowed. Supported: jpg, png, pdf."
        
    # Checking file size using stream end
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    
    if size > MAX_FILE_SIZE:
        return False, "File exceeds 10MB size limit."
        
    return True, None
