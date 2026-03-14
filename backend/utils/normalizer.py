import re

ADDRESS_DICTIONARY = {
    'apt': 'apartment',
    'bldg': 'building',
    'flr': 'floor',
    'st': 'street',
    'rd': 'road',
    'ave': 'avenue',
    'blvd': 'boulevard',
    'dist': 'district',
    'tal': 'taluka',
    'vill': 'village',
    'opp': 'opposite',
    'nr': 'near'
}

def normalize_address(address: str) -> str:
    if not address:
        return ""
        
    normalized = address.lower()
    
    # Remove excessive punctuation
    normalized = re.sub(r'[^\w\s]', ' ', normalized)
    
    # Replace abbreviations
    words = normalized.split()
    normalized_words = [ADDRESS_DICTIONARY.get(w, w) for w in words]
    
    return ' '.join(normalized_words).title()

def clean_name(name: str) -> str:
    """Removes common OCR artifacts from names."""
    if not name:
        return ""
    # Remove numbers and special chars from supposed names
    cleaned = re.sub(r'[^A-Za-z\s]', '', name)
    return ' '.join(cleaned.split()).title()
