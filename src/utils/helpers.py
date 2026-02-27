"""
Helper Functions
Utility functions for the plant health monitoring system
"""

import yaml
import os
from datetime import datetime
from typing import Dict, Any
import numpy as np
import cv2


def load_config(config_path: str = "config/config.yaml") -> Dict:
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    if not os.path.exists(config_path):
        print(f"Warning: Config file not found at {config_path}")
        return {}
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def ensure_directories_exist(directories: list):
    """
    Create directories if they don't exist
    
    Args:
        directories: List of directory paths
    """
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


def get_timestamp(format: str = "%Y%m%d_%H%M%S") -> str:
    """
    Get current timestamp as string
    
    Args:
        format: Timestamp format
        
    Returns:
        Formatted timestamp
    """
    return datetime.now().strftime(format)


def parse_plant_id(filename: str) -> str:
    """
    Extract plant ID from filename
    
    Args:
        filename: Image filename
        
    Returns:
        Plant ID
    """
    # Expected format: plantID_day_time.jpg
    name = os.path.splitext(os.path.basename(filename))[0]
    parts = name.split('_')
    return parts[0] if parts else 'unknown'


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    """
    Calculate percentage change between two values
    
    Args:
        old_value: Original value
        new_value: New value
        
    Returns:
        Percentage change
    """
    if old_value == 0:
        return 0.0
    
    change = ((new_value - old_value) / old_value) * 100
    return round(change, 2)


def resize_image_maintain_aspect(image: np.ndarray, 
                                 max_width: int = 800,
                                 max_height: int = 600) -> np.ndarray:
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: Input image
        max_width: Maximum width
        max_height: Maximum height
        
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    # Calculate aspect ratio
    aspect = width / height
    
    if width > max_width or height > max_height:
        if width / max_width > height / max_height:
            # Width is limiting factor
            new_width = max_width
            new_height = int(max_width / aspect)
        else:
            # Height is limiting factor
            new_height = max_height
            new_width = int(max_height * aspect)
        
        image = cv2.resize(image, (new_width, new_height))
    
    return image


def format_metric(value: float, metric_type: str = 'area') -> str:
    """
    Format metric value for display
    
    Args:
        value: Metric value
        metric_type: Type of metric
        
    Returns:
        Formatted string
    """
    if metric_type == 'area':
        return f"{int(value):,} px²"
    elif metric_type == 'index':
        return f"{value:.2f}"
    elif metric_type == 'percentage':
        return f"{value:.1f}%"
    elif metric_type == 'pixels':
        return f"{int(value)} px"
    else:
        return f"{value:.2f}"


def get_status_color(status: str) -> str:
    """
    Get color code for health status
    
    Args:
        status: Health status
        
    Returns:
        Color code (hex)
    """
    colors = {
        'Healthy': '#2ecc71',
        'Water_Stress': '#e74c3c',
        'Light_Stress': '#f39c12',
        'Unknown': '#95a5a6'
    }
    
    return colors.get(status, colors['Unknown'])


def get_status_emoji(status: str) -> str:
    """
    Get emoji for health status
    
    Args:
        status: Health status
        
    Returns:
        Emoji string
    """
    emojis = {
        'Healthy': '✅',
        'Water_Stress': '💧',
        'Light_Stress': '☀️',
        'Unknown': '❓'
    }
    
    return emojis.get(status, emojis['Unknown'])


def validate_image(image_path: str) -> bool:
    """
    Validate if file is a valid image
    
    Args:
        image_path: Path to image file
        
    Returns:
        True if valid image
    """
    if not os.path.exists(image_path):
        return False
    
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    ext = os.path.splitext(image_path)[1].lower()
    
    if ext not in valid_extensions:
        return False
    
    # Try to read image
    try:
        image = cv2.imread(image_path)
        return image is not None
    except:
        return False


def create_project_structure():
    """
    Create complete project directory structure
    """
    directories = [
        "data/raw/control",
        "data/raw/low_water",
        "data/raw/low_light",
        "data/processed",
        "data/features",
        "models/trained",
        "models/training_logs",
        "reports/figures",
        "reports/results",
        "demo/sample_images",
        "notebooks"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ Project structure created successfully")


def print_summary_table(data: Dict[str, Any], title: str = "Summary"):
    """
    Print formatted summary table
    
    Args:
        data: Dictionary with data to display
        title: Table title
    """
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)
    
    for key, value in data.items():
        key_formatted = key.replace('_', ' ').title()
        print(f"{key_formatted:<30} : {value}")
    
    print("=" * 60 + "\n")


if __name__ == "__main__":
    print("Helper Functions Module")
    print("=" * 60)
    print("Available utilities:")
    print("  ✓ Configuration loading")
    print("  ✓ Directory management")
    print("  ✓ Timestamp formatting")
    print("  ✓ Image validation")
    print("  ✓ Metric formatting")
    print("  ✓ Status color/emoji mapping")
