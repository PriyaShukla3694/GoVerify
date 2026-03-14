from flask import Blueprint, jsonify
from models import db, Application, Document, ExtractedField
from services.preprocessing import preprocess_pipeline
from services.ocr import perform_ocr
from services.classifier import detect_document_type
from services.extractor import extract_fields
import os

process_bp = Blueprint('process', __name__)

@process_bp.route('/api/v1/process/<application_id>', methods=['POST'])
def process_application(application_id):
    application = Application.query.get(application_id)
    if not application:
        return jsonify({"error": "Application not found"}), 404
        
    documents = Document.query.filter_by(application_id=application.id).all()
    if not documents:
        return jsonify({"error": "No documents found for processing"}), 400

    results = []
    
    for doc in documents:
        # 1. Use compressed image if available, else original
        target_image = doc.compressed_path if doc.compressed_path and os.path.exists(doc.compressed_path) else doc.file_path
        
        # 2. Preprocess Image (Deskew, Denoise, Enhance)
        enhanced_path = preprocess_pipeline(target_image)
        
        # 3. Run OCR (Hindi+English)
        ocr_text, ocr_confidence = perform_ocr(enhanced_path)
        
        # 4. Detect Document Type if unknown
        if doc.document_type == 'unknown' or not doc.document_type:
            doc.document_type = detect_document_type(ocr_text)
            
        # 5. Extract Structured Fields
        extracted = extract_fields(ocr_text, doc.document_type)
        
        # 6. Store in Database
        doc.ocr_confidence = ocr_confidence
        
        # Clear old fields just in case of reprocessing
        ExtractedField.query.filter_by(document_id=doc.id).delete()
        
        for key, value in extracted.items():
            field = ExtractedField(
                document_id=doc.id,
                field_name=key,
                field_value=value,
                confidence=ocr_confidence # Using aggregate document confidence as a proxy
            )
            db.session.add(field)
            
        results.append({
            "document_id": doc.id,
            "type": doc.document_type,
            "extracted_fields": extracted,
            "ocr_confidence": ocr_confidence
        })

    # Calculate Aggregate Confidence and Validation
    from services.scoring import calculate_confidence
    scoring_results = calculate_confidence(str(application.id))

    application.status = "processed"
    db.session.commit()

    return jsonify({
        "application_id": application.id,
        "status": "processed",
        "scoring": scoring_results,
        "documents": results
    }), 200
