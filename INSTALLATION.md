# Installation and Usage Guide

## Complete Setup Instructions

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB for installation + space for data
- **Camera** (optional): For direct image capture

### Step-by-Step Installation

#### 1. Verify Python Installation

Open terminal/command prompt and check:

```bash
python --version
```

Should show Python 3.8 or higher. If not installed, download from [python.org](https://www.python.org/downloads/)

#### 2. Navigate to Project Directory

```bash
cd C:\Users\abhis\AI-Plant-Healthy-Monitoring
```

#### 3. Install Required Packages

**Option A: Automated Setup (Windows)**
```powershell
.\setup.ps1
```

**Option B: Manual Installation**
```bash
pip install -r requirements.txt
```

This installs:
- opencv-python (image processing)
- numpy (numerical operations)
- pandas (data handling)
- scikit-learn (machine learning)
- streamlit (web dashboard)
- matplotlib, seaborn, plotly (visualization)
- joblib (model persistence)
- PyYAML (configuration)

#### 4. Verify Installation

```bash
python -c "import cv2, sklearn, streamlit, pandas; print('✅ All packages installed!')"
```

### Quick Start (First Time Users)

#### Option 1: Run Demo Mode (Fastest)

1. **Start Dashboard**
   ```bash
   python run_dashboard.py
   ```

2. **Access Dashboard**
   - Browser opens automatically at `http://localhost:8501`
   - If not, manually open that URL

3. **Try Demo**
   - Select "Run Demo" from sidebar
   - Click "▶️ Run Demo Analysis"
   - See instant results with sample data

#### Option 2: Train and Use Your Model

1. **Train the Model**
   ```bash
   python train_model.py
   ```
   
   This uses the included sample dataset (`data/plant_dataset.csv`) to train a Random Forest classifier.

2. **Start Dashboard**
   ```bash
   python run_dashboard.py
   ```

3. **Upload Image**
   - Select "Upload & Analyze"
   - Choose a plant image
   - View instant analysis

### Detailed Usage

#### Understanding the System

The system consists of several components working together:

1. **Image Processing**: Removes background, isolates plant
2. **Feature Extraction**: Calculates leaf area, green index
3. **AI Prediction**: Classifies health using trained model
4. **Dashboard**: Displays results and recommendations

#### Using the Dashboard

##### Main Modes

1. **Upload & Analyze**
   - Upload plant images
   - Get instant health analysis
   - Save results to history

2. **Run Demo**
   - Pre-loaded sample analysis
   - Perfect for demonstrations
   - No data required

3. **View History**
   - See past measurements
   - View growth trends
   - Compare plants over time

4. **About**
   - System information
   - Technical details
   - ISRO relevance

##### Sidebar Controls

- **Plant ID**: Identifier for tracking (e.g., P001)
- **Experimental Group**: 
  - Control (normal conditions)
  - Low_Water (water stress)
  - Low_Light (light stress)

#### Collecting Your Own Data

##### Equipment Needed

- Camera (smartphone OK)
- Uniform background (white paper/cloth)
- Consistent lighting
- Ruler/scale (optional, for validation)

##### Image Capture Guidelines

✅ **DO:**
- Use uniform background (white or black)
- Maintain consistent distance (30-40 cm)
- Capture in good lighting
- Keep plant centered
- Take top-down view
- Use consistent time of day

❌ **DON'T:**
- Use flash
- Capture with shadows
- Change background mid-experiment
- Vary camera distance
- Include multiple plants

##### File Organization

Place images in appropriate folders:

```
data/raw/control/       ← Healthy plants
data/raw/low_water/     ← Water stressed
data/raw/low_light/     ← Light stressed
```

**Naming Convention:**
```
plantID_day_time.jpg

Examples:
C01_day1_morning.jpg
W05_day7_evening.jpg
L03_day10_morning.jpg
```

#### Training Your Own Model

##### 1. Prepare Training Data

Create `data/plant_dataset.csv` with this format:

```csv
Leaf_Area,Green_Index,Label
25430,121.5,Healthy
9120,86.3,Water_Stress
15230,71.2,Light_Stress
...
```

**Minimum Requirements:**
- 30+ samples per class
- 50+ samples = OK
- 100+ samples = Good
- 150+ samples = Excellent

##### 2. Run Training

```bash
python train_model.py
```

##### 3. Review Results

Look for:
- Training accuracy: >80% (target)
- Test accuracy: >75% (minimum)
- Confusion matrix: saved in `reports/figures/`

##### 4. Use Trained Model

Model automatically saved to: `models/trained/plant_model.pkl`

Dashboard automatically loads this model.

#### Processing Images in Batch

For processing multiple images at once:

```python
from src.processing.image_preprocessing import ImagePreprocessor
from src.features.feature_extraction import FeatureExtractor
import os

# Initialize
preprocessor = ImagePreprocessor()
extractor = FeatureExtractor()

# Process all images in folder
image_folder = "data/raw/control"
for image_file in os.listdir(image_folder):
    if image_file.endswith('.jpg'):
        path = os.path.join(image_folder, image_file)
        
        # Preprocess
        original, mask, extracted = preprocessor.preprocess(path)
        
        # Extract features
        features = extractor.extract_all_features(original, mask)
        
        print(f"{image_file}: Area={features['leaf_area']}, GI={features['green_index']:.2f}")
```

#### Tracking Growth Over Time

##### 1. Regular Measurements

Capture images at consistent intervals (e.g., every 12 hours)

##### 2. Log Data

After each analysis, click "💾 Save Results to History"

##### 3. View Trends

Go to "View History" mode to see:
- Growth curves
- Health status changes
- Group comparisons

#### Customizing the System

##### Adjust Detection Thresholds

Edit `config/config.yaml`:

```yaml
classification:
  healthy_area_min: 20000      # Adjust based on your plants
  healthy_green_min: 100
  water_stress_area_max: 12000
  water_stress_green_max: 85
```

##### Modify Image Processing

Edit `src/processing/image_preprocessing.py`:

```python
# Adjust HSV color range for green detection
self.hsv_lower = np.array([35, 40, 40])   # Lower bound
self.hsv_upper = np.array([85, 255, 255]) # Upper bound
```

##### Change Model Parameters

Edit `src/models/train_model.py`:

```python
model = RandomForestClassifier(
    n_estimators=150,     # More trees = better (slower)
    max_depth=15,         # Deeper = more complex
    random_state=42
)
```

### Troubleshooting

#### Common Issues

##### 1. "Module not found" Error

**Problem**: Required package not installed

**Solution**:
```bash
pip install -r requirements.txt
```

##### 2. "Model file not found"

**Problem**: Model hasn't been trained

**Solution**:
```bash
python train_model.py
```

##### 3. Dashboard Won't Start

**Problem**: Streamlit not properly installed

**Solution**:
```bash
pip install --upgrade streamlit
streamlit --version
```

##### 4. Low Prediction Accuracy

**Problem**: Insufficient or poor training data

**Solutions**:
- Collect more samples (100+ per class)
- Ensure consistent image quality
- Verify labels are correct
- Check images show clear plant features

##### 5. Image Processing Fails

**Problem**: Image format or quality issues

**Solutions**:
- Convert to JPG format
- Ensure good lighting
- Check image isn't corrupted
- Try different image

##### 6. Can't Save to History

**Problem**: File permissions or path issues

**Solutions**:
- Check write permissions
- Verify `data/` folder exists
- Run as administrator (Windows)

### Running Tests

Verify system components:

```bash
# Test image processing
python tests/test_processing.py

# Test ML model
python tests/test_model.py
```

### Performance Optimization

#### For Faster Processing

1. **Reduce Image Size**
   Edit `config/config.yaml`:
   ```yaml
   image_processing:
     target_size: [480, 360]  # Smaller = faster
   ```

2. **Use Fewer Trees**
   ```python
   n_estimators=50  # Instead of 100
   ```

3. **Process in Batches**
   Process multiple images offline, then view in dashboard

#### For Better Accuracy

1. **More Training Data**
   - Minimum 100 samples per class
   - Diverse examples

2. **More Features**
   Add height, width, compactness to training

3. **More Trees**
   ```python
   n_estimators=200
   ```

### Advanced Usage

#### Export Results

Results saved to: `data/plant_records.csv`

Load in Excel/Python for further analysis:

```python
import pandas as pd
df = pd.read_csv('data/plant_records.csv')
print(df.describe())
```

#### Integrate with Other Systems

```python
from src.models.predict import predict_health

# Use in your own code
result = predict_health(leaf_area=25000, green_index=120)
print(result['status'])
print(result['confidence'])
```

#### Deploy Online

For remote access, deploy to cloud:

```bash
# Example: Deploy to Streamlit Cloud
# 1. Push code to GitHub
# 2. Connect to Streamlit Cloud
# 3. Deploy with requirements.txt
```

### Best Practices

#### Data Collection

- ✅ Capture at same time daily
- ✅ Use same background
- ✅ Maintain consistent distance
- ✅ Document all conditions
- ✅ Take multiple photos if uncertain

#### Model Training

- ✅ Balance classes (equal samples)
- ✅ Validate on test set
- ✅ Use cross-validation
- ✅ Save training logs
- ✅ Version your models

#### System Usage

- ✅ Save all results
- ✅ Review history regularly
- ✅ Act on recommendations
- ✅ Document observations
- ✅ Update model with new data

### Getting Help

#### Documentation

- [README.md](README.md) - Project overview
- [QUICKSTART.md](QUICKSTART.md) - Quick guide
- [docs/system_architecture.md](docs/system_architecture.md) - Technical details
- [docs/methodology.md](docs/methodology.md) - Scientific approach
- [docs/experiment_design.md](docs/experiment_design.md) - Experimental protocol

#### Code Comments

All code is well-commented. Read the source files for detailed explanations.

#### Community

- Check GitHub issues
- Review example notebooks
- Examine test files for usage examples

### Project Maintenance

#### Regular Updates

```bash
# Update packages
pip install --upgrade -r requirements.txt

# Retrain model with new data
python train_model.py

# Clear old logs
# (manually delete old entries from plant_records.csv)
```

#### Backup

Important files to backup:
- `data/plant_records.csv` (your data)
- `models/trained/*.pkl` (trained models)
- `data/raw/` (original images)

### Conclusion

You now have everything needed to:
- ✅ Set up the system
- ✅ Collect plant data
- ✅ Train ML models
- ✅ Monitor plant health
- ✅ Track growth over time
- ✅ Make data-driven decisions

**For quick demo**: Just run `python run_dashboard.py` and select "Run Demo"!

**For full experiment**: Follow the [Experiment Design](docs/experiment_design.md) guide.

---

**Questions?** Review the documentation or examine the code - it's all open source!

**Ready for ISRO demo?** The system is production-ready. Use demo mode for presentations!

🌱 Happy plant monitoring! 🚀
