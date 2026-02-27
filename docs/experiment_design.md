# Experiment Design

## Objective

Develop and validate an AI-based autonomous plant health monitoring system capable of:
1. Early stress detection
2. Growth tracking
3. Automated health classification
4. Real-time recommendations

## Hypothesis

**H1**: Machine learning models can accurately classify plant health status (Healthy, Water Stress, Light Stress) based on image-derived features (leaf area and green index) with >80% accuracy.

**H2**: Water and light stress will manifest as measurable changes in leaf area and green coloration before visible wilting occurs.

## Experimental Variables

### Independent Variables
1. **Water Level**
   - Control: 100% (normal watering)
   - Treatment: 50% (water stress)

2. **Light Exposure**
   - Control: 12 hours/day full spectrum
   - Treatment: 6 hours/day or reduced intensity

### Dependent Variables
1. Leaf area (pixels²)
2. Green intensity (0-255)
3. Green index (normalized)
4. Plant height (pixels)
5. Growth rate (pixels²/day)

### Controlled Variables
- Plant species
- Soil type
- Temperature
- Humidity
- Image capture conditions
- Camera settings

## Experimental Groups

### Group 1: Control (n=10)
- **Water**: Normal (100%)
- **Light**: Normal (12h/day)
- **Purpose**: Baseline healthy reference

### Group 2: Low Water (n=10)
- **Water**: Reduced (50%)
- **Light**: Normal (12h/day)
- **Purpose**: Water stress effects

### Group 3: Low Light (n=10)
- **Water**: Normal (100%)
- **Light**: Reduced (6h/day)
- **Purpose**: Light stress effects

**Total Sample Size**: 30 plants

## Timeline

### Week 1: Setup & Germination
- **Day 1-2**: Prepare growth environment
- **Day 3-5**: Seed germination
- **Day 6-7**: Transplant seedlings

### Week 2: Baseline & Treatment Initiation
- **Day 8-10**: Establish baseline measurements
- **Day 11**: Begin stress treatments
- **Day 12-14**: Daily monitoring

### Week 3: Data Collection
- **Day 15-21**: Intensive data collection
- **Frequency**: Every 6-12 hours
- **Focus**: Document stress progression

### Week 4: Analysis & Model Training
- **Day 22-23**: Complete data collection
- **Day 24-25**: Feature extraction from all images
- **Day 26-27**: Train and validate ML model
- **Day 28**: Dashboard development and testing

## Data Collection Protocol

### Image Capture Specifications

**Hardware**:
- Camera: Any smartphone/digital camera (minimum 5MP)
- Lighting: Consistent LED or natural light
- Background: White or black uniform backdrop

**Settings**:
- Distance: 30-40 cm from plant
- Angle: Directly above (top-down view)
- Focus: Automatic or manual (ensure sharpness)
- Flash: Off (use ambient/supplemental lighting)

**Timing**:
- Morning: 8:00 AM
- Evening: 8:00 PM (if applicable)
- Consistency is critical

**File Naming**:
```
{GroupCode}{PlantNumber}_day{Day}_{Time}.jpg

Examples:
C01_day1_morning.jpg   (Control, Plant 1, Day 1, Morning)
W05_day7_evening.jpg   (Low Water, Plant 5, Day 7, Evening)
L03_day10_morning.jpg  (Low Light, Plant 3, Day 10, Morning)
```

### Measurement Recording

**For each image capture, record**:
- Date and time
- Plant ID
- Group
- Days since treatment started
- Subjective visual health (notes)
- Any anomalies

**Template**:
```
Date: 2026-03-01
Time: 08:00
Plant: C01
Group: Control
Day: 5
Notes: Healthy appearance, new leaf growth
```

## Feature Extraction Procedure

### Manual Verification (Sample Check)
For validation, manually measure a subset:
1. Print image with known scale
2. Measure leaf area with grid overlay
3. Compare with automated calculation
4. Calculate accuracy

### Automated Pipeline
Run for all images:
```bash
python src/processing/batch_process.py --input data/raw --output data/processed
```

## Model Training Procedure

### 1. Prepare Dataset
```bash
python scripts/prepare_dataset.py
```
Creates `plant_dataset.csv` with all features and labels

### 2. Train Model
```bash
python src/models/train_model.py
```
Outputs:
- Trained model: `models/trained/plant_model.pkl`
- Accuracy report
- Confusion matrix

### 3. Validate Model
```bash
python scripts/validate_model.py
```
Cross-validation and performance metrics

## Expected Outcomes

### Quantitative Results

**Healthy Plants**:
- Leaf area: 20,000 - 30,000 px²
- Green index: 100 - 130
- Growth rate: +500-1000 px²/day

**Water Stressed Plants**:
- Leaf area: 8,000 - 12,000 px²
- Green index: 80 - 95
- Growth rate: -200 to +100 px²/day

**Light Stressed Plants**:
- Leaf area: 14,000 - 18,000 px²
- Green index: 65 - 85
- Growth rate: -100 to +200 px²/day

### Model Performance Targets

| Metric | Target |
|--------|--------|
| Overall Accuracy | > 80% |
| Precision (Healthy) | > 85% |
| Precision (Water Stress) | > 75% |
| Precision (Light Stress) | > 75% |
| Recall (all classes) | > 75% |

## Risk Assessment & Mitigation

### Potential Issues

1. **Uneven Growth**
   - *Mitigation*: Larger sample size, statistical analysis

2. **Image Quality Variation**
   - *Mitigation*: Standardized capture protocol, validation checks

3. **Environmental Fluctuations**
   - *Mitigation*: Controlled environment, monitoring logs

4. **Disease/Pests**
   - *Mitigation*: Regular inspection, isolation of affected plants

5. **Model Overfitting**
   - *Mitigation*: Cross-validation, train/test split, more data

## Data Analysis Plan

### Statistical Tests
- **ANOVA**: Compare leaf area across groups
- **T-tests**: Pairwise group comparisons
- **Growth curves**: Polynomial regression

### Visualization
- Box plots (group comparison)
- Line graphs (growth over time)
- Heatmaps (feature correlation)
- Confusion matrix (model performance)

## Ethical Considerations

- No animal subjects involved
- Environmentally conscious (minimal resource waste)
- Data sharing: Make dataset available for research
- Open source: Code published on GitHub

## Success Criteria

✅ **Minimum Viable**:
- Model accuracy > 75%
- Functional dashboard
- Documented methodology

✅ **Target Success**:
- Model accuracy > 80%
- Real-time analysis capability
- Comprehensive documentation
- Demo-ready system

✅ **Excellent Result**:
- Model accuracy > 85%
- Multi-plant tracking
- Historical trend analysis
- Publication-quality documentation

## Deliverables

1. **Complete Dataset**
   - Raw images (organized by group)
   - Processed images
   - Feature CSV files

2. **Trained Model**
   - Model file (.pkl)
   - Training logs
   - Performance metrics

3. **Codebase**
   - Modular Python code
   - Documentation
   - Unit tests

4. **Dashboard**
   - Functional Streamlit app
   - Demo mode
   - User guide

5. **Documentation**
   - Technical report
   - Methodology description
   - Results analysis
   - Presentation slides

## References & Resources

1. OpenCV documentation
2. Scikit-learn documentation
3. Plant physiology research papers
4. Space agriculture literature
5. Image processing techniques

## Contact & Support

**Project Lead**: [Your Name]
**Institution**: [Your Institution]
**Email**: [Your Email]
**GitHub**: [Repository Link]
