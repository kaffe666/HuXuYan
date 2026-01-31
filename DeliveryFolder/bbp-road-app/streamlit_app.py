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
BACKEND_URL = "https://huxuyan.onrender.com"

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

def get_seg_name(seg):
    """Get segment name from various possible fields."""
    return seg.get("road_name") or seg.get("name") or f"Segment {seg.get('id', '?')}"

def get_seg_coords(seg):
    """Get segment coordinates, handling both naming conventions."""
    start_lat = seg.get("start_lat") or seg.get("from_lat", 0)
    start_lon = seg.get("start_lon") or seg.get("from_lon", 0)
    end_lat = seg.get("end_lat") or seg.get("to_lat", 0)
    end_lon = seg.get("end_lon") or seg.get("to_lon", 0)
    return start_lat, start_lon, end_lat, end_lon

# ============== Session State ==============
if "user" not in st.session_state:
    st.session_state.user = None
if "language" not in st.session_state:
    st.session_state.language = "en"
if "current_page" not in st.session_state:
    st.session_state.current_page = "📊 Dashboard"

# ============== Custom CSS ==============
st.markdown("""
<style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Navigation items - block style like GitHub */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        margin: 4px 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .nav-item:hover {
        background: rgba(255,255,255,0.15);
        border-color: rgba(255,255,255,0.2);
    }
    .nav-item.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-color: transparent;
    }
    .nav-icon {
        font-size: 1.2rem;
        margin-right: 12px;
        width: 24px;
        text-align: center;
    }
    .nav-text {
        font-size: 0.95rem;
        font-weight: 500;
    }
    
    /* User profile card */
    .user-card {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
        margin: 16px 0;
        border: 1px solid rgba(255,255,255,0.15);
    }
    .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-right: 12px;
    }
    
    /* Hide default radio buttons */
    [data-testid="stSidebar"] .stRadio > div {
        display: none;
    }
    
    /* Main content improvements */
    .main .block-container {
        padding-top: 2rem;
    }
    
    /* Cards */
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ============== Sidebar ==============
with st.sidebar:
    st.markdown("## 🚲 BBP Road Monitor")
    
    # Language selector
    languages = {"en": "English", "zh": "中文", "it": "Italiano"}
    st.session_state.language = st.selectbox(
        "🌐 Language",
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        label_visibility="collapsed"
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

# Sidebar navigation with block-style design
with st.sidebar:
    # User profile card
    st.markdown(f"""
    <div class="user-card">
        <div style="display: flex; align-items: center;">
            <div class="user-avatar">👤</div>
            <div>
                <div style="font-weight: 600; font-size: 1rem;">{user['username']}</div>
                <div style="font-size: 0.8rem; opacity: 0.7;">Logged in</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### Navigation")
    
    # Block-style navigation
    nav_items = [
        ("📊", "Dashboard"),
        ("🗺️", "Route Planning"),
        ("📍", "Segments"),
        ("📝", "Reports"),
        ("🚴", "Trips"),
        ("📡", "Auto Detection"),
        ("⚙️", "Settings")
    ]
    
    for icon, name in nav_items:
        full_name = f"{icon} {name}"
        is_active = st.session_state.current_page == full_name
        
        if st.button(
            f"{icon}  {name}",
            key=f"nav_{name}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = full_name
            st.rerun()

menu = st.session_state.current_page

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
                "origin": {"lat": from_lat, "lon": from_lon},
                "destination": {"lat": to_lat, "lon": to_lon},
                "preferences": mode
            }, {"user_id": user_id})
            
            if routes and routes.get("routes"):
                st.success(f"✅ Found {len(routes['routes'])} routes!")
                
                # Show weather info
                if routes.get("weather_summary"):
                    st.info(f"🌤️ {routes['weather_summary']}")
                if routes.get("cycling_recommendation"):
                    st.write(f"🚲 {routes['cycling_recommendation']}")
                
                # Create map
                m = folium.Map(location=[(from_lat + to_lat)/2, (from_lon + to_lon)/2], zoom_start=14)
                
                # Add markers
                folium.Marker([from_lat, from_lon], popup="Origin", icon=folium.Icon(color="green")).add_to(m)
                folium.Marker([to_lat, to_lon], popup="Destination", icon=folium.Icon(color="red")).add_to(m)
                
                # Add routes
                colors = ["blue", "purple", "orange", "darkgreen", "darkred"]
                for i, route in enumerate(routes["routes"][:5]):
                    # Get geometry from GeoJSON format
                    geojson = route.get("geometry_geojson", {})
                    coords = geojson.get("coordinates", [])
                    if coords:
                        # Convert [lon, lat] to [lat, lon] for folium
                        latlon_coords = [[c[1], c[0]] for c in coords]
                        folium.PolyLine(
                            latlon_coords,
                            color=colors[i % len(colors)],
                            weight=4 if i == 0 else 3,
                            opacity=0.8 if i == 0 else 0.5,
                            popup=f"Route {route.get('route_id', i+1)}"
                        ).add_to(m)
                
                st_folium(m, width=700, height=500, returned_objects=[])
                
                # Route details
                st.subheader("📋 Route Details")
                for i, route in enumerate(routes["routes"][:5]):
                    tags_display = ", ".join(route.get("tags_localized", route.get("tags", [])))
                    with st.expander(f"Route {route.get('route_id', i+1)}: {tags_display}", expanded=(i==0)):
                        rcol1, rcol2, rcol3 = st.columns(3)
                        distance_km = route.get('total_distance', 0) / 1000
                        rcol1.metric("Distance", f"{distance_km:.2f} km")
                        rcol2.metric("Duration", route.get("duration_display", "N/A"))
                        rcol3.metric("Road Quality", f"{route.get('road_quality_score', 0):.0f}/100")
                        
                        tags = route.get("tags", [])
                        if tags:
                            st.write("**Tags:**", ", ".join(tags))
                        
                        # Show warnings if any
                        warnings = route.get("segments_warning_localized", route.get("segments_warning", []))
                        if warnings:
                            st.warning(f"⚠️ {len(warnings)} segment warning(s) on this route")

