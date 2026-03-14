import cv2
import numpy as np
import os

def deskew_image(image):
    """Detect and correct text rotation."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    # Inverse binary threshold
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Calculate angle
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    # Adjust angle
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
        
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    
    return rotated

def denoise_image(image):
    """Remove noise using Gaussian blur."""
    return cv2.GaussianBlur(image, (5, 5), 0)

def enhance_contrast(image):
    """Improve readability using CLAHE."""
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        return clahe.apply(image)

def binarize_image(image):
    """Convert to black & white."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def preprocess_pipeline(image_path, output_dir=None):
    """Full preprocessing pipeline returning path to enhanced image."""
    img = cv2.imread(image_path)
    if img is None:
        return image_path
        
    img = deskew_image(img)
    img = denoise_image(img)
    img = enhance_contrast(img)
    img = binarize_image(img)
    
    # Save the preprocessed image temporarily for OCR
    if not output_dir:
        output_dir = os.path.dirname(image_path)
    
    filename = os.path.basename(image_path)
    out_path = os.path.join(output_dir, f"preprocessed_{filename}.png")
    cv2.imwrite(out_path, img)
    
    return out_path
