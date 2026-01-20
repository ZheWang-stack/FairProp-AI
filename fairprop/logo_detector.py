import cv2
import numpy as np
import logging
from typing import Dict, Any
# from PIL import Image # Unused import removed

logger = logging.getLogger("fairprop.logo_detector")

class LogoDetector:
    """
    Detects the presence of Equal Housing Opportunity logo in property images.
    Uses template matching with OpenCV for reliable detection.
    """
    
    def __init__(self, template_path: str = "assets/eho_logo_template.png", threshold: float = 0.7):
        """
        Initialize the logo detector.
        
        Args:
            template_path: Path to the Equal Housing Opportunity logo template.
            threshold: Confidence threshold for detection (0.0 to 1.0).
        """
        self.template_path = template_path
        self.threshold = threshold
        self.template = None
        self._load_template()
    
    def _load_template(self):
        """Load the logo template for matching."""
        try:
            import os
            if os.path.exists(self.template_path):
                self.template = cv2.imread(self.template_path, cv2.IMREAD_GRAYSCALE)
                logger.info("Loaded logo template from %s", self.template_path)
            else:
                logger.warning("Logo template not found at %s. Logo detection disabled.", self.template_path)
        except Exception as e:
            logger.error("Failed to load logo template: %s", e)
    
    def detect_logo(self, image_input) -> Dict[str, Any]:
        """
        Detect Equal Housing Opportunity logo in an image.
        
        Args:
            image_input: PIL Image or path to image file.
            
        Returns:
            Dict with 'found' (bool), 'confidence' (float), and 'location' (tuple).
        """
        if self.template is None:
            return {
                "found": False,
                "confidence": 0.0,
                "message": "Logo template not loaded. Cannot perform detection."
            }
        
        try:
            # Convert PIL Image to OpenCV format
            if isinstance(image_input, str):
                img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)
            else:
                # PIL Image
                img_array = np.array(image_input.convert('L'))
                img = img_array
            
            if img is None:
                return {"found": False, "confidence": 0.0, "message": "Failed to load image"}
            
            # Perform template matching
            result = cv2.matchTemplate(img, self.template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            # Check if confidence exceeds threshold
            if max_val >= self.threshold:
                h, w = self.template.shape
                return {
                    "found": True,
                    "confidence": float(max_val),
                    "location": {
                        "top_left": max_loc,
                        "bottom_right": (max_loc[0] + w, max_loc[1] + h)
                    },
                    "message": f"Equal Housing Opportunity logo detected with {max_val:.2%} confidence."
                }
            else:
                return {
                    "found": False,
                    "confidence": float(max_val),
                    "message": f"Logo not found. Best match confidence: {max_val:.2%} (threshold: {self.threshold:.2%})"
                }
                
        except Exception as e:
            logger.error("Logo detection failed: %s", e)
            return {
                "found": False,
                "confidence": 0.0,
                "message": f"Detection error: {str(e)}"
            }
    
    def detect_logo_multi_scale(self, image_input) -> Dict[str, Any]:
        """
        Detect logo at multiple scales (more robust but slower).
        
        Args:
            image_input: PIL Image or path to image file.
            
        Returns:
            Dict with detection results.
        """
        if self.template is None:
            return {"found": False, "confidence": 0.0, "message": "Template not loaded"}
        
        try:
            # Load image
            if isinstance(image_input, str):
                img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)
            else:
                img_array = np.array(image_input.convert('L'))
                img = img_array
            
            if img is None:
                return {"found": False, "confidence": 0.0, "message": "Failed to load image"}
            
            # Try multiple scales
            best_confidence = 0.0
            best_location = None
            scales = [0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
            
            for scale in scales:
                resized_template = cv2.resize(self.template, None, fx=scale, fy=scale)
                
                # Skip if template is larger than image
                if resized_template.shape[0] > img.shape[0] or resized_template.shape[1] > img.shape[1]:
                    continue
                
                result = cv2.matchTemplate(img, resized_template, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(result)
                
                if max_val > best_confidence:
                    best_confidence = max_val
                    h, w = resized_template.shape
                    best_location = {
                        "top_left": max_loc,
                        "bottom_right": (max_loc[0] + w, max_loc[1] + h),
                        "scale": scale
                    }
            
            if best_confidence >= self.threshold:
                return {
                    "found": True,
                    "confidence": float(best_confidence),
                    "location": best_location,
                    "message": f"Logo detected at scale {best_location['scale']}x with {best_confidence:.2%} confidence."
                }
            else:
                return {
                    "found": False,
                    "confidence": float(best_confidence),
                    "message": f"Logo not found across all scales. Best: {best_confidence:.2%}"
                }
                
        except Exception as e:
            logger.error("Multi-scale detection failed: %s", e)
            return {"found": False, "confidence": 0.0, "message": f"Error: {str(e)}"}
