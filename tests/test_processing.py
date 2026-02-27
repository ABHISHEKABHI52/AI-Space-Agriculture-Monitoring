"""
Test Image Processing Module
Unit tests for image preprocessing functions
"""

import unittest
import numpy as np
import cv2
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.processing.image_preprocessing import ImagePreprocessor, preprocess_image
from src.processing.plant_segmentation import PlantSegmenter


class TestImagePreprocessor(unittest.TestCase):
    """Test image preprocessing functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.preprocessor = ImagePreprocessor(target_size=(640, 480))
        
        # Create a simple test image (green square on white background)
        self.test_image = np.ones((480, 640, 3), dtype=np.uint8) * 255
        # Add green square in center
        self.test_image[200:280, 270:370] = [0, 255, 0]  # BGR green
    
    def test_resize_image(self):
        """Test image resizing"""
        large_image = np.ones((1000, 1200, 3), dtype=np.uint8)
        resized = self.preprocessor.resize_image(large_image)
        
        self.assertEqual(resized.shape, (480, 640, 3))
    
    def test_convert_to_hsv(self):
        """Test BGR to HSV conversion"""
        hsv = self.preprocessor.convert_to_hsv(self.test_image)
        
        self.assertEqual(hsv.shape, self.test_image.shape)
        self.assertEqual(len(hsv.shape), 3)
    
    def test_create_green_mask(self):
        """Test green color mask creation"""
        hsv = self.preprocessor.convert_to_hsv(self.test_image)
        mask = self.preprocessor.create_green_mask(hsv)
        
        # Mask should be binary
        unique_values = np.unique(mask)
        self.assertTrue(np.all(np.isin(unique_values, [0, 255])))
        
        # Some pixels should be detected as green
        self.assertGreater(np.count_nonzero(mask), 0)
    
    def test_remove_noise(self):
        """Test noise removal"""
        # Create noisy mask
        mask = np.zeros((480, 640), dtype=np.uint8)
        mask[200:280, 270:370] = 255
        # Add noise
        mask[50, 50] = 255
        mask[100, 100] = 255
        
        cleaned = self.preprocessor.remove_noise(mask, kernel_size=5)
        
        # Noise should be reduced
        self.assertLessEqual(np.count_nonzero(cleaned), np.count_nonzero(mask))
    
    def test_extract_plant_region(self):
        """Test plant region extraction"""
        mask = np.zeros((480, 640), dtype=np.uint8)
        mask[200:280, 270:370] = 255
        
        extracted = self.preprocessor.extract_plant_region(self.test_image, mask)
        
        self.assertEqual(extracted.shape, self.test_image.shape)
        
        # Outside mask should be black
        self.assertTrue(np.all(extracted[0, 0] == [0, 0, 0]))


class TestPlantSegmenter(unittest.TestCase):
    """Test plant segmentation functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.segmenter = PlantSegmenter(min_contour_area=1000)
        
        # Create test mask with plant region
        self.test_mask = np.zeros((480, 640), dtype=np.uint8)
        cv2.circle(self.test_mask, (320, 240), 50, 255, -1)
    
    def test_find_plant_contours(self):
        """Test contour detection"""
        contours = self.segmenter.find_plant_contours(self.test_mask)
        
        self.assertGreater(len(contours), 0)
    
    def test_get_largest_contour(self):
        """Test largest contour selection"""
        contours = self.segmenter.find_plant_contours(self.test_mask)
        largest = self.segmenter.get_largest_contour(contours)
        
        self.assertIsNotNone(largest)
    
    def test_get_bounding_box(self):
        """Test bounding box calculation"""
        contours = self.segmenter.find_plant_contours(self.test_mask)
        largest = self.segmenter.get_largest_contour(contours)
        bbox = self.segmenter.get_bounding_box(largest)
        
        self.assertEqual(len(bbox), 4)  # x, y, width, height
        self.assertGreater(bbox[2], 0)  # width > 0
        self.assertGreater(bbox[3], 0)  # height > 0


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestImagePreprocessor))
    suite.addTests(loader.loadTestsFromTestCase(TestPlantSegmenter))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
