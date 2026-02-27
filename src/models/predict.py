"""
Prediction Module
Load trained model and make predictions on new data
"""

import joblib
import numpy as np
from typing import Dict, Tuple, List
import os


class PlantHealthPredictor:
    """
    Make predictions using trained model
    """
    
    def __init__(self, model_path: str = "models/trained/plant_model.pkl"):
        """
        Initialize predictor
        
        Args:
            model_path: Path to trained model file
        """
        self.model_path = model_path
        self.model = None
        self.label_encoder = None
        self.feature_names = None
        self.is_loaded = False
        
        # Try to load model
        if os.path.exists(model_path):
            self.load_model()
    
    def load_model(self, model_path: str = None):
        """
        Load trained model
        
        Args:
            model_path: Path to model file
        """
        if model_path is None:
            model_path = self.model_path
        
        if not os.path.exists(model_path):
            print(f"⚠️ Model file not found: {model_path}")
            self.is_loaded = False
            return False
        
        try:
            model_data = joblib.load(model_path)
            
            self.model = model_data['model']
            self.label_encoder = model_data['label_encoder']
            self.feature_names = model_data.get('feature_names', ['Leaf_Area', 'Green_Index'])
            self.is_loaded = True
            
            print(f"✅ Model loaded successfully")
            print(f"   Features: {self.feature_names}")
            print(f"   Classes: {self.label_encoder.classes_}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_loaded = False
            return False
    
    def predict(self, leaf_area: float, green_index: float) -> Tuple[str, float]:
        """
        Predict plant health status
        
        Args:
            leaf_area: Leaf area in pixels
            green_index: Green index value
            
        Returns:
            (predicted_status, confidence) tuple
        """
        if not self.is_loaded:
            return self._fallback_prediction(leaf_area, green_index)
        
        # Prepare input
        X = np.array([[leaf_area, green_index]])
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        status = self.label_encoder.inverse_transform([prediction])[0]
        
        # Get confidence
        probabilities = self.model.predict_proba(X)[0]
        confidence = float(np.max(probabilities) * 100)
        
        return status, confidence
    
    def predict_batch(self, leaf_areas: List[float], 
                     green_indices: List[float]) -> List[Tuple[str, float]]:
        """
        Predict multiple samples
        
        Args:
            leaf_areas: List of leaf areas
            green_indices: List of green indices
            
        Returns:
            List of (status, confidence) tuples
        """
        if not self.is_loaded:
            return [self._fallback_prediction(area, gi) 
                   for area, gi in zip(leaf_areas, green_indices)]
        
        # Prepare input
        X = np.column_stack([leaf_areas, green_indices])
        
        # Make predictions
        predictions = self.model.predict(X)
        statuses = self.label_encoder.inverse_transform(predictions)
        
        # Get confidences
        probabilities = self.model.predict_proba(X)
        confidences = np.max(probabilities, axis=1) * 100
        
        return list(zip(statuses, confidences))
    
    def predict_with_details(self, leaf_area: float, 
                            green_index: float) -> Dict:
        """
        Predict with detailed probability breakdown
        
        Args:
            leaf_area: Leaf area
            green_index: Green index
            
        Returns:
            Dictionary with prediction details
        """
        if not self.is_loaded:
            status, confidence = self._fallback_prediction(leaf_area, green_index)
            return {
                'status': status,
                'confidence': confidence,
                'probabilities': {},
                'method': 'rule_based'
            }
        
        # Prepare input
        X = np.array([[leaf_area, green_index]])
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        status = self.label_encoder.inverse_transform([prediction])[0]
        
        # Get all probabilities
        probabilities = self.model.predict_proba(X)[0]
        confidence = float(np.max(probabilities) * 100)
        
        # Create probability dictionary
        prob_dict = {}
        for class_name, prob in zip(self.label_encoder.classes_, probabilities):
            prob_dict[class_name] = float(prob * 100)
        
        return {
            'status': status,
            'confidence': confidence,
            'probabilities': prob_dict,
            'features': {
                'leaf_area': leaf_area,
                'green_index': green_index
            },
            'method': 'ml_model'
        }
    
    def _fallback_prediction(self, leaf_area: float, 
                            green_index: float) -> Tuple[str, float]:
        """
        Rule-based prediction when model not available
        
        Args:
            leaf_area: Leaf area
            green_index: Green index
            
        Returns:
            (status, confidence) tuple
        """
        # Simple rule-based classification
        if leaf_area >= 20000 and green_index >= 100:
            return "Healthy", 85.0
        elif leaf_area < 12000 and green_index < 85:
            return "Water_Stress", 75.0
        elif green_index < 75:
            return "Light_Stress", 70.0
        elif leaf_area < 15000:
            return "Water_Stress", 70.0
        else:
            return "Healthy", 65.0
    
    def get_recommendation(self, status: str) -> str:
        """
        Get care recommendation based on status
        
        Args:
            status: Predicted status
            
        Returns:
            Recommendation text
        """
        recommendations = {
            'Healthy': "✅ Plant is healthy! Continue current care routine.",
            'Water_Stress': "⚠️ Water Stress Detected! Recommendation: Increase watering frequency and check soil moisture.",
            'Light_Stress': "⚠️ Light Stress Detected! Recommendation: Increase light exposure or move plant to brighter location."
        }
        
        return recommendations.get(status, "Monitor plant condition regularly.")


def predict_health(leaf_area: float, green_index: float, 
                  model_path: str = "models/trained/plant_model.pkl") -> Dict:
    """
    Convenience function for health prediction
    
    Args:
        leaf_area: Leaf area
        green_index: Green index
        model_path: Path to model
        
    Returns:
        Prediction dictionary
    """
    predictor = PlantHealthPredictor(model_path)
    result = predictor.predict_with_details(leaf_area, green_index)
    result['recommendation'] = predictor.get_recommendation(result['status'])
    
    return result


if __name__ == "__main__":
    print("Plant Health Prediction Module")
    print("=" * 60)
    
    # Test prediction
    predictor = PlantHealthPredictor()
    
    if predictor.is_loaded:
        print("\n✅ Model loaded successfully")
        
        # Test cases
        test_cases = [
            (25000, 120, "Healthy plant"),
            (9000, 85, "Water stressed plant"),
            (15000, 70, "Light stressed plant")
        ]
        
        print("\nTest Predictions:")
        print("-" * 60)
        
        for area, gi, description in test_cases:
            result = predictor.predict_with_details(area, gi)
            print(f"\n{description}:")
            print(f"  Leaf Area: {area}, Green Index: {gi}")
            print(f"  Status: {result['status']}")
            print(f"  Confidence: {result['confidence']:.2f}%")
            print(f"  {predictor.get_recommendation(result['status'])}")
    
    else:
        print("\n⚠️ Model not loaded - using rule-based prediction")
        print("Train a model first using: python src/models/train_model.py")
