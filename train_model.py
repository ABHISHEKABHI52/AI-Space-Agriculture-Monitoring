"""
Training Script
Convenience script to train the model from command line
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.train_model import train_model_from_csv


def main():
    """Main training function"""
    print("=" * 70)
    print(" " * 15 + "🌱 Plant Health Model Training 🌱")
    print("=" * 70)
    
    # Check for training data
    csv_file = "data/plant_dataset.csv"
    
    if not os.path.exists(csv_file):
        print(f"\n❌ Training data not found: {csv_file}")
        print("\nPlease create a dataset with the following format:")
        print("  Columns: Leaf_Area, Green_Index, Label")
        print("  Labels: Healthy, Water_Stress, Light_Stress")
        print("\nExample data is provided in demo/demo_data.csv")
        return 1
    
    # Train model
    try:
        model, results = train_model_from_csv(
            csv_file=csv_file,
            feature_cols=['Leaf_Area', 'Green_Index'],
            label_col='Label',
            test_size=0.2,
            save_path='models/trained/plant_model.pkl'
        )
        
        print("\n" + "=" * 70)
        print("✅ Training Completed Successfully!")
        print("=" * 70)
        print(f"\n📊 Final Results:")
        print(f"   Training Accuracy: {results['train_accuracy']:.2%}")
        if 'test_accuracy' in results:
            print(f"   Test Accuracy: {results['test_accuracy']:.2%}")
        
        print(f"\n💾 Model saved to: models/trained/plant_model.pkl")
        print(f"\n🚀 Ready to use! Start dashboard with:")
        print("   streamlit run app/streamlit_app.py")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
