"""
BBP Road Application - Streamlit Frontend
This connects to the FastAPI backend for full functionality.
"""
import streamlit as st
import pandas as pd
import numpy as np
import requests
import folium
from streamlit_folium import st_folium
from datetime import datetime

# ============== Configuration ==============
# Change this to your deployed backend URL when deploying
# For local: "http://127.0.0.1:8000"
# For cloud: "https://your-backend.railway.app" or similar
BACKEND_URL = st.sidebar.text_input(
    "Backend URL", 
    value="http://127.0.0.1:8000",
    help="Enter your FastAPI backend URL"
)

# ============== Page Configuration ==============
st.set_page_config(
    page_title="🚲 BBP Road Monitor",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== Helper Functions ==============
def api_get(endpoint: str, params: dict = None):
    """Make GET request to backend API."""
    try:
        resp = requests.get(f"{BACKEND_URL}{endpoint}", params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}. Is it running?")
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

def api_post(endpoint: str, json_data: dict = None, params: dict = None):
    """Make POST request to backend API."""
    try:
        resp = requests.post(f"{BACKEND_URL}{endpoint}", json=json_data, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}. Is it running?")
        return None
    except Exception as e:
        st.error(f"API Error: {e}")
        return None

# ============== Session State ==============
if "user" not in st.session_state:
    st.session_state.user = None
if "language" not in st.session_state:
    st.session_state.language = "en"

# ============== Sidebar ==============
st.sidebar.title("🚲 BBP Road Monitor")

# Language selector
languages = {"en": "English", "zh": "中文", "it": "Italiano"}
st.session_state.language = st.sidebar.selectbox(
    "Language / 语言",
    options=list(languages.keys()),
    format_func=lambda x: languages[x],
    index=0
)

# ============== Login Section ==============
if st.session_state.user is None:
    st.title("🚲 Best Bike Paths (BBP)")
    st.markdown("### Road Condition Monitoring & Route Planning")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("---")
        username = st.text_input("👤 Enter Username", placeholder="e.g., alice")
        
        if st.button("🚀 Login / Register", use_container_width=True):
            if username.strip():
                result = api_post("/api/users", {"username": username.strip()})
                if result:
                    st.session_state.user = result
                    st.rerun()
            else:
                st.warning("Please enter a username")
        
        st.markdown("---")
        st.info("💡 Enter any username to login. New users are automatically registered.")
    
    st.stop()

# ============== Main App (After Login) ==============
user = st.session_state.user
user_id = user["id"]

# Sidebar navigation
st.sidebar.markdown(f"**👤 Logged in as:** {user['username']}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    st.rerun()

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    ["📊 Dashboard", "🗺️ Route Planning", "📍 Segments", "📝 Reports", 
     "🚴 Trips", "📡 Auto Detection", "⚙️ Settings"]
)

# ============== Dashboard ==============
if menu == "📊 Dashboard":
    st.title("📊 Dashboard")
    
    # Fetch stats
    stats = api_get("/api/stats", {"user_id": user_id})
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🛣️ Total Segments", stats.get("total_segments", 0))
        col2.metric("📝 Total Reports", stats.get("total_reports", 0))
        col3.metric("🚴 Total Trips", stats.get("total_trips", 0))
        col4.metric("👥 Active Users", stats.get("active_users", 0))
        
        st.markdown("---")
        
        # Weather
        st.subheader("🌤️ Current Weather")
        weather = api_get("/api/weather", {"lat": 45.478, "lon": 9.227, "user_id": user_id})
        if weather:
            wcol1, wcol2, wcol3, wcol4 = st.columns(4)
            wcol1.metric("Condition", weather.get("condition_localized", "N/A"))
            wcol2.metric("Temperature", f"{weather.get('temperature_c', 'N/A')}°C")
            wcol3.metric("Wind", f"{weather.get('wind_speed_kmh', 'N/A')} km/h")
            wcol4.metric("Rain Chance", f"{weather.get('rain_chance_percent', 'N/A')}%")
            
            if weather.get("is_cycling_friendly"):
                st.success("🚲 Great conditions for cycling!")
            else:
                st.warning("⚠️ Check weather conditions before cycling")

# ============== Route Planning ==============
elif menu == "🗺️ Route Planning":
    st.title("🗺️ Route Planning")
    st.markdown("Plan your cycling route with real road geometry from OSRM.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 Origin")
        from_lat = st.number_input("Latitude", value=45.4781, key="from_lat", format="%.4f")
        from_lon = st.number_input("Longitude", value=9.2275, key="from_lon", format="%.4f")
    
    with col2:
        st.subheader("🏁 Destination")
        to_lat = st.number_input("Latitude", value=45.4642, key="to_lat", format="%.4f")
        to_lon = st.number_input("Longitude", value=9.1900, key="to_lon", format="%.4f")
    
    # Scoring mode
    mode = st.selectbox(
        "🎯 Optimization Mode",
        ["safety_first", "shortest", "balanced"],
        format_func=lambda x: {
            "safety_first": "🛡️ Safety First (avoid bad roads)",
            "shortest": "📏 Shortest Distance",
            "balanced": "⚖️ Balanced"
        }.get(x, x)
    )
    
    if st.button("🔍 Find Routes", use_container_width=True):
        with st.spinner("Fetching routes from OSRM..."):
            routes = api_post("/api/path/search", {
                "from_lat": from_lat,
                "from_lon": from_lon,
                "to_lat": to_lat,
                "to_lon": to_lon,
                "mode": mode
            }, {"user_id": user_id})
            
            if routes and routes.get("routes"):
                st.success(f"✅ Found {len(routes['routes'])} routes!")
                
                # Create map
                m = folium.Map(location=[(from_lat + to_lat)/2, (from_lon + to_lon)/2], zoom_start=14)
                
                # Add markers
                folium.Marker([from_lat, from_lon], popup="Origin", icon=folium.Icon(color="green")).add_to(m)
                folium.Marker([to_lat, to_lon], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
                
                # Add routes
                colors = ["blue", "purple", "orange", "darkgreen", "darkred"]
                for i, route in enumerate(routes["routes"][:5]):
                    coords = route.get("geometry", {}).get("coordinates", [])
                    if coords:
                        # Convert [lon, lat] to [lat, lon] for folium
                        latlon_coords = [[c[1], c[0]] for c in coords]
                        folium.PolyLine(
                            latlon_coords,
                            color=colors[i % len(colors)],
                            weight=4 if i == 0 else 3,
                            opacity=0.8 if i == 0 else 0.5,
                            popup=f"Route {i+1}: {route.get('label', 'N/A')}"
                        ).add_to(m)
                
                st_folium(m, width=700, height=500)
                
                # Route details
                st.subheader("📋 Route Details")
                for i, route in enumerate(routes["routes"][:5]):
                    with st.expander(f"Route {i+1}: {route.get('label', 'Unknown')}", expanded=(i==0)):
                        rcol1, rcol2, rcol3 = st.columns(3)
                        rcol1.metric("Distance", f"{route.get('distance_km', 0):.2f} km")
                        rcol2.metric("Duration", route.get("duration_str", "N/A"))
                        rcol3.metric("Score", f"{route.get('score', 0):.1f}")
                        
                        tags = route.get("tags", [])
                        if tags:
                            st.write("**Tags:**", ", ".join(tags))

# ============== Segments ==============
elif menu == "📍 Segments":
    st.title("📍 Road Segments")
    
    # Fetch segments
    segments = api_get("/api/segments", {"user_id": user_id})
    
    if segments:
        # Create map with segments
        if segments:
            center_lat = sum(s["from_lat"] for s in segments) / len(segments)
            center_lon = sum(s["from_lon"] for s in segments) / len(segments)
        else:
            center_lat, center_lon = 45.478, 9.227
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
        
        status_colors = {
            "optimal": "green",
            "medium": "orange", 
            "suboptimal": "red",
            "maintenance": "gray"
        }
        
        for seg in segments:
            color = status_colors.get(seg["status"], "blue")
            folium.PolyLine(
                [[seg["from_lat"], seg["from_lon"]], [seg["to_lat"], seg["to_lon"]]],
                color=color,
                weight=5,
                popup=f"{seg['name']}: {seg.get('status_localized', seg['status'])}"
            ).add_to(m)
        
        st_folium(m, width=700, height=400)
        
        # Segment list
        st.subheader("📋 Segment List")
        df = pd.DataFrame([{
            "ID": s["id"],
            "Name": s["name"],
            "Status": s.get("status_localized", s["status"]),
            "Obstacles": ", ".join(s.get("obstacles", [])) or "None"
        } for s in segments])
        st.dataframe(df, use_container_width=True)
    
    # Add new segment
    st.markdown("---")
    st.subheader("➕ Add New Segment")
    with st.form("new_segment"):
        name = st.text_input("Segment Name", placeholder="e.g., Via Roma")
        col1, col2 = st.columns(2)
        with col1:
            from_lat = st.number_input("From Latitude", value=45.478, format="%.4f")
            from_lon = st.number_input("From Longitude", value=9.227, format="%.4f")
        with col2:
            to_lat = st.number_input("To Latitude", value=45.479, format="%.4f")
            to_lon = st.number_input("To Longitude", value=9.228, format="%.4f")
        
        status = st.selectbox("Status", ["optimal", "medium", "suboptimal", "maintenance"])
        
        if st.form_submit_button("Create Segment"):
            result = api_post("/api/segments", {
                "name": name,
                "from_lat": from_lat,
                "from_lon": from_lon,
                "to_lat": to_lat,
                "to_lon": to_lon,
                "status": status,
                "user_id": user_id
            })
            if result:
                st.success(f"✅ Segment '{name}' created!")
                st.rerun()

# ============== Reports ==============
elif menu == "📝 Reports":
    st.title("📝 Road Condition Reports")
    
    # Get segments for dropdown
    segments = api_get("/api/segments", {"user_id": user_id})
    
    if segments:
        segment_options = {s["id"]: f"{s['name']} (ID: {s['id']})" for s in segments}
        
        # Submit new report
        st.subheader("📝 Submit New Report")
        with st.form("new_report"):
            segment_id = st.selectbox(
                "Select Segment",
                options=list(segment_options.keys()),
                format_func=lambda x: segment_options[x]
            )
            
            condition = st.select_slider(
                "Road Condition",
                options=["suboptimal", "medium", "optimal"],
                value="medium",
                format_func=lambda x: {"optimal": "✅ Optimal", "medium": "⚠️ Medium", "suboptimal": "❌ Poor"}.get(x, x)
            )
            
            comment = st.text_area("Comment", placeholder="Describe the road condition...")
            
            if st.form_submit_button("Submit Report"):
                result = api_post(f"/api/segments/{segment_id}/reports", {
                    "user_id": user_id,
                    "condition": condition,
                    "comment": comment
                })
                if result:
                    st.success("✅ Report submitted successfully!")
                    st.rerun()
        
        # View reports
        st.markdown("---")
        st.subheader("📋 Recent Reports")
        
        selected_seg = st.selectbox(
            "View reports for segment:",
            options=list(segment_options.keys()),
            format_func=lambda x: segment_options[x],
            key="view_reports_seg"
        )
        
        reports = api_get(f"/api/segments/{selected_seg}/reports")
        if reports:
            for report in reports[:10]:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    col1.write(f"**{report.get('comment', 'No comment')}**")
                    col2.write(f"Status: {report.get('condition', 'N/A')}")
                    col3.write(f"Confirmed: {'✅' if report.get('confirmed') else '❌'}")
                    
                    if not report.get("confirmed"):
                        if st.button(f"Confirm Report #{report['id']}", key=f"confirm_{report['id']}"):
                            api_post(f"/api/reports/{report['id']}/confirm", {"user_id": user_id})
                            st.rerun()
                    st.markdown("---")

# ============== Trips ==============
elif menu == "🚴 Trips":
    st.title("🚴 Trip Management")
    
    # Create new trip
    st.subheader("➕ Start New Trip")
    with st.form("new_trip"):
        col1, col2 = st.columns(2)
        with col1:
            from_lat = st.number_input("Start Latitude", value=45.478, format="%.4f")
            from_lon = st.number_input("Start Longitude", value=9.227, format="%.4f")
        with col2:
            to_lat = st.number_input("End Latitude", value=45.464, format="%.4f")
            to_lon = st.number_input("End Longitude", value=9.190, format="%.4f")
        
        if st.form_submit_button("🚀 Create Trip"):
            result = api_post("/api/trips", {
                "user_id": user_id,
                "from_lat": from_lat,
                "from_lon": from_lon,
                "to_lat": to_lat,
                "to_lon": to_lon
            })
            if result:
                st.success(f"✅ Trip #{result['id']} created!")
                st.rerun()
    
    # List trips
    st.markdown("---")
    st.subheader("📋 Your Trips")
    
    trips = api_get("/api/trips", {"user_id": user_id})
    if trips:
        for trip in trips[:10]:
            with st.expander(f"Trip #{trip['id']} - {trip.get('created_at', 'N/A')[:10]}"):
                col1, col2, col3 = st.columns(3)
                col1.metric("Distance", f"{trip.get('distance_km', 0):.2f} km")
                col2.metric("Duration", trip.get("duration_str", "N/A"))
                col3.metric("Status", trip.get("status", "N/A"))

# ============== Auto Detection ==============
elif menu == "📡 Auto Detection":
    st.title("📡 Automatic Road Condition Detection")
    st.markdown("Simulate accelerometer data to detect road anomalies.")
    
    # Sensor simulation
    st.subheader("📊 Sensor Data Simulation")
    
    col1, col2 = st.columns(2)
    with col1:
        speed = st.slider("Current Speed (km/h)", 0, 50, 18)
    with col2:
        severity = st.selectbox("Simulate Event", ["Normal", "Bump", "Pothole", "Severe"])
    
    # Generate accelerometer data based on severity
    severity_multiplier = {"Normal": 1, "Bump": 3, "Pothole": 5, "Severe": 8}
    mult = severity_multiplier.get(severity, 1)
    
    sensor_data = pd.DataFrame(
        np.random.randn(50, 3) * mult,
        columns=['Accel_X', 'Accel_Y', 'Accel_Z']
    )
    
    st.line_chart(sensor_data)
    
    # Detection thresholds (from your backend)
    max_accel = sensor_data.abs().max().max()
    st.metric("Peak Acceleration", f"{max_accel:.1f} m/s²")
    
    if max_accel > 25:
        st.error("🚨 SEVERE - Major road damage detected!")
    elif max_accel > 15:
        st.warning("⚠️ POTHOLE - Significant road defect detected!")
    elif max_accel > 8:
        st.info("📍 BUMP - Minor road irregularity detected")
    else:
        st.success("✅ Road surface is smooth")
    
    # Submit detection to segment
    st.markdown("---")
    st.subheader("📤 Submit Detection")
    
    segments = api_get("/api/segments", {"user_id": user_id})
    if segments:
        segment_options = {s["id"]: f"{s['name']} (ID: {s['id']})" for s in segments}
        segment_id = st.selectbox(
            "Apply to Segment",
            options=list(segment_options.keys()),
            format_func=lambda x: segment_options[x]
        )
        
        if st.button("📤 Submit Auto-Detection"):
            # Prepare sensor reading
            reading = {
                "acceleration_x": float(sensor_data["Accel_X"].iloc[-1]),
                "acceleration_y": float(sensor_data["Accel_Y"].iloc[-1]),
                "acceleration_z": float(sensor_data["Accel_Z"].iloc[-1]),
                "speed_mps": speed / 3.6,
                "gps_accuracy_m": 5.0
            }
            result = api_post(f"/api/segments/{segment_id}/auto-detect", reading)
            if result:
                st.success(f"✅ Detection submitted! Severity: {result.get('severity', 'Unknown')}")

# ============== Settings ==============
elif menu == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    # Fetch current settings
    settings = api_get(f"/api/users/{user_id}/settings")
    
    st.subheader("🌐 Language Preference")
    new_lang = st.selectbox(
        "Select Language",
        options=["en", "zh", "it"],
        format_func=lambda x: {"en": "English", "zh": "中文", "it": "Italiano"}.get(x, x),
        index=["en", "zh", "it"].index(settings.get("language", "en")) if settings else 0
    )
    
    st.subheader("🎨 Display Settings")
    dark_mode = st.toggle("Dark Mode", value=settings.get("dark_mode", False) if settings else False)
    
    st.subheader("🔔 Notifications")
    notifications = st.toggle("Enable Notifications", value=settings.get("notifications", True) if settings else True)
    
    if st.button("💾 Save Settings"):
        result = api_post(f"/api/users/{user_id}/settings", {
            "language": new_lang,
            "dark_mode": dark_mode,
            "notifications": notifications
        })
        if result:
            st.success("✅ Settings saved!")
            st.rerun()
    
    st.markdown("---")
    st.subheader("ℹ️ User Information")
    st.json(user)

# ============== Footer ==============
st.sidebar.markdown("---")
st.sidebar.caption(f"BBP Road Monitor v2.0")
st.sidebar.caption(f"Backend: {BACKEND_URL}")
