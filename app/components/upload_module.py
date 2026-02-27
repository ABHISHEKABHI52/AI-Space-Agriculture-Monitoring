"""
Image Upload Module
Handles image upload and validation
"""

import streamlit as st
from PIL import Image
import os


def validate_uploaded_file(uploaded_file) -> bool:
    """
    Validate uploaded file
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        True if valid
    """
    if uploaded_file is None:
        return False
    
    # Check file size (max 10MB)
    if uploaded_file.size > 10 * 1024 * 1024:
        st.error("❌ File too large! Maximum size is 10MB")
        return False
    
    # Check file type
    valid_types = ['jpg', 'jpeg', 'png']
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    if file_ext not in valid_types:
        st.error(f"❌ Invalid file type! Supported: {', '.join(valid_types)}")
        return False
    
    return True


def handle_image_upload():
    """
    Handle image upload with validation
    
    Returns:
        Path to saved image or None
    """
    uploaded_file = st.file_uploader(
        "Upload plant image",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear image of the plant"
    )
    
    if uploaded_file is not None:
        if validate_uploaded_file(uploaded_file):
            # Save temporarily
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            
            temp_path = os.path.join(temp_dir, uploaded_file.name)
            
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success("✅ Image uploaded successfully!")
            return temp_path
    
    return None


def display_upload_guidelines():
    """Display guidelines for image upload"""
    st.markdown("""
    ### 📸 Image Upload Guidelines
    
    For best results:
    - ✅ Use uniform background (white or black preferred)
    - ✅ Ensure good lighting
    - ✅ Keep consistent distance from camera
    - ✅ Center the plant in frame
    - ✅ Avoid shadows
    - ✅ Image format: JPG, JPEG, or PNG
    - ✅ Max file size: 10MB
    """)


if __name__ == "__main__":
    st.title("Image Upload Module")
    display_upload_guidelines()
    image_path = handle_image_upload()
    
    if image_path:
        st.image(image_path, caption="Uploaded Image")
