import os
from werkzeug.utils import secure_filename
from flask import current_app

def save_uploaded_file(file, application_id, document_type=None):
    """
    Saves an uploaded file to data/uploads/{application_id}/.
    Returns the absolute path to the saved file and its size.
    """
    upload_base = current_app.config['UPLOAD_FOLDER']
    app_folder = os.path.join(upload_base, application_id)
    
    os.makedirs(app_folder, exist_ok=True)
    
    filename = secure_filename(file.filename)
    if document_type:
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        filename = f"{document_type}.{ext}"
        
    file_path = os.path.join(app_folder, filename)
    file.save(file_path)
    
    # Get file size
    size_bytes = os.path.getsize(file_path)
    
    return file_path, size_bytes
