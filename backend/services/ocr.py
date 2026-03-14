import pytesseract
from PIL import Image
import os

def perform_ocr(image_path, lang='hin+eng'):
    """
    Runs Tesseract OCR on a preprocessed image.
    Supports Hindi and English by default.
    Returns: extracted_text (str), average_confidence (float)
    """
    if not os.path.exists(image_path):
        return "", 0.0
        
    try:
        # Get raw text
        text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
        
        # Get detailed data for confidence scoring
        data = pytesseract.image_to_data(Image.open(image_path), lang=lang, output_type=pytesseract.Output.DICT)
        
        # Calculate average confidence
        confidences = [int(c) for c in data['conf'] if int(c) >= 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        # Normalize text slightly
        text = text.strip()
        
        return text, avg_confidence / 100.0  # normalize to 0-1
        
    except Exception as e:
        print(f"OCR Exception: {e}")
        return "", 0.0
