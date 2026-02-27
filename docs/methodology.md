# Methodology

## Research Approach

This project employs a systematic machine learning approach to develop an autonomous plant health monitoring system suitable for space agriculture applications.

## 1. Experimental Design

### 1.1 Plant Selection
**Selected Species**: Chickpea, Mustard, or Lettuce

**Rationale**:
- Fast growth cycle (10-15 days for visible results)
- Well-documented stress responses
- Suitable for space agriculture research
- Easy to cultivate in controlled environments

### 1.2 Experimental Groups

| Group | Treatment | Purpose |
|-------|-----------|---------|
| Control | Normal water + light | Baseline healthy reference |
| Low Water | 50% water reduction | Water stress simulation |
| Low Light | Reduced light exposure | Light stress simulation |

**Sample Size**: Minimum 10 plants per group (30 total)

**Duration**: 10-15 days

### 1.3 Data Collection Protocol

**Frequency**: Every 6-12 hours

**Conditions**:
- Consistent background (white/black)
- Fixed camera distance
- Uniform lighting
- Same time of day

**Naming Convention**: `plantID_day_time.jpg`
Example: `P001_day5_morning.jpg`

## 2. Image Processing Pipeline

### 2.1 Preprocessing
```
Input Image (any size)
    ↓
Resize to 640x480
    ↓
Convert BGR → HSV
    ↓
Apply green color mask
    ↓
Morphological operations (denoise)
    ↓
Plant region extracted
```

### 2.2 Color Space Selection
**HSV vs RGB**: We use HSV because:
- Better color separation
- Lighting invariance
- Easier threshold definition
- Green range: H=35-85°, S=40-255, V=40-255

### 2.3 Segmentation
**Method**: Color-based thresholding + contour detection

**Steps**:
1. Create binary mask (green = 1, non-green = 0)
2. Apply morphological opening (remove noise)
3. Apply morphological closing (fill holes)
4. Find contours
5. Select largest contour (main plant)

## 3. Feature Engineering

### 3.1 Primary Features

#### Leaf Area (LA)
```
LA = Count of green pixels in mask
Unit: pixels²
Range: 5,000 - 100,000 typical
```

**Significance**: Direct growth indicator

#### Green Index (GI)
```
GI = (2 * G - R - B) / (2 * G + R + B)
Unit: normalized value
Range: 60 - 130 typical
```

**Significance**: Health and chlorophyll indicator

### 3.2 Secondary Features

- **Plant Height**: Bounding box height
- **Plant Width**: Bounding box width
- **Compactness**: 4π × Area / Perimeter²
- **Growth Rate**: ΔArea / Δtime

## 4. Machine Learning Model

### 4.1 Model Selection: Random Forest Classifier

**Rationale**:
- Handles non-linear relationships
- Robust to outliers
- Provides feature importance
- No need for feature scaling
- Built-in confidence scores

### 4.2 Training Configuration

```python
RandomForestClassifier(
    n_estimators=100,      # Number of trees
    max_depth=10,          # Tree depth limit
    random_state=42        # Reproducibility
)
```

### 4.3 Training Process

```
Load Dataset (CSV)
    ↓
Features: [Leaf_Area, Green_Index]
Labels: [Healthy, Water_Stress, Light_Stress]
    ↓
Train/Test Split (80/20)
    ↓
Train Random Forest
    ↓
Evaluate Performance
    ↓
Save Model (.pkl)
```

### 4.4 Classification Logic

| Leaf Area | Green Index | Predicted Status |
|-----------|-------------|------------------|
| > 20,000  | > 100       | Healthy |
| < 12,000  | < 85        | Water Stress |
| Medium    | < 75        | Light Stress |

*Note: These are approximate thresholds; actual model learns complex decision boundaries*

### 4.5 Model Evaluation Metrics

- **Accuracy**: Overall correctness
- **Precision**: Correct positive predictions
- **Recall**: Ability to find all positives
- **F1-Score**: Harmonic mean of precision/recall
- **Confusion Matrix**: Detailed error analysis

## 5. Validation Strategy

### 5.1 Cross-Validation
- K-Fold CV (k=5)
- Stratified split to maintain class balance

### 5.2 Test Set Evaluation
- 20% holdout test set
- Never used in training

### 5.3 Expected Performance
- **Target Accuracy**: > 80%
- **Minimum Viable**: > 75%

## 6. Data Logging

### 6.1 Historical Records
All measurements logged to CSV:
- Timestamp
- Plant ID
- Group
- All extracted features
- Predicted status
- Confidence score

### 6.2 Growth Tracking
Calculate growth rate from historical data:
```
Growth Rate = (Current Area - Previous Area) / Time Elapsed
```

## 7. Dashboard Implementation

### 7.1 Technology: Streamlit

**Justification**:
- Python-native (integrates with CV/ML code)
- Rapid development
- Interactive widgets
- Real-time updates

### 7.2 User Workflow

```
1. Upload Image
    ↓
2. Automatic Processing
    ↓
3. Display Results:
   - Original vs Processed
   - Extracted Metrics
   - Health Status
   - Confidence Score
   - Recommendations
    ↓
4. Log to History
    ↓
5. View Historical Trends
```

## 8. Alert System

### 8.1 Trigger Conditions
- Water Stress: Leaf area < 12,000 OR green index < 85
- Light Stress: Green index < 75
- Healthy: All metrics in normal range

### 8.2 Recommendations
Automated care suggestions based on detected status

## 9. Quality Assurance

### 9.1 Testing Strategy
- Unit tests for each module
- Integration tests for pipeline
- Visual inspection of processed images

### 9.2 Error Handling
- Image validation
- Model availability fallback
- Robust file I/O

## 10. Space Agriculture Relevance

### 10.1 Autonomous Operation
- Minimal human intervention
- Scheduled monitoring
- Automatic alerts

### 10.2 Resource Optimization
- Early stress detection → faster intervention
- Reduced water waste
- Optimized light usage

### 10.3 Scalability
- Multi-plant tracking
- Long-duration missions
- Modular design for expansion

## References

1. Color-based plant segmentation techniques
2. Random Forest for agricultural applications
3. Space agriculture research (NASA, ISRO)
4. Plant stress detection methodologies
