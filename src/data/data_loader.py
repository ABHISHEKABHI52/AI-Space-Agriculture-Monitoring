"""
Data Loader Module
Handles loading and organizing image data
"""

import os
import glob
from typing import List, Dict, Tuple
import cv2
import numpy as np


class DataLoader:
    """
    Load and organize plant image data
    """
    
    def __init__(self, data_root: str = "data/raw"):
        """
        Initialize data loader
        
        Args:
            data_root: Root directory containing image data
        """
        self.data_root = data_root
        self.groups = ["control", "low_water", "low_light"]
        
    def get_group_directories(self) -> Dict[str, str]:
        """
        Get paths to group directories
        
        Returns:
            Dictionary mapping group names to paths
        """
        group_dirs = {}
        for group in self.groups:
            path = os.path.join(self.data_root, group)
            if os.path.exists(path):
                group_dirs[group] = path
        return group_dirs
    
    def load_images_from_group(self, group: str, 
                               extensions: List[str] = ['jpg', 'jpeg', 'png']) -> List[Dict]:
        """
        Load all images from a specific group
        
        Args:
            group: Group name (control, low_water, low_light)
            extensions: Valid image extensions
            
        Returns:
            List of dictionaries with image info
        """
        group_path = os.path.join(self.data_root, group)
        
        if not os.path.exists(group_path):
            print(f"Warning: Group directory not found: {group_path}")
            return []
        
        images_info = []
        
        for ext in extensions:
            pattern = os.path.join(group_path, f"*.{ext}")
            files = glob.glob(pattern)
            
            for file_path in files:
                filename = os.path.basename(file_path)
                
                images_info.append({
                    'path': file_path,
                    'filename': filename,
                    'group': group,
                    'exists': True
                })
        
        return images_info
    
    def load_all_images(self) -> Dict[str, List[Dict]]:
        """
        Load images from all groups
        
        Returns:
            Dictionary mapping group names to image info lists
        """
        all_images = {}
        
        for group in self.groups:
            images = self.load_images_from_group(group)
            if images:
                all_images[group] = images
                print(f"Loaded {len(images)} images from {group}")
        
        return all_images
    
    def parse_filename(self, filename: str) -> Dict:
        """
        Parse information from filename
        Expected format: plantID_day_time.jpg or similar
        
        Args:
            filename: Image filename
            
        Returns:
            Dictionary with parsed info
        """
        name = os.path.splitext(filename)[0]
        parts = name.split('_')
        
        info = {
            'filename': filename,
            'plant_id': parts[0] if len(parts) > 0 else 'unknown',
            'day': parts[1] if len(parts) > 1 else 'unknown',
            'time': parts[2] if len(parts) > 2 else 'unknown'
        }
        
        return info
    
    def get_statistics(self) -> Dict:
        """
        Get dataset statistics
        
        Returns:
            Dictionary with statistics
        """
        all_images = self.load_all_images()
        
        stats = {
            'total_images': sum(len(imgs) for imgs in all_images.values()),
            'groups': {},
            'group_names': list(all_images.keys())
        }
        
        for group, images in all_images.items():
            stats['groups'][group] = len(images)
        
        return stats


def load_data(data_root: str = "data/raw") -> Dict:
    """
    Convenience function to load all data
    
    Args:
        data_root: Root data directory
        
    Returns:
        Dictionary with all image information
    """
    loader = DataLoader(data_root)
    return loader.load_all_images()


if __name__ == "__main__":
    print("Data Loader Module")
    print("=" * 50)
    
    loader = DataLoader()
    stats = loader.get_statistics()
    
    print(f"\nDataset Statistics:")
    print(f"Total Images: {stats['total_images']}")
    print(f"\nImages per group:")
    for group, count in stats['groups'].items():
        print(f"  {group}: {count}")