# ============== Segments ==============
elif menu == "📍 Segments":
    st.title("📍 Road Segments")
    
    # Fetch segments
    segments = api_get("/api/segments", {"user_id": user_id})
    
    if segments and len(segments) > 0:
        # Create map with segments - use helper function for coords
        coords_list = [get_seg_coords(s) for s in segments if get_seg_coords(s)[0] != 0]
        if coords_list:
            center_lat = sum(c[0] for c in coords_list) / len(coords_list)
            center_lon = sum(c[1] for c in coords_list) / len(coords_list)
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
            start_lat, start_lon, end_lat, end_lon = get_seg_coords(seg)
            if start_lat == 0:
                continue
            color = status_colors.get(seg.get("status", "unknown"), "blue")
            name = get_seg_name(seg)
            folium.PolyLine(
                [[start_lat, start_lon], [end_lat, end_lon]],
                color=color,
                weight=5,
                popup=f"{name}: {seg.get('status_localized', seg.get('status', 'unknown'))}"
            ).add_to(m)
        
        st_folium(m, width=700, height=400, returned_objects=[])
        
        # Segment list
        st.subheader("📋 Segment List")
        df = pd.DataFrame([{
            "ID": s["id"],
            "Name": get_seg_name(s),
            "Status": s.get("status_localized", s.get("status", "unknown")),
            "Obstacles": s.get("obstacle", "None") or "None"
        } for s in segments])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No segments found. Add some segments to get started!")
    
    # Add new segment
    st.markdown("---")
    st.subheader("➕ Add New Segment")
    with st.form("new_segment"):
        seg_name = st.text_input("Road Name", placeholder="e.g., Via Roma")
        col1, col2 = st.columns(2)
        with col1:
            start_lat = st.number_input("Start Latitude", value=45.478, format="%.4f")
            start_lon = st.number_input("Start Longitude", value=9.227, format="%.4f")
        with col2:
            end_lat = st.number_input("End Latitude", value=45.479, format="%.4f")
            end_lon = st.number_input("End Longitude", value=9.228, format="%.4f")
        
        seg_status = st.selectbox("Status", ["optimal", "medium", "suboptimal", "maintenance"])
        obstacle = st.text_input("Obstacle (optional)", placeholder="e.g., pothole")
        
        if st.form_submit_button("Create Segment"):
            result = api_post("/api/segments", {
                "user_id": user_id,
                "road_name": seg_name,
                "start_lat": start_lat,
                "start_lon": start_lon,
                "end_lat": end_lat,
                "end_lon": end_lon,
                "status": seg_status,
                "obstacle": obstacle if obstacle else None
            })
            if result:
                st.success(f"✅ Segment created!")
                st.rerun()

# ============== Reports ==============
elif menu == "📝 Reports":
    st.title("📝 Road Condition Reports")
    
    # Get segments for dropdown
    segments = api_get("/api/segments", {"user_id": user_id})
    
    if segments:
        segment_options = {s["id"]: f"{get_seg_name(s)} (ID: {s['id']})" for s in segments}
        
        # Submit new report
        st.subheader("📝 Submit New Report")
        with st.form("submit_report_form"):
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
            
            note = st.text_area("Notes", placeholder="Describe the road condition...")
            
            if st.form_submit_button("Submit Report"):
                result = api_post(f"/api/segments/{segment_id}/reports", {
                    "user_id": user_id,
                    "note": note
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
                    col1.write(f"**{report.get('note', 'No notes')}**")
                    col2.write(f"ID: {report.get('id', 'N/A')}")
                    col3.write(f"Confirmed: {'✅' if report.get('confirmed') else '❌'}")
                    
                    if not report.get("confirmed"):
                        if st.button(f"Confirm Report #{report['id']}", key=f"confirm_{report['id']}"):
                            api_post(f"/api/reports/{report['id']}/confirm", {"user_id": user_id})
                            st.rerun()
                    st.markdown("---")
        else:
            st.info("No reports for this segment yet")

# ============== Trips ==============
elif menu == "🚴 Trips":
    st.title("🚴 Trip Management")
    
    # Create new trip
    st.subheader("➕ Start New Trip")
    with st.form("new_trip"):
        col1, col2 = st.columns(2)
        with col1:
            trip_start_lat = st.number_input("Start Latitude", value=45.478, format="%.4f")
            trip_start_lon = st.number_input("Start Longitude", value=9.227, format="%.4f")
        with col2:
            trip_end_lat = st.number_input("End Latitude", value=45.464, format="%.4f")
            trip_end_lon = st.number_input("End Longitude", value=9.190, format="%.4f")
        
        if st.form_submit_button("🚀 Create Trip"):
            result = api_post("/api/trips", {
                "user_id": user_id,
                "start_lat": trip_start_lat,
                "start_lon": trip_start_lon,
                "end_lat": trip_end_lat,
                "end_lon": trip_end_lon
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
        segment_options = {s["id"]: f"{get_seg_name(s)} (ID: {s['id']})" for s in segments}
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
st.sidebar.caption("BBP Road Monitor v2.0")
st.sidebar.caption(f"Backend: {BACKEND_URL}")
