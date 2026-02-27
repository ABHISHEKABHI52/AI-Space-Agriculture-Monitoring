"""
Test Model Module
Unit tests for machine learning model
"""

import unittest
import numpy as np
import pandas as pd
import sys
import os
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.train_model import PlantHealthModel
from src.models.predict import PlantHealthPredictor


class TestPlantHealthModel(unittest.TestCase):
    """Test model training functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.model = PlantHealthModel(n_estimators=10, max_depth=5, random_state=42)
        
        # Create synthetic training data
        np.random.seed(42)
        n_samples = 100
        
        # Healthy: high area, high green
        healthy_area = np.random.normal(25000, 2000, n_samples // 3)
        healthy_green = np.random.normal(120, 10, n_samples // 3)
        
        # Water stress: low area, low green
        water_area = np.random.normal(9000, 1000, n_samples // 3)
        water_green = np.random.normal(85, 5, n_samples // 3)
        
        # Light stress: medium area, low green
        light_area = np.random.normal(15000, 1500, n_samples // 3)
        light_green = np.random.normal(70, 5, n_samples // 3)
        
        # Combine data
        X = np.column_stack([
            np.concatenate([healthy_area, water_area, light_area]),
            np.concatenate([healthy_green, water_green, light_green])
        ])
        
        y = np.array(['Healthy'] * (n_samples // 3) + 
                    ['Water_Stress'] * (n_samples // 3) + 
                    ['Light_Stress'] * (n_samples // 3))
        
        # Create DataFrame
        self.df = pd.DataFrame({
            'Leaf_Area': X[:, 0],
            'Green_Index': X[:, 1],
            'Label': y
        })
        
        self.X, self.y = self.model.prepare_data(self.df)
    
    def test_prepare_data(self):
        """Test data preparation"""
        self.assertEqual(len(self.X), len(self.df))
        self.assertEqual(len(self.y), len(self.df))
        self.assertEqual(self.X.shape[1], 2)  # 2 features
    
    def test_train(self):
        """Test model training"""
        results = self.model.train(self.X, self.y)
        
        self.assertIn('train_accuracy', results)
        self.assertIn('feature_importance', results)
        self.assertGreater(results['train_accuracy'], 0.5)
        self.assertTrue(self.model.is_trained)
    
    def test_predict(self):
        """Test prediction"""
        # Train first
        self.model.train(self.X, self.y)
        
        # Test prediction
        test_X = np.array([[25000, 120]])  # Healthy plant
        prediction = self.model.predict(test_X)
        
        self.assertEqual(len(prediction), 1)
        self.assertIn(prediction[0], ['Healthy', 'Water_Stress', 'Light_Stress'])
    
    def test_predict_proba(self):
        """Test probability prediction"""
        self.model.train(self.X, self.y)
        
        test_X = np.array([[25000, 120]])
        probabilities = self.model.predict_proba(test_X)
        
        self.assertEqual(probabilities.shape, (1, 3))  # 1 sample, 3 classes
        self.assertAlmostEqual(np.sum(probabilities), 1.0, places=5)


class TestPlantHealthPredictor(unittest.TestCase):
    """Test prediction functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.predictor = PlantHealthPredictor()
    
    def test_fallback_prediction(self):
        """Test rule-based fallback prediction"""
        # Healthy
        status, conf = self.predictor._fallback_prediction(25000, 120)
        self.assertEqual(status, "Healthy")
        self.assertGreater(conf, 0)
        
        # Water stress
        status, conf = self.predictor._fallback_prediction(9000, 80)
        self.assertEqual(status, "Water_Stress")
        
        # Light stress
        status, conf = self.predictor._fallback_prediction(15000, 70)
        self.assertEqual(status, "Light_Stress")
    
    def test_get_recommendation(self):
        """Test recommendation generation"""
        healthy_rec = self.predictor.get_recommendation('Healthy')
        self.assertIn('healthy', healthy_rec.lower())
        
        water_rec = self.predictor.get_recommendation('Water_Stress')
        self.assertIn('water', water_rec.lower())
        
        light_rec = self.predictor.get_recommendation('Light_Stress')
        self.assertIn('light', light_rec.lower())


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPlantHealthModel))
    suite.addTests(loader.loadTestsFromTestCase(TestPlantHealthPredictor))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
