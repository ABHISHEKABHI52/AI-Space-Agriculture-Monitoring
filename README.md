# AI-Based Autonomous Plant Health Monitoring System for Space Applications

## 🌱 Project Overview

An autonomous, low-cost system designed for space agriculture that analyzes plant images, detects early stress, monitors growth, and provides real-time health status through an interactive dashboard.

### Target Applications
- Space missions (future space farming)
- Closed environment agriculture
- Automated plant monitoring for space habitats
- Resource-optimized plant cultivation

## 🚀 ISRO Relevance

This system provides:
- **Autonomous plant monitoring** - Reduced astronaut workload
- **Early stress detection** - Proactive intervention
- **Water & energy optimization** - Critical for space missions
- **Scalable for space habitats** - Modular design
- **Real-time health tracking** - Continuous monitoring

## 📊 System Architecture

```
Plant Image → Image Processing → Feature Extraction → AI Model → Dashboard → Alert
```

### System Layers
1. **Input Layer**: Image upload / camera integration
2. **Processing Layer**: OpenCV-based analysis
3. **AI Layer**: Random Forest classification model
4. **Storage Layer**: CSV / database logging
5. **Interface Layer**: Streamlit dashboard

## 🔬 Experimental Setup

### Plant Groups
| Group | Condition |
|-------|-----------|
| Control | Normal water + light |
| Low Water | 50% water stress |
| Low Light | Reduced light exposure |

### Data Collection
- **Duration**: 10-15 days
- **Sample Size**: 10+ plants per group
- **Capture Frequency**: Every 6-12 hours
- **Conditions**: Same background, distance, lighting

## 🧠 AI Model

### Features Extracted
1. **Leaf Area**: Green pixel count
2. **Green Intensity**: Average green channel value
3. **Growth Rate**: Area change over time

### Classification Categories
- Healthy
- Water Stress
- Light Stress

### Model Performance
- Algorithm: Random Forest Classifier
- Expected Accuracy: >80%
- Confidence Score: Included

## 📁 Project Structure

```
plant-health-monitoring/
├── config/              # Configuration files
├── data/                # Raw and processed data
├── models/              # Trained models
├── notebooks/           # Jupyter notebooks for analysis
├── src/                 # Source code modules
├── app/                 # Streamlit dashboard
├── demo/                # Demo data and samples
├── reports/             # Results and documentation
├── docs/                # Technical documentation
└── tests/               # Unit tests
```

## 🛠️ Installation

### Requirements
- Python 3.8+
- OpenCV
- Scikit-learn
- Streamlit

### Setup
```bash
# Clone or navigate to project directory
cd AI-Plant-Healthy-Monitoring

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Run Demo Mode
```bash
streamlit run app/streamlit_app.py
```
Click "Run Demo" to see the system in action with sample data.

### 2. Train Model with Your Data
```bash
python src/models/train_model.py
```

### 3. Process New Images
```python
from src.processing.image_preprocessing import preprocess_image
from src.features.feature_extraction import extract_features
from src.models.predict import predict_health

# Process and predict
processed = preprocess_image("path/to/image.jpg")
features = extract_features(processed)
status = predict_health(features)
```

## 📈 Features

### Image Processing
- Automatic plant segmentation
- HSV color space analysis
- Noise reduction
- Background removal

### Health Monitoring
- Real-time status prediction
- Confidence scoring
- Growth trend analysis
- Historical data tracking

### Dashboard
- Image upload interface
- Side-by-side comparison (original vs processed)
- Live metrics display
- Growth graphs
- Alert system with recommendations

## 📊 Expected Outputs

1. Early stress detection (before visible symptoms)
2. Growth comparison across groups
3. Model accuracy >80%
4. Automated health dashboard
5. Historical data tracking and visualization

## 🔬 Experimental Design

### Data Collection Protocol
1. Germinate plants (chickpea/mustard/lettuce)
2. Assign to treatment groups
3. Capture images at regular intervals
4. Maintain consistent conditions
5. Log all observations

### Image Capture Guidelines
- Use consistent background (white/black)
- Maintain fixed distance from camera
- Ensure even lighting
- Capture at same time daily
- Name files systematically: `plantID_day_time.jpg`

## 📝 Project Timeline

| Week | Tasks |
|------|-------|
| Week 1 | Setup + Germination |
| Week 2 | Data collection |
| Week 3 | Image processing + Model training |
| Week 4 | Dashboard + Testing + Report |

## 🎯 Final Deliverables

- ✅ Complete dataset with labeled images
- ✅ Python codebase (modular and documented)
- ✅ Trained Random Forest model
- ✅ Interactive Streamlit dashboard
- ✅ Growth analysis graphs
- ✅ Technical report
- ✅ Presentation materials

## 📚 Documentation

Detailed documentation available in `docs/`:
- [System Architecture](docs/system_architecture.md)
- [Methodology](docs/methodology.md)
- [Experiment Design](docs/experiment_design.md)

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/
```

## 📄 License

This project is developed for research and educational purposes.

## 👥 Contributors

Autonomous Plant Health Monitoring System
For Space Agriculture Applications

---

**Note**: This system demonstrates the feasibility of autonomous plant monitoring for future space missions, addressing the critical need for resource-efficient agriculture in closed environments.
