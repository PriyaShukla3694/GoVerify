import re
from utils.patterns import AADHAAR_NUMBER_PATTERN, PAN_NUMBER_PATTERN, DOB_PATTERN

def extract_fields(ocr_text: str, doc_type: str) -> dict:
    """
    Extracts structured fields from raw OCR text.
    Returns: {"name": ..., "dob": ..., "document_number": ...}
    """
    fields = {}
    lines = [line.strip() for line in ocr_text.split('\n') if line.strip()]
    
    # Global DOB extraction
    dob_match = re.search(DOB_PATTERN, ocr_text)
    if dob_match:
        fields['dob'] = dob_match.group()

    if doc_type == 'aadhaar':
        # Aadhaar Number
        num_match = re.search(AADHAAR_NUMBER_PATTERN, ocr_text)
        if num_match:
            fields['document_number'] = num_match.group()
            
        # Very rough name extraction heuristic for hackathon
        for i, line in enumerate(lines):
            # Look for line before DOB
            if 'dob' in fields and fields['dob'] in line.lower() and i > 0:
                fields['name'] = lines[i-1]
                break

    elif doc_type == 'pan':
        # PAN Number
        num_match = re.search(PAN_NUMBER_PATTERN, ocr_text)
        if num_match:
            fields['document_number'] = num_match.group()
            
        # Name Extraction Heuristic (Usually above Father's Name)
        for i, line in enumerate(lines):
            if "father" in line.lower() or "पिता" in line:
                if i > 0:
                    fields['name'] = lines[i-1]
                if i + 1 < len(lines):
                    fields['father_name'] = lines[i+1]
                break

    # Apply Auto-Correction / Normalization Here
    from utils.normalizer import clean_name, normalize_address
    
    if 'name' in fields:
        fields['name'] = clean_name(fields['name'])
    if 'father_name' in fields:
        fields['father_name'] = clean_name(fields['father_name'])
    if 'address' in fields:
        fields['address'] = normalize_address(fields['address'])
                
    return fields
