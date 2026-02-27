# System Architecture

## Overview

The AI-Based Autonomous Plant Health Monitoring System follows a modular architecture designed for reliability, scalability, and ease of maintenance.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     INPUT LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Camera       │  │ File Upload  │  │ Database     │      │
│  │ Interface    │  │ Module       │  │ Import       │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 PROCESSING LAYER                             │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Image Preprocessing                              │       │
│  │  - Resize & Normalize                             │       │
│  │  - HSV Conversion                                 │       │
│  │  - Green Mask Generation                          │       │
│  │  - Noise Removal                                  │       │
│  └──────────────────────────────────────────────────┘       │
│                           │                                  │
│  ┌──────────────────────────────────────────────────┐       │
│  │  Plant Segmentation                               │       │
│  │  - Contour Detection                              │       │
│  │  - Region Extraction                              │       │
│  │  - Bounding Box Calculation                       │       │
│  └──────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 FEATURE EXTRACTION LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Leaf Area    │  │ Green        │  │ Morphology   │      │
│  │ Calculation  │  │ Intensity    │  │ Features     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     AI LAYER                                 │
│  ┌────────────────────────────────────────────────┐         │
│  │  Random Forest Classifier                       │         │
│  │  - Feature: Leaf Area                           │         │
│  │  - Feature: Green Index                         │         │
│  │  - Output: Health Status                        │         │
│  │  - Output: Confidence Score                     │         │
│  └────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  STORAGE LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ CSV Logging  │  │ Model        │  │ Image        │      │
│  │ (Historical) │  │ Persistence  │  │ Archive      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                 PRESENTATION LAYER                           │
│  ┌────────────────────────────────────────────────┐         │
│  │  Streamlit Dashboard                            │         │
│  │  - Image Display                                │         │
│  │  - Metrics Visualization                        │         │
│  │  - Health Status Display                        │         │
│  │  - Alert System                                 │         │
│  │  - Historical Graphs                            │         │
│  └────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. Input Layer
**Purpose**: Receive plant images from various sources

**Components**:
- **Camera Interface**: Direct camera feed integration
- **File Upload**: Manual image upload via web interface
- **Database Import**: Batch processing from storage

### 2. Processing Layer
**Purpose**: Prepare images for feature extraction

**Key Operations**:
- **Preprocessing**: Standardize image format and size
- **Color Space Conversion**: BGR → HSV for better color segmentation
- **Mask Generation**: Isolate green (plant) regions
- **Noise Removal**: Morphological operations to clean mask

### 3. Feature Extraction Layer
**Purpose**: Extract quantitative health indicators

**Features**:
- **Leaf Area**: Total green pixel count
- **Green Intensity**: Average green channel value
- **Green Index**: Normalized color health metric
- **Morphological Features**: Height, width, compactness

### 4. AI Layer
**Purpose**: Classify plant health status

**Model**: Random Forest Classifier
- **Input**: Leaf Area + Green Index
- **Output**: Healthy / Water_Stress / Light_Stress
- **Confidence**: Probability score for prediction

### 5. Storage Layer
**Purpose**: Persist data and models

**Components**:
- **Historical Data**: CSV logs of all measurements
- **Model Storage**: Serialized trained models
- **Image Archive**: Processed plant images

### 6. Presentation Layer
**Purpose**: User interface and visualization

**Features**:
- Interactive dashboard
- Real-time analysis
- Historical trends
- Alert system
- Export capabilities

## Data Flow

1. **Image Capture** → Image uploaded or captured
2. **Preprocessing** → Image cleaned and normalized
3. **Segmentation** → Plant isolated from background
4. **Feature Extraction** → Quantitative metrics calculated
5. **Prediction** → ML model classifies health
6. **Logging** → Results saved to database
7. **Display** → Results shown on dashboard
8. **Alert** → Notifications if stress detected

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Image Processing | OpenCV |
| Machine Learning | Scikit-learn (Random Forest) |
| Data Management | Pandas, CSV |
| Visualization | Matplotlib, Plotly, Seaborn |
| Configuration | YAML |

## Design Principles

1. **Modularity**: Each component is independent and testable
2. **Scalability**: Can handle multiple plants and long-term monitoring
3. **Reliability**: Fallback mechanisms for robustness
4. **Maintainability**: Clear code structure and documentation
5. **Performance**: Optimized for real-time analysis

## Future Extensions

- Multiple camera support
- Real-time streaming
- Mobile app integration
- Cloud deployment
- Advanced deep learning models
- Multi-spectral imaging support
