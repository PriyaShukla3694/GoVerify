from models import Application, Document, ValidationResult
import json

def generate_report(application_id: str) -> dict:
    application = Application.query.get(application_id)
    if not application:
        return {"error": "Application not found"}
        
    validation = ValidationResult.query.filter_by(application_id=application_id).first()
    documents = Document.query.filter_by(application_id=application_id).all()
    
    docs_payload = []
    for doc in documents:
        docs_payload.append({
            "document_id": doc.id,
            "type": doc.document_type,
            "extracted_fields": {f.field_name: f.field_value for f in doc.extracted_fields},
            "ocr_confidence": doc.ocr_confidence
        })
        
    report = {
        "application_id": application.id,
        "timestamp": str(application.created_at),
        "overall_confidence": application.overall_confidence,
        "recommendation": application.recommendation,
        "documents_processed": docs_payload,
        "validation_results": {},
        "field_confidence_scores": {},
        "flags": [],
        "metadata_comparison": {
            "user_provided_name": application.provided_name,
            "user_provided_dob": application.provided_dob,
            "user_provided_address": application.provided_address,
        }
    }
    
    if validation:
        report["validation_results"] = {
            "name_match": validation.name_match,
            "dob_match": validation.dob_match,
            "address_match": validation.address_match
        }
        report["field_confidence_scores"] = json.loads(validation.field_confidence_scores) if validation.field_confidence_scores else {}
        
        mismatches = json.loads(validation.mismatches) if validation.mismatches else []
        for miss in mismatches:
            report["flags"].append({
                "field": miss.get("field"),
                "reason": f"Low similarity between documents ({miss.get('similarity', 0)*100}%)",
                "severity": "medium" if miss.get('similarity', 0) > 0.5 else "high"
            })
            
    return report
