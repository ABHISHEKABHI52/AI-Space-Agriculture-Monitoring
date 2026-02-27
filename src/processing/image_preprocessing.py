"""
Image Preprocessing Module
Handles image loading, resizing, color conversion, and plant segmentation
"""

import cv2
import numpy as np
from typing import Tuple, Optional
import os


class ImagePreprocessor:
    """
    Image preprocessing for plant health analysis
    """
    
    def __init__(self, target_size: Tuple[int, int] = (640, 480)):
        """
        Initialize preprocessor
        
        Args:
            target_size: Target image size (width, height)
        """
        self.target_size = target_size
        # HSV color range for green (plant leaves)
        self.hsv_lower = np.array([35, 40, 40])
        self.hsv_upper = np.array([85, 255, 255])
        
    def load_image(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load image from file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Loaded image or None if failed
        """
        if not os.path.exists(image_path):
            print(f"Error: Image not found at {image_path}")
            return None
            
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not read image {image_path}")
            return None
            
        return image
    
    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image to target size
        
        Args:
            image: Input image
            
        Returns:
            Resized image
        """
        return cv2.resize(image, self.target_size)
    
    def convert_to_hsv(self, image: np.ndarray) -> np.ndarray:
        """
        Convert BGR image to HSV color space
        
        Args:
            image: BGR image
            
        Returns:
            HSV image
        """
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    def create_green_mask(self, hsv_image: np.ndarray) -> np.ndarray:
        """
        Create binary mask for green regions (plant leaves)
        
        Args:
            hsv_image: Image in HSV color space
            
        Returns:
            Binary mask (0 or 255)
        """
        mask = cv2.inRange(hsv_image, self.hsv_lower, self.hsv_upper)
        return mask
    
    def remove_noise(self, mask: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """
        Remove noise from binary mask using morphological operations
        
        Args:
            mask: Binary mask
            kernel_size: Kernel size for morphological operations
            
        Returns:
            Cleaned mask
        """
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        # Opening: removes small noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Closing: fills small holes
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        return mask
    
    def extract_plant_region(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Extract plant region from image using mask
        
        Args:
            image: Original image
            mask: Binary mask
            
        Returns:
            Masked image (plant only)
        """
        result = cv2.bitwise_and(image, image, mask=mask)
        return result
    
    def preprocess(self, image_path: str, save_output: bool = False, 
                   output_path: str = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Complete preprocessing pipeline
        
        Args:
            image_path: Path to input image
            save_output: Whether to save processed images
            output_path: Directory to save outputs
            
        Returns:
            Tuple of (original_resized, plant_mask, extracted_plant)
        """
        # Load image
        image = self.load_image(image_path)
        if image is None:
            return None, None, None
        
        # Resize
        image_resized = self.resize_image(image)
        
        # Convert to HSV
        hsv = self.convert_to_hsv(image_resized)
        
        # Create green mask
        mask = self.create_green_mask(hsv)
        
        # Remove noise
        mask_clean = self.remove_noise(mask)
        
        # Extract plant region
        plant_extracted = self.extract_plant_region(image_resized, mask_clean)
        
        # Save outputs if requested
        if save_output and output_path:
            os.makedirs(output_path, exist_ok=True)
            filename = os.path.basename(image_path)
            name, ext = os.path.splitext(filename)
            
            cv2.imwrite(os.path.join(output_path, f"{name}_original{ext}"), image_resized)
            cv2.imwrite(os.path.join(output_path, f"{name}_mask{ext}"), mask_clean)
            cv2.imwrite(os.path.join(output_path, f"{name}_extracted{ext}"), plant_extracted)
        
        return image_resized, mask_clean, plant_extracted


def preprocess_image(image_path: str, target_size: Tuple[int, int] = (640, 480)) -> dict:
    """
    Convenience function for image preprocessing
    
    Args:
        image_path: Path to image
        target_size: Target image size
        
    Returns:
        Dictionary with processed images
    """
    preprocessor = ImagePreprocessor(target_size)
    original, mask, extracted = preprocessor.preprocess(image_path)
    
    return {
        'original': original,
        'mask': mask,
        'extracted': extracted,
        'success': original is not None
    }


if __name__ == "__main__":
    # Test preprocessing
    print("Image Preprocessing Module")
    print("=" * 50)
    
    # Example usage
    test_image = "data/raw/control/plant1_day1.jpg"
    if os.path.exists(test_image):
        result = preprocess_image(test_image)
        if result['success']:
            print("✅ Preprocessing successful")
            print(f"Image shape: {result['original'].shape}")
        else:
            print("❌ Preprocessing failed")
    else:
        print(f"Test image not found: {test_image}")
        print("Please add sample images to test the module")
