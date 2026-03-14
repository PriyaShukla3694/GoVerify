from fuzzywuzzy import fuzz
from models import ValidationResult, Application, Document, ExtractedField, db

def _get_field_val(fields, name):
    for f in fields:
        if f.field_name == name:
            return f.field_value
    return None

def cross_validate(application_id: str) -> dict:
    application = Application.query.get(application_id)
    if not application:
        return {}
        
    documents = Document.query.filter_by(application_id=application_id).all()
    
    # We expect at least an Aadhaar and a PAN for full cross-validation
    aadhaar_doc = next((d for d in documents if d.document_type == 'aadhaar'), None)
    pan_doc = next((d for d in documents if d.document_type == 'pan'), None)
    
    name_match = True
    dob_match = True
    address_match = False # PAN usually doesn't have address, so we check against user provided metadata
    mismatches = []
    
    aadhaar_name = None
    pan_name = None
    
    if aadhaar_doc and pan_doc:
        aadhaar_fields = aadhaar_doc.extracted_fields
        pan_fields = pan_doc.extracted_fields
        
        aadhaar_name = _get_field_val(aadhaar_fields, 'name')
        pan_name = _get_field_val(pan_fields, 'name')
        
        if aadhaar_name and pan_name:
            similarity = fuzz.token_sort_ratio(aadhaar_name.lower(), pan_name.lower())
            if similarity < 80:
                name_match = False
                mismatches.append({
                    "field": "name",
                    "aadhaar_value": aadhaar_name,
                    "pan_value": pan_name,
                    "similarity": similarity / 100.0
                })
                
        aadhaar_dob = _get_field_val(aadhaar_fields, 'dob')
        pan_dob = _get_field_val(pan_fields, 'dob')
        if aadhaar_dob and pan_dob and aadhaar_dob != pan_dob:
            dob_match = False
            mismatches.append({
                "field": "dob",
                "aadhaar_value": aadhaar_dob,
                "pan_value": pan_dob,
                "similarity": 0.0
            })

    # Validate against user provided metadata (if any)
    if application.provided_name:
        comparison_name = aadhaar_name or pan_name
        if comparison_name:
            sim = fuzz.token_sort_ratio(application.provided_name.lower(), comparison_name.lower())
            if sim < 80:
                name_match = False
                mismatches.append({
                    "field": "metadata_name",
                    "extracted_value": comparison_name,
                    "user_value": application.provided_name,
                    "similarity": sim / 100.0
                })

    if application.provided_address and aadhaar_doc:
        aadhaar_address = _get_field_val(aadhaar_doc.extracted_fields, 'address')
        if aadhaar_address:
            sim = fuzz.token_sort_ratio(application.provided_address.lower(), aadhaar_address.lower())
            address_match = sim >= 60
            if not address_match:
                mismatches.append({
                    "field": "address",
                    "extracted_value": aadhaar_address,
                    "user_value": application.provided_address,
                    "similarity": sim / 100.0
                })

    return {
        "name_match": name_match,
        "dob_match": dob_match,
        "address_match": address_match,
        "mismatches": mismatches
    }
