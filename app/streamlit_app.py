"""
Streamlit Dashboard - Main Application
Autonomous Plant Health Monitoring System for Space Agriculture
"""

import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from components.dashboard import render_header, render_sidebar, render_main_panel
from components.upload_module import handle_image_upload
from components.alert_system import show_alert
from src.utils.helpers import create_project_structure

# Page configuration
st.set_page_config(
    page_title="Plant Health Monitoring - Space Agriculture",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2ecc71;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2ecc71;
        margin: 1rem 0;
    }
    .status-healthy {
        color: #2ecc71;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .status-stress {
        color: #e74c3c;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #27ae60;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Ensure project structure exists
    try:
        create_project_structure()
    except:
        pass
    
    # Header
    render_header()
    
    # Sidebar
    app_mode = render_sidebar()
    
    # Main content based on mode
    if app_mode == "Upload & Analyze":
        render_main_panel()
    
    elif app_mode == "Run Demo":
        from components.dashboard import render_demo_mode
        render_demo_mode()
    
    elif app_mode == "View History":
        from components.dashboard import render_history_view
        render_history_view()
    
    elif app_mode == "About":
        render_about_page()


def render_about_page():
    """Render about page"""
    st.markdown("## 🚀 About This System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Project Overview
        
        This **Autonomous Plant Health Monitoring System** is designed for space agriculture 
        applications, providing:
        
        - 🌱 **Automated Image Analysis**
        - 🔍 **Early Stress Detection**
        - 📊 **Growth Tracking**
        - 🤖 **AI-Powered Predictions**
        - 📈 **Real-time Dashboard**
        
        ### Technology Stack
        
        - **Image Processing**: OpenCV
        - **Machine Learning**: Random Forest (Scikit-learn)
        - **Dashboard**: Streamlit
        - **Visualization**: Matplotlib, Plotly
        
        ### Features Analyzed
        
        1. **Leaf Area** - Growth indicator
        2. **Green Intensity** - Health indicator
        3. **Growth Rate** - Development tracking
        """)
    
    with col2:
        st.markdown("""
        ### ISRO Relevance
        
        This system addresses critical needs for **future space missions**:
        
        ✅ **Autonomous Operation**
        - Reduces astronaut workload
        - 24/7 monitoring capability
        
        ✅ **Resource Optimization**
        - Early stress detection
        - Efficient water/light usage
        
        ✅ **Scalability**
        - Modular design
        - Adaptable to different plants
        
        ✅ **Data-Driven Decisions**
        - Historical tracking
        - Predictive analytics
        
        ### Classification Categories
        
        - 🟢 **Healthy** - Optimal conditions
        - 🔴 **Water Stress** - Insufficient water
        - 🟡 **Light Stress** - Insufficient light
        
        ### Model Performance
        
        - **Algorithm**: Random Forest Classifier
        - **Expected Accuracy**: >80%
        - **Confidence Scoring**: Included
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 📚 How It Works
    
    1. **📷 Image Capture** - Upload plant image
    2. **🔬 Preprocessing** - Background removal, plant segmentation
    3. **📊 Feature Extraction** - Calculate health metrics
    4. **🤖 AI Prediction** - Random Forest classification
    5. **📈 Display Results** - Visual dashboard with recommendations
    
    ### 🎯 Use Cases
    
    - Space stations and habitats
    - Closed environment agriculture
    - Remote plant monitoring
    - Agricultural research
    """)


if __name__ == "__main__":
    main()
