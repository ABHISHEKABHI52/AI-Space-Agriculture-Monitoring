"""
Dashboard Components
Main rendering functions for the dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
from PIL import Image
import cv2

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.processing.image_preprocessing import preprocess_image
from src.features.feature_extraction import extract_features
from src.models.predict import predict_health
from src.data.data_logger import DataLogger
from src.visualization.plot_growth import PlantVisualizer


def render_header():
    """Render application header"""
    st.markdown("""
    <div class="main-header">
        🌱 Autonomous Plant Monitoring System – Space Agriculture 🚀
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style='text-align: center; color: #7f8c8d; font-size: 1.1rem;'>
    AI-Powered Plant Health Detection for Future Space Missions
    </p>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render sidebar with controls"""
    st.sidebar.markdown("## 🎛️ Control Panel")
    
    app_mode = st.sidebar.selectbox(
        "Select Mode",
        ["Upload & Analyze", "Run Demo", "View History", "About"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📋 Plant Information")
    
    plant_id = st.sidebar.text_input("Plant ID", value="P001")
    
    group = st.sidebar.selectbox(
        "Experimental Group",
        ["Control", "Low_Water", "Low_Light"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ System Info")
    st.sidebar.info("""
    **Status**: 🟢 Online
    
    **Model**: Random Forest
    
    **Accuracy**: >80%
    """)
    
    # Store in session state
    st.session_state['plant_id'] = plant_id
    st.session_state['group'] = group
    
    return app_mode


def render_main_panel():
    """Render main analysis panel"""
    st.markdown("## 📸 Upload and Analyze Plant Image")
    
    uploaded_file = st.file_uploader(
        "Choose a plant image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the plant with uniform background"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Process and analyze
        analyze_image(temp_path)
        
        # Clean up
        try:
            os.remove(temp_path)
        except:
            pass
    else:
        st.info("👆 Please upload an image to begin analysis")
        
        # Show example
        st.markdown("### 📝 Example Analysis Workflow")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 1️⃣ Upload Image")
            st.markdown("Upload plant photo")
        
        with col2:
            st.markdown("#### 2️⃣ AI Analysis")
            st.markdown("Automatic processing")
        
        with col3:
            st.markdown("#### 3️⃣ Get Results")
            st.markdown("Health status & recommendations")


def analyze_image(image_path: str):
    """Analyze uploaded image"""
    st.markdown("### 🔬 Analysis Results")
    
    # Create columns for image display
    col1, col2 = st.columns(2)
    
    with st.spinner("Processing image..."):
        # Preprocess image
        result = preprocess_image(image_path)
        
        if not result['success']:
            st.error("❌ Failed to process image. Please try another image.")
            return
        
        original = result['original']
        mask = result['mask']
        extracted = result['extracted']
    
    # Display images
    with col1:
        st.markdown("#### 📷 Original Image")
        st.image(cv2.cvtColor(original, cv2.COLOR_BGR2RGB), use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Processed Image")
        st.image(cv2.cvtColor(extracted, cv2.COLOR_BGR2RGB), use_container_width=True)
    
    # Extract features
    with st.spinner("Extracting features..."):
        plant_id = st.session_state.get('plant_id', 'P001')
        group = st.session_state.get('group', 'Control')
        
        features = extract_features(original, mask, plant_id, group)
    
    # Make prediction
    with st.spinner("Analyzing health status..."):
        prediction = predict_health(
            features['leaf_area'],
            features['green_index']
        )
    
    # Display metrics
    st.markdown("### 📊 Health Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Leaf Area",
            value=f"{features['leaf_area']:,} px²",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Green Index",
            value=f"{features['green_index']:.2f}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Plant Height",
            value=f"{features['plant_height']} px",
            delta=None
        )
    
    with col4:
        st.metric(
            label="Plant Width",
            value=f"{features['plant_width']} px",
            delta=None
        )
    
    # Display prediction
    st.markdown("### 🎯 Health Status Prediction")
    
    status = prediction['status']
    confidence = prediction['confidence']
    
    # Color-coded status display
    if status == 'Healthy':
        status_color = "🟢"
        box_color = "#d5f4e6"
    elif status == 'Water_Stress':
        status_color = "🔴"
        box_color = "#fadbd8"
    else:
        status_color = "🟡"
        box_color = "#fcf3cf"
    
    st.markdown(f"""
    <div style='background-color: {box_color}; padding: 2rem; border-radius: 10px; margin: 1rem 0;'>
        <h2 style='text-align: center; margin: 0;'>{status_color} {status.replace('_', ' ')}</h2>
        <p style='text-align: center; font-size: 1.2rem; margin-top: 0.5rem;'>
            Confidence: {confidence:.1f}%
        </p>
    </div>
    """, unsafe_html=True)
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    st.info(prediction['recommendation'])
    
    # Probability breakdown
    if 'probabilities' in prediction and prediction['probabilities']:
        st.markdown("### 📈 Probability Breakdown")
        prob_df = pd.DataFrame([
            {'Status': k.replace('_', ' '), 'Probability': f"{v:.1f}%"}
            for k, v in prediction['probabilities'].items()
        ])
        st.dataframe(prob_df, hide_index=True, use_container_width=True)
    
    # Save results
    if st.button("💾 Save Results to History"):
        save_results_to_history(features, prediction)


def save_results_to_history(features: dict, prediction: dict):
    """Save analysis results to history"""
    try:
        logger = DataLogger()
        
        data = {
            **features,
            'health_status': prediction['status'],
            'confidence': prediction['confidence']
        }
        
        logger.log_measurement(data)
        st.success("✅ Results saved to history!")
    except Exception as e:
        st.error(f"❌ Error saving results: {e}")


def render_demo_mode():
    """Render demo mode with sample data"""
    st.markdown("## 🎬 Demo Mode")
    
    st.info("🎯 Demo mode shows the system in action with pre-loaded sample data")
    
    if st.button("▶️ Run Demo Analysis", type="primary"):
        # Create sample data
        demo_data = [
            {
                'name': 'Healthy Plant',
                'leaf_area': 25000,
                'green_index': 120,
                'description': 'Control group - optimal conditions'
            },
            {
                'name': 'Water Stressed Plant',
                'leaf_area': 9000,
                'green_index': 85,
                'description': 'Low water group - 50% water'
            },
            {
                'name': 'Light Stressed Plant',
                'leaf_area': 15000,
                'green_index': 70,
                'description': 'Low light group - reduced exposure'
            }
        ]
        
        for i, plant in enumerate(demo_data):
            st.markdown(f"### 🌱 Sample {i+1}: {plant['name']}")
            st.markdown(f"*{plant['description']}*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Leaf Area", f"{plant['leaf_area']:,} px²")
                st.metric("Green Index", f"{plant['green_index']:.1f}")
            
            with col2:
                prediction = predict_health(plant['leaf_area'], plant['green_index'])
                st.markdown(f"**Status**: {prediction['status'].replace('_', ' ')}")
                st.markdown(f"**Confidence**: {prediction['confidence']:.1f}%")
                st.markdown(f"**Recommendation**: {prediction['recommendation']}")
            
            st.markdown("---")


def render_history_view():
    """Render historical data view"""
    st.markdown("## 📜 Historical Data")
    
    try:
        logger = DataLogger()
        df = logger.load_history()
        
        if df.empty:
            st.warning("📊 No historical data available yet. Analyze some images first!")
            return
        
        st.success(f"📊 Found {len(df)} records")
        
        # Summary statistics
        st.markdown("### 📈 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Unique Plants", df['plant_id'].nunique())
        with col3:
            if 'health_status' in df.columns:
                healthy_count = len(df[df['health_status'] == 'Healthy'])
                st.metric("Healthy Plants", healthy_count)
        
        # Display data
        st.markdown("### 📋 Records")
        st.dataframe(df, use_container_width=True)
        
        # Visualizations
        if len(df) > 0:
            st.markdown("### 📊 Visualizations")
            
            viz = PlantVisualizer()
            
            # Growth plot
            if 'leaf_area' in df.columns:
                try:
                    fig = viz.plot_growth_over_time(df)
                    st.pyplot(fig)
                except Exception as e:
                    st.error(f"Could not generate growth plot: {e}")
        
    except Exception as e:
        st.error(f"❌ Error loading history: {e}")
