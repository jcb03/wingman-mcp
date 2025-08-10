import base64
import io
from PIL import Image
from typing import Optional, Tuple

class ImageProcessor:
    @staticmethod
    def process_base64_image(base64_string: str) -> Optional[bytes]:
        """Process base64 image string and return bytes"""
        try:
            # Remove data URL prefix if present
            if "," in base64_string:
                base64_string = base64_string.split(",")[1]
            
            # Decode base64
            image_data = base64.b64decode(base64_string)
            
            # Validate it's a valid image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if too large (max 1024x1024 for API efficiency)
            if img.size[0] > 1024 or img.size[1] > 1024:
                img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=85)
            return output.getvalue()
            
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    @staticmethod
    def validate_image_size(image_data: bytes) -> bool:
        """Validate image size is reasonable"""
        try:
            # Max 10MB
            return len(image_data) <= 10 * 1024 * 1024
        except:
            return False

# Global processor instance
image_processor = ImageProcessor()
