import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(page_title="Best Bike Paths (BBP) - System Prototype", layout="wide")

st.title("🚲 Best Bike Paths (BBP)")
st.markdown("### Requirements Engineering & Design Project")

# Sidebar navigation based on project scope
menu = st.sidebar.selectbox("Navigation", ["Record Trip (Automated)", "Search Paths", "Manual Report"])

if menu == "Record Trip (Automated)":
    st.header("📍 Automated Trip Recording")
    st.info("System is acquiring data from mobile accelerometer and gyroscope...") [cite: 95]
    
    # Simulate Real-time sensor data for pothole detection
    # This addresses the project requirement for identifying potholes via device movement [cite: 95]
    sensor_data = pd.DataFrame(np.random.randn(20, 3), columns=['Accel_X', 'Accel_Y', 'Accel_Z'])
    st.line_chart(sensor_data)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Speed", "18 km/h") [cite: 86]
    col2.metric("Distance", "4.5 km") [cite: 86]
    col3.metric("Status", "Biking Detected") [cite: 94]

    if st.button("Simulate Pothole Detection"):
        st.warning("Significant movement detected! Confirm pothole location?") [cite: 96]

elif menu == "Search Paths":
    st.header("🗺️ Browse Bike Paths")
    st.write("Find the best paths based on status and score.") [cite: 99, 100]
    
    origin = st.text_input("Origin", "Piazza Leonardo da Vinci")
    destination = st.text_input("Destination", "Duomo di Milano")
    
    # Interactive Map for path visualization [cite: 99]
    m = folium.Map(location=[45.478, 9.227], zoom_start=14)
    folium.Marker(
        [45.478, 9.227], 
        popup="Optimal Path", 
        tooltip="Status: Optimal"
    ).add_to(m) [cite: 88, 103]
    st_folium(m, width=700, height=450)

elif menu == "Manual Report":
    st.header("📝 Manual Path Information")
    st.write("Manually insert street information and status.") [cite: 90, 91]
    
    street_name = st.text_input("Street Name")
    path_status = st.select_slider(
        "Path Status",
        options=["Requires Maintenance", "Sufficient", "Medium", "Optimal"]
    ) [cite: 88]
    
    obstacles = st.text_area("Describe Obstacles (e.g., potholes, rare cars)") [cite: 88, 89]
    
    if st.button("Submit Report"):
        st.success("Information successfully stored in BBP inventory.") [cite: 84, 85]
