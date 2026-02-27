"""
Alert System Module
Display alerts and recommendations based on plant health
"""

import streamlit as st


def show_alert(status: str, confidence: float, recommendation: str = None):
    """
    Display health status alert
    
    Args:
        status: Health status
        confidence: Confidence percentage
        recommendation: Optional recommendation text
    """
    
    # Configure alert based on status
    if status == 'Healthy':
        alert_type = 'success'
        icon = '✅'
        color = '#2ecc71'
        message = "Plant is Healthy!"
        default_rec = "Continue current care routine. Monitor regularly."
        
    elif status == 'Water_Stress':
        alert_type = 'error'
        icon = '💧'
        color = '#e74c3c'
        message = "Water Stress Detected!"
        default_rec = "Increase watering frequency. Check soil moisture level."
        
    elif status == 'Light_Stress':
        alert_type = 'warning'
        icon = '☀️'
        color = '#f39c12'
        message = "Light Stress Detected!"
        default_rec = "Increase light exposure. Move plant to brighter location or add grow lights."
        
    else:
        alert_type = 'info'
        icon = '❓'
        color = '#95a5a6'
        message = "Status Unknown"
        default_rec = "Monitor plant condition closely."
    
    # Use provided recommendation or default
    rec_text = recommendation if recommendation else default_rec
    
    # Display alert
    st.markdown(f"""
    <div style='background-color: {color}20; border-left: 5px solid {color}; 
                padding: 1.5rem; border-radius: 5px; margin: 1rem 0;'>
        <h2 style='color: {color}; margin: 0;'>{icon} {message}</h2>
        <p style='font-size: 1.1rem; margin-top: 0.5rem;'>
            Confidence: <strong>{confidence:.1f}%</strong>
        </p>
        <hr style='border-color: {color}50;'>
        <p style='margin: 0;'><strong>Recommendation:</strong> {rec_text}</p>
    </div>
    """, unsafe_allow_html=True)


def show_detailed_alert(prediction_result: dict):
    """
    Show detailed alert with probability breakdown
    
    Args:
        prediction_result: Dictionary with prediction details
    """
    status = prediction_result.get('status', 'Unknown')
    confidence = prediction_result.get('confidence', 0)
    recommendation = prediction_result.get('recommendation', None)
    probabilities = prediction_result.get('probabilities', {})
    
    # Show main alert
    show_alert(status, confidence, recommendation)
    
    # Show probability breakdown if available
    if probabilities:
        st.markdown("### 📊 Detailed Probability Breakdown")
        
        # Create columns for each class
        cols = st.columns(len(probabilities))
        
        for idx, (class_name, prob) in enumerate(probabilities.items()):
            with cols[idx]:
                # Format class name
                display_name = class_name.replace('_', ' ').title()
                
                # Color based on probability
                if prob > 50:
                    color = '#2ecc71'
                elif prob > 25:
                    color = '#f39c12'
                else:
                    color = '#95a5a6'
                
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; 
                            background-color: {color}20; border-radius: 5px;'>
                    <h4 style='color: {color}; margin: 0;'>{display_name}</h4>
                    <p style='font-size: 2rem; font-weight: bold; 
                              color: {color}; margin: 0.5rem 0;'>
                        {prob:.1f}%
                    </p>
                </div>
                """, unsafe_allow_html=True)


def show_comparison_alert(current_status: str, previous_status: str):
    """
    Show alert comparing current and previous status
    
    Args:
        current_status: Current health status
        previous_status: Previous health status
    """
    if current_status == previous_status:
        st.info(f"ℹ️ Status unchanged: {current_status}")
    elif current_status == 'Healthy':
        st.success(f"🎉 Improvement! Changed from {previous_status} to {current_status}")
    else:
        st.warning(f"⚠️ Status changed from {previous_status} to {current_status}")


def show_action_recommendations(status: str):
    """
    Show specific action recommendations
    
    Args:
        status: Health status
    """
    st.markdown("### 🎯 Action Items")
    
    actions = {
        'Healthy': [
            "✅ Continue current watering schedule",
            "✅ Maintain light exposure levels",
            "✅ Monitor for any changes",
            "✅ Document growth progress"
        ],
        'Water_Stress': [
            "💧 Increase watering frequency",
            "💧 Check soil moisture level",
            "💧 Ensure proper drainage",
            "💧 Monitor leaf turgor",
            "💧 Consider adjusting watering schedule"
        ],
        'Light_Stress': [
            "☀️ Increase light exposure duration",
            "☀️ Move closer to light source",
            "☀️ Consider supplemental grow lights",
            "☀️ Check for obstructions blocking light",
            "☀️ Rotate plant for even exposure"
        ]
    }
    
    action_list = actions.get(status, ["Monitor plant condition"])
    
    for action in action_list:
        st.markdown(f"- {action}")


if __name__ == "__main__":
    st.title("Alert System Module")
    
    st.markdown("### Example Alerts:")
    
    # Example healthy
    st.markdown("#### Healthy Plant")
    show_alert('Healthy', 92.5)
    
    # Example water stress
    st.markdown("#### Water Stressed Plant")
    show_alert('Water_Stress', 87.3)
    
    # Example light stress
    st.markdown("#### Light Stressed Plant")
    show_alert('Light_Stress', 78.9)
