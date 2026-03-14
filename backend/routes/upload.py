from flask import Blueprint, request, jsonify, current_app
from models import db, Application, Document
from services.storage import save_uploaded_file
from utils.validators import validate_file

from services.compression import compress_image

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/api/v1/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"error": "No files part in the request"}), 400

    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected for uploading"}), 400

    # Parse metadata if sent
    metadata = request.form.get('metadata', {})
    
    # 1. Create Application
    application = Application(
        provided_name=request.form.get('name', ''),
        provided_dob=request.form.get('dob', ''),
        provided_address=request.form.get('address', '')
    )
    db.session.add(application)
    db.session.flush() # get application ID

    upload_results = []
    
    # 2. Process Files
    for file in files:
        is_valid, error = validate_file(file)
        if not is_valid:
            continue
            
        # Detect basic document type from form input if provided, else use general naming
        doc_type = request.form.get(f'type_{file.filename}', 'unknown')
        
        # Save original file
        file_path, size_bytes = save_uploaded_file(file, str(application.id))
        
        # Compress the file immediately (Hackathon shortcut: Sync processing)
        compressed_path, compressed_size_bytes = compress_image(file_path, current_app.config['PROCESSED_FOLDER'])
        
        document = Document(
            application_id=application.id,
            original_filename=file.filename,
            file_path=file_path,
            compressed_path=compressed_path,
            file_size_bytes=size_bytes,
            compressed_size_bytes=compressed_size_bytes,
            document_type=doc_type
        )
        db.session.add(document)
        upload_results.append({
            "filename": file.filename,
            "original_size": size_bytes,
            "compressed_size": compressed_size_bytes
        })

    if not upload_results:
        db.session.rollback()
        return jsonify({"error": "All files failed validation."}), 400

    db.session.commit()

    return jsonify({
        "application_id": application.id,
        "status": "uploaded",
        "files": upload_results
    }), 201
