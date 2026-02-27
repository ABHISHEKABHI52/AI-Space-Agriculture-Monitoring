"""
Plant Segmentation Module
Advanced segmentation techniques for plant isolation
"""

import cv2
import numpy as np
from typing import List, Tuple


class PlantSegmenter:
    """
    Advanced plant segmentation using contour detection
    """
    
    def __init__(self, min_contour_area: int = 1000):
        """
        Initialize segmenter
        
        Args:
            min_contour_area: Minimum area for valid plant contour
        """
        self.min_contour_area = min_contour_area
    
    def find_plant_contours(self, mask: np.ndarray) -> List:
        """
        Find contours of plant in binary mask
        
        Args:
            mask: Binary mask image
            
        Returns:
            List of contours
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter small contours
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > self.min_contour_area]
        
        return valid_contours
    
    def get_largest_contour(self, contours: List) -> np.ndarray:
        """
        Get the largest contour (main plant)
        
        Args:
            contours: List of contours
            
        Returns:
            Largest contour or None
        """
        if not contours:
            return None
        
        largest = max(contours, key=cv2.contourArea)
        return largest
    
    def draw_contours(self, image: np.ndarray, contours: List, 
                     color: Tuple[int, int, int] = (0, 255, 0), 
                     thickness: int = 2) -> np.ndarray:
        """
        Draw contours on image
        
        Args:
            image: Input image
            contours: List of contours
            color: Color in BGR
            thickness: Line thickness
            
        Returns:
            Image with drawn contours
        """
        result = image.copy()
        cv2.drawContours(result, contours, -1, color, thickness)
        return result
    
    def get_bounding_box(self, contour: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Get bounding box for contour
        
        Args:
            contour: Input contour
            
        Returns:
            (x, y, width, height)
        """
        return cv2.boundingRect(contour)
    
    def crop_to_plant(self, image: np.ndarray, contour: np.ndarray, 
                      padding: int = 10) -> np.ndarray:
        """
        Crop image to plant region with padding
        
        Args:
            image: Input image
            contour: Plant contour
            padding: Padding around plant
            
        Returns:
            Cropped image
        """
        x, y, w, h = self.get_bounding_box(contour)
        
        # Add padding
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(image.shape[1] - x, w + 2 * padding)
        h = min(image.shape[0] - y, h + 2 * padding)
        
        cropped = image[y:y+h, x:x+w]
        return cropped
    
    def segment_plant(self, image: np.ndarray, mask: np.ndarray) -> dict:
        """
        Complete plant segmentation pipeline
        
        Args:
            image: Original image
            mask: Binary mask
            
        Returns:
            Dictionary with segmentation results
        """
        # Find contours
        contours = self.find_plant_contours(mask)
        
        if not contours:
            return {
                'success': False,
                'contours': [],
                'largest_contour': None,
                'bounding_box': None,
                'cropped': None
            }
        
        # Get largest contour (main plant)
        largest = self.get_largest_contour(contours)
        bbox = self.get_bounding_box(largest)
        
        # Draw contours
        contour_image = self.draw_contours(image, [largest])
        
        # Crop to plant
        cropped = self.crop_to_plant(image, largest)
        
        return {
            'success': True,
            'contours': contours,
            'largest_contour': largest,
            'bounding_box': bbox,
            'contour_image': contour_image,
            'cropped': cropped,
            'num_contours': len(contours)
        }


def segment_plant_from_image(image: np.ndarray, mask: np.ndarray, 
                             min_area: int = 1000) -> dict:
    """
    Convenience function for plant segmentation
    
    Args:
        image: Original image
        mask: Binary mask
        min_area: Minimum contour area
        
    Returns:
        Segmentation results
    """
    segmenter = PlantSegmenter(min_contour_area=min_area)
    return segmenter.segment_plant(image, mask)


if __name__ == "__main__":
    print("Plant Segmentation Module")
    print("=" * 50)
    print("This module provides advanced segmentation capabilities")
    print("for isolating plants from background")
