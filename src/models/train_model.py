"""
Model Training Module
Train Random Forest classifier for plant health prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns


class PlantHealthModel:
    """
    Random Forest model for plant health classification
    """
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 10, 
                 random_state: int = 42):
        """
        Initialize model
        
        Args:
            n_estimators: Number of trees
            max_depth: Maximum tree depth
            random_state: Random seed
        """
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        self.is_trained = False
        
    def prepare_data(self, df: pd.DataFrame, 
                    feature_cols: list = None, 
                    label_col: str = 'Label') -> tuple:
        """
        Prepare data for training
        
        Args:
            df: DataFrame with features and labels
            feature_cols: List of feature column names
            label_col: Name of label column
            
        Returns:
            (X, y) tuple
        """
        if feature_cols is None:
            feature_cols = ['Leaf_Area', 'Green_Index']
        
        self.feature_names = feature_cols
        
        X = df[feature_cols].values
        y = df[label_col].values
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        return X, y_encoded
    
    def train(self, X_train, y_train, X_test=None, y_test=None):
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_test: Test features (optional)
            y_test: Test labels (optional)
            
        Returns:
            Dictionary with training results
        """
        print("Training Random Forest model...")
        print(f"Training samples: {len(X_train)}")
        
        # Train model
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate on training set
        train_pred = self.model.predict(X_train)
        train_accuracy = accuracy_score(y_train, train_pred)
        
        results = {
            'train_accuracy': train_accuracy,
            'feature_importance': dict(zip(self.feature_names, self.model.feature_importances_))
        }
        
        print(f"Training Accuracy: {train_accuracy:.4f}")
        
        # Evaluate on test set if provided
        if X_test is not None and y_test is not None:
            test_pred = self.model.predict(X_test)
            test_accuracy = accuracy_score(y_test, test_pred)
            
            results['test_accuracy'] = test_accuracy
            results['test_predictions'] = test_pred
            results['test_labels'] = y_test
            
            print(f"Test Accuracy: {test_accuracy:.4f}")
            
            # Classification report
            class_names = self.label_encoder.classes_
            report = classification_report(y_test, test_pred, 
                                          target_names=class_names)
            results['classification_report'] = report
            print("\nClassification Report:")
            print(report)
            
            # Confusion matrix
            cm = confusion_matrix(y_test, test_pred)
            results['confusion_matrix'] = cm
        
        return results
    
    def cross_validate(self, X, y, cv: int = 5):
        """
        Perform cross-validation
        
        Args:
            X: Features
            y: Labels
            cv: Number of folds
            
        Returns:
            Cross-validation scores
        """
        print(f"Performing {cv}-fold cross-validation...")
        scores = cross_val_score(self.model, X, y, cv=cv, scoring='accuracy')
        
        print(f"CV Scores: {scores}")
        print(f"Mean CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
        
        return scores
    
    def predict(self, X):
        """
        Make predictions
        
        Args:
            X: Features
            
        Returns:
            Predicted labels
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        predictions = self.model.predict(X)
        return self.label_encoder.inverse_transform(predictions)
    
    def predict_proba(self, X):
        """
        Get prediction probabilities
        
        Args:
            X: Features
            
        Returns:
            Probability matrix
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        return self.model.predict_proba(X)
    
    def save_model(self, filepath: str = "models/trained/plant_model.pkl"):
        """
        Save trained model
        
        Args:
            filepath: Path to save model
        """
        if not self.is_trained:
            print("Warning: Saving untrained model")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"✅ Model saved to {filepath}")
    
    def load_model(self, filepath: str = "models/trained/plant_model.pkl"):
        """
        Load trained model
        
        Args:
            filepath: Path to model file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        print(f"✅ Model loaded from {filepath}")
    
    def plot_confusion_matrix(self, cm, save_path: str = None):
        """
        Plot confusion matrix
        
        Args:
            cm: Confusion matrix
            save_path: Path to save figure
        """
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.label_encoder.classes_,
                   yticklabels=self.label_encoder.classes_)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path)
            print(f"Confusion matrix saved to {save_path}")
        
        plt.close()


def train_model_from_csv(csv_file: str, 
                        feature_cols: list = None,
                        label_col: str = 'Label',
                        test_size: float = 0.2,
                        save_path: str = "models/trained/plant_model.pkl"):
    """
    Train model from CSV file
    
    Args:
        csv_file: Path to CSV with training data
        feature_cols: Feature column names
        label_col: Label column name
        test_size: Test set proportion
        save_path: Path to save trained model
        
    Returns:
        Trained model and results
    """
    if feature_cols is None:
        feature_cols = ['Leaf_Area', 'Green_Index']
    
    print("=" * 60)
    print("Plant Health Model Training")
    print("=" * 60)
    
    # Load data
    print(f"\n1. Loading data from {csv_file}")
    df = pd.read_csv(csv_file)
    print(f"   Loaded {len(df)} samples")
    print(f"   Features: {feature_cols}")
    print(f"   Classes: {df[label_col].unique()}")
    
    # Initialize model
    model = PlantHealthModel()
    
    # Prepare data
    print("\n2. Preparing data...")
    X, y = model.prepare_data(df, feature_cols, label_col)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    print(f"   Train set: {len(X_train)} samples")
    print(f"   Test set: {len(X_test)} samples")
    
    # Train model
    print("\n3. Training model...")
    results = model.train(X_train, y_train, X_test, y_test)
    
    # Save model
    print(f"\n4. Saving model to {save_path}")
    model.save_model(save_path)
    
    # Save confusion matrix
    if 'confusion_matrix' in results:
        cm_path = "reports/figures/confusion_matrix.png"
        model.plot_confusion_matrix(results['confusion_matrix'], cm_path)
    
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    
    return model, results


if __name__ == "__main__":
    # Example usage
    print("Model Training Module")
    print("=" * 60)
    
    # Check for training data
    csv_file = "data/plant_dataset.csv"
    
    if os.path.exists(csv_file):
        print(f"Found training data: {csv_file}")
        print("Run: python src/models/train_model.py to train")
    else:
        print(f"Training data not found: {csv_file}")
        print("\nCreate a CSV file with columns:")
        print("  - Leaf_Area")
        print("  - Green_Index")
        print("  - Label (Healthy, Water_Stress, Light_Stress)")
