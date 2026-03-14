from services.validator import cross_validate, _get_field_val
from models import db, Application, Document, ValidationResult
import json

def calculate_confidence(application_id: str) -> dict:
    application = Application.query.get(application_id)
    if not application:
        return {}

    # Run validation
    validation_data = cross_validate(application_id)
    documents = Document.query.filter_by(application_id=application_id).all()
    
    field_scores = {}
    aggregate_score = 0.0
    field_count = 0
    
    # Analyze fields across documents
    for doc in documents:
        for field in doc.extracted_fields:
            # Base rules
            ocr_conf = field.confidence or 0.0
            format_conf = 1.0 # Assuming regex matched, it is 1.0 format valid
            match_conf = 1.0
            
            # Check if this field had a mismatch
            for mismatch in validation_data.get('mismatches', []):
                if field.field_name in mismatch.get('field', ''):
                    match_conf = mismatch.get('similarity', 0.0)
                    break
                    
            field_confidence = (ocr_conf * 0.4) + (format_conf * 0.3) + (match_conf * 0.3)
            field_scores[field.field_name] = round(field_confidence, 2)
            
            aggregate_score += field_confidence
            field_count += 1
            
    overall_confidence = round(aggregate_score / field_count, 2) if field_count > 0 else 0.0
    
    # Determine Recommendation
    if overall_confidence >= 0.90:
        recommendation = "auto_approve"
    elif overall_confidence >= 0.70:
        recommendation = "flag_for_review"
    else:
        recommendation = "manual_review_required"
        
    # Store Validation Result in DB
    val_result = ValidationResult(
        application_id=application_id,
        name_match=validation_data.get('name_match', False),
        dob_match=validation_data.get('dob_match', False),
        address_match=validation_data.get('address_match', False),
        mismatches=json.dumps(validation_data.get('mismatches', [])),
        field_confidence_scores=json.dumps(field_scores)
    )
    db.session.add(val_result)
    
    # Update app
    application.overall_confidence = overall_confidence
    application.recommendation = recommendation
    application.status = "flagged_for_review" if recommendation != "auto_approve" else "approved"
    
    db.session.commit()
    
    return {
        "overall_confidence": overall_confidence,
        "field_scores": field_scores,
        "recommendation": recommendation,
        "validation_data": validation_data
    }
