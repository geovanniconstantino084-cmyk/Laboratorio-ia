"""Validation utilities for inputs"""

import logging
from typing import Tuple
import os
from PIL import Image

logger = logging.getLogger(__name__)

# Allowed image formats
ALLOWED_FORMATS = {'JPEG', 'PNG', 'WEBP'}

# Maximum file size (20MB)
MAX_FILE_SIZE = 20 * 1024 * 1024

# Blacklisted characters/patterns
BLACKLISTED_PATTERNS = ['<script', 'javascript:', 'onclick', 'onerror']


def validate_image(image_path: str) -> Tuple[bool, str]:
    """
    Validate image file
    
    Args:
        image_path: Path to image file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file exists
        if not os.path.exists(image_path):
            return False, "File not found"
        
        # Check file size
        file_size = os.path.getsize(image_path)
        if file_size > MAX_FILE_SIZE:
            return False, f"File too large (max {MAX_FILE_SIZE / 1024 / 1024}MB)"
        
        # Check file format
        try:
            with Image.open(image_path) as img:
                if img.format not in ALLOWED_FORMATS:
                    return False, f"Format not supported. Allowed: {ALLOWED_FORMATS}"
                
                # Check dimensions
                width, height = img.size
                if width < 256 or height < 256:
                    return False, "Image too small (minimum 256x256)"
                if width > 4096 or height > 4096:
                    return False, "Image too large (maximum 4096x4096)"
        
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
        
        return True, "Valid"
        
    except Exception as e:
        logger.error(f"Error validating image: {str(e)}")
        return False, f"Validation error: {str(e)}"


def validate_prompt(text: str, max_length: int = 1000) -> bool:
    """
    Validate text prompt
    
    Args:
        text: Text to validate
        max_length: Maximum text length
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Check length
        if len(text) == 0 or len(text) > max_length:
            return False
        
        # Check for blacklisted patterns
        text_lower = text.lower()
        for pattern in BLACKLISTED_PATTERNS:
            if pattern in text_lower:
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating prompt: {str(e)}")
        return False
