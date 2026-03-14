from utils.patterns import AADHAAR_KEYWORDS, PAN_KEYWORDS, PASSPORT_KEYWORDS

def detect_document_type(ocr_text: str) -> str:
    """
    Returns: 'aadhaar', 'pan', 'passport', 'voter_id', 'driving_license', 'unknown'
    """
    text = ocr_text.lower()
    
    # Check simple keyword matches
    if any(keyword in text for keyword in AADHAAR_KEYWORDS):
        return 'aadhaar'
        
    if any(keyword in text for keyword in PAN_KEYWORDS):
        return 'pan'
        
    if any(keyword in text for keyword in PASSPORT_KEYWORDS):
        return 'passport'
        
    return 'unknown'
