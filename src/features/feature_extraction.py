"""
Feature Extraction Module
Extracts quantitative features from plant images for health analysis
"""

import cv2
import numpy as np
from typing import Dict, List
import pandas as pd
from datetime import datetime


class FeatureExtractor:
    """
    Extract health-related features from plant images
    """
    
    def __init__(self):
        """Initialize feature extractor"""
        pass
    
    def calculate_leaf_area(self, mask: np.ndarray) -> int:
        """
        Calculate leaf area from binary mask
        
        Args:
            mask: Binary mask of plant
            
        Returns:
            Leaf area in pixels
        """
        # Count non-zero pixels (green/plant pixels)
        leaf_area = np.count_nonzero(mask)
        return leaf_area
    
    def calculate_green_intensity(self, image: np.ndarray, mask: np.ndarray) -> float:
        """
        Calculate average green intensity of plant
        
        Args:
            image: BGR image
            mask: Binary mask of plant
            
        Returns:
            Average green channel value
        """
        if mask is None or np.count_nonzero(mask) == 0:
            return 0.0
        
        # Extract green channel
        green_channel = image[:, :, 1]
        
        # Get green values only from plant region
        plant_green = green_channel[mask > 0]
        
        if len(plant_green) == 0:
            return 0.0
        
        # Calculate average
        avg_green = np.mean(plant_green)
        return float(avg_green)
    
    def calculate_green_index(self, image: np.ndarray, mask: np.ndarray) -> float:
        """
        Calculate normalized green index
        
        Args:
            image: BGR image
            mask: Binary mask
            
        Returns:
            Green index value
        """
        if mask is None or np.count_nonzero(mask) == 0:
            return 0.0
        
        # Get plant pixels
        plant_pixels = image[mask > 0]
        
        if len(plant_pixels) == 0:
            return 0.0
        
        # Calculate relative green
        # Green Index = (2*G - R - B) / (2*G + R + B)
        b, g, r = plant_pixels[:, 0], plant_pixels[:, 1], plant_pixels[:, 2]
        
        numerator = 2 * g - r - b
        denominator = 2 * g + r + b + 1e-6  # avoid division by zero
        
        green_index = np.mean(numerator / denominator) * 100
        return float(green_index)
    
    def calculate_plant_height(self, mask: np.ndarray) -> int:
        """
        Calculate plant height from mask
        
        Args:
            mask: Binary mask
            
        Returns:
            Height in pixels
        """
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0
        
        # Get bounding box of largest contour
        largest = max(contours, key=cv2.contourArea)
        _, _, _, height = cv2.boundingRect(largest)
        
        return height
    
    def calculate_plant_width(self, mask: np.ndarray) -> int:
        """
        Calculate plant width from mask
        
        Args:
            mask: Binary mask
            
        Returns:
            Width in pixels
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0
        
        largest = max(contours, key=cv2.contourArea)
        _, _, width, _ = cv2.boundingRect(largest)
        
        return width
    
    def calculate_compactness(self, mask: np.ndarray) -> float:
        """
        Calculate compactness (circularity) of plant
        
        Args:
            mask: Binary mask
            
        Returns:
            Compactness value (0-1)
        """
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return 0.0
        
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        perimeter = cv2.arcLength(largest, True)
        
        if perimeter == 0:
            return 0.0
        
        # Compactness = 4π * area / perimeter²
        compactness = (4 * np.pi * area) / (perimeter ** 2)
        return float(compactness)
    
    def extract_all_features(self, image: np.ndarray, mask: np.ndarray, 
                            plant_id: str = None, group: str = None) -> Dict:
        """
        Extract all features from image
        
        Args:
            image: BGR image
            mask: Binary mask
            plant_id: Plant identifier
            group: Experimental group
            
        Returns:
            Dictionary of features
        """
        features = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'plant_id': plant_id,
            'group': group,
            'leaf_area': self.calculate_leaf_area(mask),
            'green_intensity': self.calculate_green_intensity(image, mask),
            'green_index': self.calculate_green_index(image, mask),
            'plant_height': self.calculate_plant_height(mask),
            'plant_width': self.calculate_plant_width(mask),
            'compactness': self.calculate_compactness(mask)
        }
        
        return features
    
    def calculate_growth_rate(self, historical_data: pd.DataFrame, 
                             plant_id: str, window_days: int = 3) -> float:
        """
        Calculate growth rate from historical data
        
        Args:
            historical_data: DataFrame with historical measurements
            plant_id: Plant identifier
            window_days: Time window for calculation
            
        Returns:
            Growth rate (area change per day)
        """
        # Filter data for this plant
        plant_data = historical_data[historical_data['plant_id'] == plant_id]
        
        if len(plant_data) < 2:
            return 0.0
        
        # Sort by timestamp
        plant_data = plant_data.sort_values('timestamp')
        
        # Get recent data
        recent = plant_data.tail(window_days)
        
        if len(recent) < 2:
            return 0.0
        
        # Calculate rate
        first_area = recent.iloc[0]['leaf_area']
        last_area = recent.iloc[-1]['leaf_area']
        
        growth_rate = (last_area - first_area) / len(recent)
        return float(growth_rate)


def extract_features(image: np.ndarray, mask: np.ndarray, 
                     plant_id: str = None, group: str = None) -> Dict:
    """
    Convenience function for feature extraction
    
    Args:
        image: BGR image
        mask: Binary mask
        plant_id: Plant ID
        group: Experimental group
        
    Returns:
        Feature dictionary
    """
    extractor = FeatureExtractor()
    return extractor.extract_all_features(image, mask, plant_id, group)


def features_to_dataframe(features_list: List[Dict]) -> pd.DataFrame:
    """
    Convert list of feature dictionaries to DataFrame
    
    Args:
        features_list: List of feature dictionaries
        
    Returns:
        pandas DataFrame
    """
    return pd.DataFrame(features_list)


if __name__ == "__main__":
    print("Feature Extraction Module")
    print("=" * 50)
    print("Available features:")
    print("  - Leaf Area (pixels)")
    print("  - Green Intensity (0-255)")
    print("  - Green Index (normalized)")
    print("  - Plant Height (pixels)")
    print("  - Plant Width (pixels)")
    print("  - Compactness (0-1)")
    print("  - Growth Rate (calculated from history)")
