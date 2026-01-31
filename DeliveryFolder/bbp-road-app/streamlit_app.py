"""
BBP Road Application - Streamlit Frontend
Connects to FastAPI backend for full functionality.
"""
import streamlit as st
import pandas as pd
import numpy as np
import requests
import folium
from streamlit_folium import st_folium

# Page Configuration
st.set_page_config(page_title="🚲 BBP Road Monitor", page_icon="🚲", layout="wide")

# Backend URL
BACKEND_URL = st.sidebar.text_input("Backend URL", value="https://huxuyan.onrender.com")

# Helper functions
def api_get(endpoint, params=None):
    try:
        resp = requests.get(f"{BACKEND_URL}{endpoint}", params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except:
        return None

def api_post(endpoint, json_data=None, params=None):
    try:
        resp = requests.post(f"{BACKEND_URL}{endpoint}", json=json_data, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except:
        return None

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# Login
if st.session_state.user is None:
    st.title("🚲 Best Bike Paths (BBP)")
    st.markdown("### Road Condition Monitoring & Route Planning")
    username = st.text_input("👤 Enter Username", placeholder="e.g., alice")
    if st.button("🚀 Login"):
        if username.strip():
            result = api_post("/api/users", {"username": username.strip()})
            if result:
                st.session_state.user = result
                st.rerun()
    st.stop()

user = st.session_state.user
user_id = user["id"]

st.sidebar.markdown(f"**👤 {user['username']}**")
if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.rerun()

menu = st.sidebar.radio("Navigation", ["📊 Dashboard", "🗺️ Route Planning", "📍 Segments", "📡 Auto Detection"])

if menu == "📊 Dashboard":
    st.title("📊 Dashboard")
    stats = api_get("/api/stats", {"user_id": user_id})
    if stats:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Segments", stats.get("total_segments", 0))
        c2.metric("Reports", stats.get("total_reports", 0))
        c3.metric("Trips", stats.get("total_trips", 0))
        c4.metric("Users", stats.get("active_users", 0))

elif menu == "🗺️ Route Planning":
    st.title("🗺️ Route Planning")
    c1, c2 = st.columns(2)
    with c1:
        from_lat = st.number_input("From Lat", value=45.4781, format="%.4f")
        from_lon = st.number_input("From Lon", value=9.2275, format="%.4f")
    with c2:
        to_lat = st.number_input("To Lat", value=45.4642, format="%.4f")
        to_lon = st.number_input("To Lon", value=9.1900, format="%.4f")
    
    if st.button("🔍 Find Routes"):
        routes = api_post("/api/path/search", {"from_lat": from_lat, "from_lon": from_lon, "to_lat": to_lat, "to_lon": to_lon, "mode": "balanced"})
        if routes and routes.get("routes"):
            m = folium.Map(location=[(from_lat+to_lat)/2, (from_lon+to_lon)/2], zoom_start=14)
            folium.Marker([from_lat, from_lon], popup="Start", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker([to_lat, to_lon], popup="End", icon=folium.Icon(color="red")).add_to(m)
            for i, route in enumerate(routes["routes"][:3]):
                coords = route.get("geometry", {}).get("coordinates", [])
                if coords:
                    folium.PolyLine([[c[1], c[0]] for c in coords], color=["blue","purple","orange"][i], weight=4).add_to(m)
            st_folium(m, width=700, height=500)

elif menu == "📍 Segments":
    st.title("📍 Road Segments")
    segments = api_get("/api/segments", {"user_id": user_id})
    if segments:
        m = folium.Map(location=[45.478, 9.227], zoom_start=13)
        for seg in segments:
            color = {"optimal": "green", "medium": "orange", "suboptimal": "red"}.get(seg["status"], "blue")
            folium.PolyLine([[seg["from_lat"], seg["from_lon"]], [seg["to_lat"], seg["to_lon"]]], color=color, weight=5, popup=seg["name"]).add_to(m)
        st_folium(m, width=700, height=400)

elif menu == "📡 Auto Detection":
    st.title("📡 Auto Detection")
    severity = st.selectbox("Simulate", ["Normal", "Bump", "Pothole", "Severe"])
    mult = {"Normal": 1, "Bump": 3, "Pothole": 5, "Severe": 8}[severity]
    data = pd.DataFrame(np.random.randn(50, 3) * mult, columns=['X', 'Y', 'Z'])
    st.line_chart(data)
    max_acc = data.abs().max().max()
    if max_acc > 25:
        st.error("🚨 SEVERE damage!")
    elif max_acc > 15:
        st.warning("⚠️ POTHOLE detected!")
    elif max_acc > 8:
        st.info("📍 BUMP detected")
    else:
        st.success("✅ Smooth road")

st.sidebar.caption(f"Backend: {BACKEND_URL}")
