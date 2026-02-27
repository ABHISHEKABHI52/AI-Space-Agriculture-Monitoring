# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

This guide will help you get the Plant Health Monitoring System up and running quickly.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Basic command line knowledge

## Step 1: Installation (2 minutes)

### Clone or Navigate to Project
```bash
cd C:\Users\abhis\AI-Plant-Healthy-Monitoring
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- OpenCV (image processing)
- Scikit-learn (machine learning)
- Streamlit (dashboard)
- Pandas, Matplotlib (data handling and visualization)

## Step 2: Train the Model (1 minute)

The project includes sample training data. Train your first model:

```bash
python train_model.py
```

Expected output:
```
✅ Training Completed Successfully!
📊 Final Results:
   Training Accuracy: 95.00%
   Test Accuracy: 92.50%
💾 Model saved to: models/trained/plant_model.pkl
```

## Step 3: Launch Dashboard (1 minute)

Start the web dashboard:

```bash
python run_dashboard.py
```

Or directly with Streamlit:
```bash
streamlit run app/streamlit_app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

## Step 4: Try it Out! (1 minute)

### Option A: Run Demo Mode
1. In the sidebar, select **"Run Demo"**
2. Click **"▶️ Run Demo Analysis"**
3. See the system analyze sample plants

### Option B: Upload Your Own Image
1. Select **"Upload & Analyze"** mode
2. Click **"Browse files"**
3. Upload a plant image
4. View instant analysis results!

## Understanding the Dashboard

### Sidebar Controls
- **Select Mode**: Choose between upload, demo, history, or about
- **Plant ID**: Identifier for tracking
- **Experimental Group**: Control, Low Water, or Low Light

### Main Panel
- **Image Display**: Original vs processed comparison
- **Health Metrics**: Leaf area, green index, dimensions
- **Prediction**: AI health status with confidence score
- **Recommendations**: Actionable care suggestions

## Next Steps

### Add Your Own Data

#### 1. Capture Plant Images
- Use consistent background
- Maintain fixed distance
- Ensure good lighting
- Name files: `plantID_day_time.jpg`

#### 2. Organize Images
Place images in appropriate folders:
```
data/raw/control/       # Healthy plants
data/raw/low_water/     # Water stressed plants
data/raw/low_light/     # Light stressed plants
```

#### 3. Process and Train
Once you have enough images (30+ per group):
```bash
python train_model.py
```

### Customize the System

#### Adjust Detection Thresholds
Edit `config/config.yaml`:
```yaml
classification:
  healthy_area_min: 20000
  healthy_green_min: 100
```

#### Modify Model Parameters
Edit `src/models/train_model.py`:
```python
model = RandomForestClassifier(
    n_estimators=150,  # More trees
    max_depth=15       # Deeper trees
)
```

## Common Issues & Solutions

### Issue: "Module not found"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: "Model file not found"
**Solution**: Train the model first
```bash
python train_model.py
```

### Issue: Dashboard won't open
**Solution**: Check if Streamlit is installed
```bash
pip install streamlit
streamlit --version
```

### Issue: Poor prediction accuracy
**Solution**:
1. Collect more training data (100+ samples)
2. Ensure consistent image quality
3. Check data labels are correct

## File Structure Quick Reference

```
project/
├── app/                    # Dashboard application
│   ├── streamlit_app.py   # Main dashboard
│   └── components/        # UI components
├── src/                   # Source code
│   ├── models/           # ML models
│   ├── processing/       # Image processing
│   └── features/         # Feature extraction
├── data/                 # Data storage
│   ├── raw/             # Original images
│   └── plant_dataset.csv # Training data
├── models/              # Trained models
└── train_model.py       # Training script
```

## Commands Cheat Sheet

| Task | Command |
|------|---------|
| Install dependencies | `pip install -r requirements.txt` |
| Train model | `python train_model.py` |
| Run dashboard | `python run_dashboard.py` |
| Run tests | `python -m pytest tests/` |
| Process images | `python src/processing/image_preprocessing.py` |

## Tips for Best Results

1. **Image Quality**
   - ✅ Use uniform background
   - ✅ Good lighting
   - ✅ Clear focus
   - ❌ Avoid shadows
   - ❌ Don't use flash

2. **Data Collection**
   - Minimum 10 plants per group
   - Capture every 12 hours
   - 10-15 day duration
   - Consistent conditions

3. **Model Training**
   - More data = better accuracy
   - Balance classes (equal samples)
   - Validate on test set

## Getting Help

### Documentation
- [System Architecture](docs/system_architecture.md)
- [Methodology](docs/methodology.md)
- [Experiment Design](docs/experiment_design.md)

### Check System Status
```bash
python -c "import cv2, sklearn, streamlit; print('All modules OK!')"
```

### Run Tests
```bash
python tests/test_processing.py
python tests/test_model.py
```

## What's Next?

After mastering the basics:

1. **Experiment Design**: Read `docs/experiment_design.md`
2. **Custom Features**: Add new measurements
3. **Advanced Models**: Try other algorithms
4. **Deployment**: Host on cloud for remote access

## Quick Demo Script

Want to see everything in action? Run this:

```bash
# 1. Train model
python train_model.py

# 2. Start dashboard
python run_dashboard.py

# 3. In browser: Click "Run Demo"
```

Done! You should see the system analyze sample plants automatically.

## Success Checklist

- ✅ Installed all dependencies
- ✅ Trained the model successfully
- ✅ Dashboard opens in browser
- ✅ Can analyze images
- ✅ Understand the results

Congratulations! You're ready to monitor plant health like a pro! 🌱🚀

---

**Questions?** Check the full documentation in the `docs/` folder or review the code comments.

**Ready for ISRO Demo?** Use the "Run Demo" mode - it's pre-loaded with impressive results!
