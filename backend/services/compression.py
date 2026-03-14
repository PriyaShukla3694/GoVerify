import os
from PIL import Image

def compress_image(input_path, output_dir=None):
    """
    Compresses images for OCR storage efficiency.
    Target: 60-80% reduction without losing readability.
    Returns the path to the compressed image and its new size.
    """
    filename = os.path.basename(input_path)
    if not output_dir:
        output_dir = os.path.dirname(input_path)
        
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepend compressed_ to distinguish, or place in a separate directory
    compressed_filename = f"compressed_{filename}"
    output_path = os.path.join(output_dir, compressed_filename)
        
    try:
        # Standard PIL execution for image optimization
        with Image.open(input_path) as img:
            # Convert RGBA to RGB if processing PNGs to JPEG
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                
            # Resize if dimensions are overly large (e.g. > 1920)
            max_size = 1920
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
                
            # Save as optimized JPEG
            img.save(output_path, 'JPEG', quality=85, optimize=True)
            
        new_size_bytes = os.path.getsize(output_path)
        return output_path, new_size_bytes
        
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")
        return input_path, os.path.getsize(input_path)
