"""
BBP Road Application - Streamlit Frontend
Professional UI with full i18n support - Gemini Style
"""
import streamlit as st
import pandas as pd
import numpy as np
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
from datetime import datetime
import time
import json

# ============== Configuration ==============
BACKEND_URL = "https://huxuyan.onrender.com"

# ============== Page Configuration ==============
st.set_page_config(
    page_title="BBP Road Monitor",
    page_icon="B",
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
        st.error(f"Cannot connect to backend at {BACKEND_URL}. Is it running?")
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
        st.error(f"Cannot connect to backend at {BACKEND_URL}. Is it running?")
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

def api_patch(endpoint: str, json_data: dict = None):
    """Make PATCH request to backend API."""
    try:
        resp = requests.patch(f"{BACKEND_URL}{endpoint}", json=json_data, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except:
        return None

def geocode_place(query: str):
    """Convert place name to coordinates using Nominatim."""
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": query,
            "format": "json",
            "limit": 5,
            "addressdetails": 1
        }
        headers = {"User-Agent": "BBP-Road-App/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        results = resp.json()
        return results
    except:
        return []

def reverse_geocode(lat: float, lon: float):
    """Convert coordinates to place name."""
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat, "lon": lon, "format": "json"}
        headers = {"User-Agent": "BBP-Road-App/1.0"}
        resp = requests.get(url, params=params, headers=headers, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("display_name", "")
    except:
        pass
    return ""

# ============== Translations ==============
TRANSLATIONS = {
    "en": {
        "app_title": "BBP Road Monitor",
        "dashboard": "Dashboard",
        "route_planning": "Route Planning",
        "segments": "Segments",
        "reports": "Reports",
        "trips": "Trips",
        "auto_detection": "Auto Detection",
        "settings": "Settings",
        "logout": "Sign Out",
        "logged_in": "Logged in",
        "find_routes": "Find Routes",
        "origin": "Origin",
        "destination": "Destination",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "save_settings": "Save Settings",
        "language": "Language",
        "dark_mode": "Dark Mode",
        "notifications": "Notifications",
        "navigation": "NAVIGATION",
        "total_segments": "Total Segments",
        "total_reports": "Total Reports", 
        "total_trips": "Total Trips",
        "active_users": "Active Users",
        "current_weather": "Current Weather",
        "condition": "Condition",
        "temperature": "Temperature",
        "wind": "Wind Speed",
        "rain_chance": "Rain Chance",
        "great_cycling": "Great conditions for cycling!",
        "check_weather": "Check weather conditions before cycling",
        "plan_route": "Plan your cycling route with real road geometry",
        "optimization_mode": "Optimization Mode",
        "safety_first": "Safety First",
        "shortest": "Shortest Distance",
        "balanced": "Balanced",
        "route_details": "Route Details",
        "distance": "Distance",
        "duration": "Duration",
        "road_quality": "Road Quality",
        "tags": "Tags",
        "road_segments": "Road Segments",
        "segment_list": "Segment List",
        "add_segment": "Add New Segment",
        "road_name": "Road Name",
        "status": "Status",
        "obstacle": "Obstacle",
        "create_segment": "Create Segment",
        "segment_created": "Segment created!",
        "no_segments": "No segments found",
        "optimal": "Optimal",
        "medium": "Medium",
        "suboptimal": "Suboptimal",
        "maintenance": "Maintenance",
        "road_reports": "Road Condition Reports",
        "submit_report": "Submit New Report",
        "select_segment": "Select Segment",
        "road_condition": "Road Condition",
        "notes": "Notes",
        "submit": "Submit",
        "report_submitted": "Report submitted!",
        "recent_reports": "Recent Reports",
        "no_reports": "No reports yet",
        "confirmed": "Confirmed",
        "confirm_report": "Confirm",
        "trip_management": "Trip Management",
        "start_trip": "Start New Trip",
        "create_trip": "Create Trip",
        "trip_created": "Trip created!",
        "your_trips": "Your Trips",
        "trip": "Trip",
        "auto_detect_title": "Automatic Road Condition Detection",
        "auto_detect_desc": "Real-time road surface analysis using device sensors",
        "current_location": "Current Location",
        "current_speed": "Current Speed",
        "sensor_data": "Sensor Data",
        "peak_acceleration": "Peak Acceleration",
        "detection_result": "Detection Result",
        "severe_damage": "SEVERE - Major road damage detected",
        "pothole_detected": "POTHOLE - Road defect detected",
        "bump_detected": "BUMP - Minor irregularity detected",
        "smooth_road": "Road surface is smooth",
        "submit_detection": "Submit Detection",
        "apply_to_segment": "Apply to Segment",
        "simulate_event": "Simulate Event",
        "normal": "Normal",
        "bump": "Bump",
        "pothole": "Pothole",
        "severe": "Severe",
        "language_pref": "Language Preference",
        "display_settings": "Display Settings",
        "settings_saved": "Settings saved!",
        "save_failed": "Failed to save settings",
        "user_info": "User Information",
        "user_id": "User ID",
        "username": "Username",
        "member_since": "Member Since",
        "account_status": "Account Status",
        "active": "Active",
        "welcome": "Welcome to BBP",
        "welcome_subtitle": "Road Condition Monitoring & Route Planning",
        "enter_username": "Enter Username",
        "login_register": "Login / Register",
        "login_hint": "Enter any username to login. New users are automatically registered.",
        "start_lat": "Start Latitude",
        "start_lon": "Start Longitude",
        "end_lat": "End Latitude",
        "end_lon": "End Longitude",
        "search_origin": "Search origin location",
        "search_destination": "Search destination",
        "search_placeholder": "Enter city, address or place name...",
        "search": "Search",
        "click_map_hint": "Click on the map to set location, or drag the markers",
        "origin_marker": "Origin (drag to move)",
        "dest_marker": "Destination (drag to move)",
        "no_results": "No results found",
        "select_location": "Select location",
        "from_location": "From",
        "to_location": "To",
        "sensor_history": "Sensor History",
        "no_sensor_data": "No sensor data recorded yet",
        "recording_time": "Recording Time",
        "acceleration": "Acceleration",
        "altitude": "Altitude",
        "accel_x_label": "X-axis (Left/Right)",
        "accel_y_label": "Y-axis (Forward/Back)",
        "accel_z_label": "Z-axis (Up/Down)",
        "time_samples": "Time (samples)",
        "accel_unit": "Acceleration (m/s2)",
        "search_start": "Search start location",
        "search_end": "Search end location",
        "search_origin_place": "Search origin",
        "search_destination_place": "Search destination",
        "start_point": "Start Point",
        "end_point": "End Point",
        "search_place": "Search place",
        "map_instructions": "Drag markers or click map to adjust locations",
    },
    "zh": {
        "app_title": "BBP 道路监测",
        "dashboard": "仪表板",
        "route_planning": "路线规划",
        "segments": "路段管理",
        "reports": "路况报告",
        "trips": "行程记录",
        "auto_detection": "自动检测",
        "settings": "系统设置",
        "logout": "退出登录",
        "logged_in": "已登录",
        "find_routes": "搜索路线",
        "origin": "起点",
        "destination": "终点",
        "latitude": "纬度",
        "longitude": "经度",
        "save_settings": "保存设置",
        "language": "语言",
        "dark_mode": "深色模式",
        "notifications": "通知",
        "navigation": "导航菜单",
        "total_segments": "路段总数",
        "total_reports": "报告总数",
        "total_trips": "行程总数",
        "active_users": "活跃用户",
        "current_weather": "当前天气",
        "condition": "天气状况",
        "temperature": "温度",
        "wind": "风速",
        "rain_chance": "降雨概率",
        "great_cycling": "非常适合骑行！",
        "check_weather": "骑行前请注意天气状况",
        "plan_route": "使用真实道路数据规划骑行路线",
        "optimization_mode": "优化模式",
        "safety_first": "安全优先",
        "shortest": "最短距离",
        "balanced": "综合平衡",
        "route_details": "路线详情",
        "distance": "距离",
        "duration": "时长",
        "road_quality": "道路质量",
        "tags": "标签",
        "road_segments": "道路路段",
        "segment_list": "路段列表",
        "add_segment": "添加新路段",
        "road_name": "道路名称",
        "status": "状态",
        "obstacle": "障碍物",
        "create_segment": "创建路段",
        "segment_created": "路段创建成功！",
        "no_segments": "暂无路段数据",
        "optimal": "优良",
        "medium": "中等",
        "suboptimal": "较差",
        "maintenance": "维护中",
        "road_reports": "道路状况报告",
        "submit_report": "提交新报告",
        "select_segment": "选择路段",
        "road_condition": "道路状况",
        "notes": "备注",
        "submit": "提交",
        "report_submitted": "报告提交成功！",
        "recent_reports": "最近报告",
        "no_reports": "暂无报告",
        "confirmed": "已确认",
        "confirm_report": "确认",
        "trip_management": "行程管理",
        "start_trip": "开始新行程",
        "create_trip": "创建行程",
        "trip_created": "行程创建成功！",
        "your_trips": "我的行程",
        "trip": "行程",
        "auto_detect_title": "自动道路状况检测",
        "auto_detect_desc": "使用设备传感器实时分析路面状况",
        "current_location": "当前位置",
        "current_speed": "当前速度",
        "sensor_data": "传感器数据",
        "peak_acceleration": "峰值加速度",
        "detection_result": "检测结果",
        "severe_damage": "严重 - 检测到重大道路损坏",
        "pothole_detected": "坑洞 - 检测到道路缺陷",
        "bump_detected": "颠簸 - 检测到轻微不平",
        "smooth_road": "路面平整",
        "submit_detection": "提交检测",
        "apply_to_segment": "应用到路段",
        "simulate_event": "模拟事件",
        "normal": "正常",
        "bump": "颠簸",
        "pothole": "坑洞",
        "severe": "严重",
        "language_pref": "语言偏好",
        "display_settings": "显示设置",
        "settings_saved": "设置保存成功！",
        "save_failed": "保存设置失败",
        "user_info": "用户信息",
        "user_id": "用户 ID",
        "username": "用户名",
        "member_since": "注册时间",
        "account_status": "账户状态",
        "active": "活跃",
        "welcome": "欢迎使用 BBP",
        "welcome_subtitle": "道路状况监测与路线规划系统",
        "enter_username": "输入用户名",
        "login_register": "登录 / 注册",
        "login_hint": "输入任意用户名即可登录，新用户将自动注册。",
        "start_lat": "起点纬度",
        "start_lon": "起点经度",
        "end_lat": "终点纬度",
        "end_lon": "终点经度",
        "search_origin": "搜索起点",
        "search_destination": "搜索终点",
        "search_placeholder": "输入城市、地址或地名...",
        "search": "搜索",
        "click_map_hint": "点击地图设置位置，或拖动标记",
        "origin_marker": "起点（拖动移动）",
        "dest_marker": "终点（拖动移动）",
        "no_results": "未找到结果",
        "select_location": "选择位置",
        "from_location": "从",
        "to_location": "到",
        "sensor_history": "传感器历史",
        "no_sensor_data": "暂无传感器数据",
        "recording_time": "记录时间",
        "acceleration": "加速度",
        "altitude": "海拔",
        "accel_x_label": "X轴（左右方向）",
        "accel_y_label": "Y轴（前后方向）",
        "accel_z_label": "Z轴（上下方向）",
        "time_samples": "时间（采样点）",
        "accel_unit": "加速度 (m/s2)",
        "search_start": "搜索起始位置",
        "search_end": "搜索结束位置",
        "search_origin_place": "搜索起点",
        "search_destination_place": "搜索终点",
        "start_point": "起始点",
        "end_point": "结束点",
        "search_place": "搜索地点",
        "map_instructions": "拖动标记或点击地图调整位置",
    },
    "it": {
        "app_title": "BBP Monitor Stradale",
        "dashboard": "Cruscotto",
        "route_planning": "Pianificazione Percorso",
        "segments": "Segmenti",
        "reports": "Rapporti",
        "trips": "Viaggi",
        "auto_detection": "Rilevamento Auto",
        "settings": "Impostazioni",
        "logout": "Esci",
        "logged_in": "Connesso",
        "find_routes": "Trova Percorsi",
        "origin": "Origine",
        "destination": "Destinazione",
        "latitude": "Latitudine",
        "longitude": "Longitudine",
        "save_settings": "Salva Impostazioni",
        "language": "Lingua",
        "dark_mode": "Modalita Scura",
        "notifications": "Notifiche",
        "navigation": "NAVIGAZIONE",
        "total_segments": "Segmenti Totali",
        "total_reports": "Rapporti Totali",
        "total_trips": "Viaggi Totali",
        "active_users": "Utenti Attivi",
        "current_weather": "Meteo Attuale",
        "condition": "Condizione",
        "temperature": "Temperatura",
        "wind": "Velocita Vento",
        "rain_chance": "Probabilita Pioggia",
        "great_cycling": "Ottime condizioni per il ciclismo!",
        "check_weather": "Controlla le condizioni meteo prima di pedalare",
        "plan_route": "Pianifica il tuo percorso ciclistico",
        "optimization_mode": "Modalita Ottimizzazione",
        "safety_first": "Sicurezza Prima",
        "shortest": "Distanza Minima",
        "balanced": "Bilanciato",
        "route_details": "Dettagli Percorso",
        "distance": "Distanza",
        "duration": "Durata",
        "road_quality": "Qualita Strada",
        "tags": "Tag",
        "road_segments": "Segmenti Stradali",
        "segment_list": "Lista Segmenti",
        "add_segment": "Aggiungi Segmento",
        "road_name": "Nome Strada",
        "status": "Stato",
        "obstacle": "Ostacolo",
        "create_segment": "Crea Segmento",
        "segment_created": "Segmento creato!",
        "no_segments": "Nessun segmento trovato",
        "optimal": "Ottimale",
        "medium": "Medio",
        "suboptimal": "Subottimale",
        "maintenance": "Manutenzione",
        "road_reports": "Rapporti Condizioni Stradali",
        "submit_report": "Invia Rapporto",
        "select_segment": "Seleziona Segmento",
        "road_condition": "Condizione Strada",
        "notes": "Note",
        "submit": "Invia",
        "report_submitted": "Rapporto inviato!",
        "recent_reports": "Rapporti Recenti",
        "no_reports": "Nessun rapporto",
        "confirmed": "Confermato",
        "confirm_report": "Conferma",
        "trip_management": "Gestione Viaggi",
        "start_trip": "Inizia Viaggio",
        "create_trip": "Crea Viaggio",
        "trip_created": "Viaggio creato!",
        "your_trips": "I Tuoi Viaggi",
        "trip": "Viaggio",
        "auto_detect_title": "Rilevamento Automatico Condizioni",
        "auto_detect_desc": "Analisi superficie stradale tramite sensori",
        "current_location": "Posizione Attuale",
        "current_speed": "Velocita Attuale",
        "sensor_data": "Dati Sensore",
        "peak_acceleration": "Accelerazione Massima",
        "detection_result": "Risultato",
        "severe_damage": "GRAVE - Danno stradale importante",
        "pothole_detected": "BUCA - Difetto stradale rilevato",
        "bump_detected": "DOSSO - Irregolarita minore",
        "smooth_road": "Superficie stradale liscia",
        "submit_detection": "Invia Rilevamento",
        "apply_to_segment": "Applica a Segmento",
        "simulate_event": "Simula Evento",
        "normal": "Normale",
        "bump": "Dosso",
        "pothole": "Buca",
        "severe": "Grave",
        "language_pref": "Preferenza Lingua",
        "display_settings": "Impostazioni Display",
        "settings_saved": "Impostazioni salvate!",
        "save_failed": "Impossibile salvare le impostazioni",
        "user_info": "Informazioni Utente",
        "user_id": "ID Utente",
        "username": "Nome Utente",
        "member_since": "Membro Dal",
        "account_status": "Stato Account",
        "active": "Attivo",
        "welcome": "Benvenuto in BBP",
        "welcome_subtitle": "Monitoraggio Condizioni Stradali",
        "enter_username": "Inserisci Nome Utente",
        "login_register": "Accedi / Registrati",
        "login_hint": "Inserisci un nome utente per accedere.",
        "start_lat": "Latitudine Inizio",
        "start_lon": "Longitudine Inizio",
        "end_lat": "Latitudine Fine",
        "end_lon": "Longitudine Fine",
        "search_origin": "Cerca origine",
        "search_destination": "Cerca destinazione",
        "search_placeholder": "Inserisci citta, indirizzo o luogo...",
        "search": "Cerca",
        "click_map_hint": "Clicca sulla mappa o trascina i marcatori",
        "origin_marker": "Origine (trascina)",
        "dest_marker": "Destinazione (trascina)",
        "no_results": "Nessun risultato",
        "select_location": "Seleziona posizione",
        "from_location": "Da",
        "to_location": "A",
        "sensor_history": "Cronologia Sensori",
        "no_sensor_data": "Nessun dato sensore",
        "recording_time": "Ora Registrazione",
        "acceleration": "Accelerazione",
        "altitude": "Altitudine",
        "accel_x_label": "Asse X (Sinistra/Destra)",
        "accel_y_label": "Asse Y (Avanti/Indietro)",
        "accel_z_label": "Asse Z (Su/Giu)",
        "time_samples": "Tempo (campioni)",
        "accel_unit": "Accelerazione (m/s2)",
        "search_start": "Cerca posizione inizio",
        "search_end": "Cerca posizione fine",
        "search_origin_place": "Cerca origine",
        "search_destination_place": "Cerca destinazione",
        "start_point": "Punto Iniziale",
        "end_point": "Punto Finale",
        "search_place": "Cerca luogo",
        "map_instructions": "Trascina i marcatori o clicca sulla mappa",
    }
}

def t(key: str) -> str:
    """Translate a key to current language."""
    lang = st.session_state.get("language", "en")
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

# ============== Session State ==============
if "user" not in st.session_state:
    st.session_state.user = None
if "language" not in st.session_state:
    st.session_state.language = "en"
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "gps_lat" not in st.session_state:
    st.session_state.gps_lat = 45.4642
if "gps_lon" not in st.session_state:
    st.session_state.gps_lon = 9.1900
if "origin_lat" not in st.session_state:
    st.session_state.origin_lat = 45.4781
if "origin_lon" not in st.session_state:
    st.session_state.origin_lon = 9.2275
if "dest_lat" not in st.session_state:
    st.session_state.dest_lat = 45.4642
if "dest_lon" not in st.session_state:
    st.session_state.dest_lon = 9.1900
if "sensor_readings" not in st.session_state:
    st.session_state.sensor_readings = []

# ============== Dynamic CSS - Gemini Style ==============
if st.session_state.dark_mode:
    st.markdown("""
    <style>
        .stApp { background-color: #131314 !important; }
        .stApp, .stApp p, .stApp span, .stApp label, .stApp div { color: #e3e3e3 !important; }
        h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
        [data-testid="stSidebar"] { background-color: #1e1f20 !important; border-right: 1px solid #3c4043 !important; }
        [data-testid="stSidebar"] * { color: #e3e3e3 !important; }
        .stTextInput input, .stSelectbox > div > div, .stNumberInput input {
            background-color: #2d2e2f !important; color: #e3e3e3 !important; border: 1px solid #3c4043 !important; border-radius: 8px !important;
        }
        .stButton > button { background-color: #8ab4f8 !important; color: #202124 !important; border: none !important; border-radius: 20px !important; }
        .stButton > button:hover { background-color: #aecbfa !important; }
        .stButton > button[kind="secondary"] { background-color: transparent !important; color: #8ab4f8 !important; border: 1px solid #3c4043 !important; }
        [data-testid="stMetric"] { background-color: #2d2e2f !important; padding: 16px !important; border-radius: 12px !important; border: 1px solid #3c4043 !important; }
        [data-testid="stMetricLabel"] { color: #9aa0a6 !important; }
        [data-testid="stMetricValue"] { color: #e3e3e3 !important; }
        .streamlit-expanderHeader { background-color: #2d2e2f !important; color: #e3e3e3 !important; }
        hr { border-color: #3c4043 !important; }
        .user-card { background: #2d2e2f; border: 1px solid #3c4043; border-radius: 12px; padding: 20px; margin: 16px 0; }
        .user-card h4 { color: #e3e3e3 !important; margin: 0 0 4px 0; }
        .user-card p { color: #9aa0a6 !important; margin: 0; font-size: 0.9rem; }
        .info-table { width: 100%; border-collapse: collapse; }
        .info-table td { padding: 12px 0; border-bottom: 1px solid #3c4043; color: #e3e3e3; }
        .info-table td:last-child { text-align: right; }
        /* Sidebar toggle button - make VERY visible with bright color */
        [data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"],
        [data-testid="stSidebarNavCollapseIcon"], button[aria-label="Collapse sidebar"],
        button[aria-label="Expand sidebar"] {
            background-color: #8ab4f8 !important;
            border-radius: 8px !important;
            padding: 8px !important;
            min-width: 40px !important;
            min-height: 40px !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg, [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarNavCollapseIcon"] svg,
        button[aria-label="Collapse sidebar"] svg, button[aria-label="Expand sidebar"] svg {
            stroke: #1a1a1a !important;
            fill: #1a1a1a !important;
            width: 28px !important;
            height: 28px !important;
        }
        button[kind="header"] svg, .stApp header button svg {
            stroke: #ffffff !important;
            fill: #ffffff !important;
            width: 24px !important;
            height: 24px !important;
        }
        /* Header buttons (Fork, Star, etc.) */
        .stApp header, [data-testid="stHeader"] {
            background-color: #1e1f20 !important;
        }
        .stApp header button, [data-testid="stHeader"] button,
        [data-testid="stToolbar"] button {
            background-color: #5f6368 !important;
            color: #ffffff !important;
            border: 1px solid #8ab4f8 !important;
            border-radius: 6px !important;
        }
        .stApp header button:hover, [data-testid="stHeader"] button:hover,
        [data-testid="stToolbar"] button:hover {
            background-color: #8ab4f8 !important;
            color: #1a1a1a !important;
        }
        /* Toolbar/menu area */
        [data-testid="stToolbar"] {
            background-color: #1e1f20 !important;
        }
        [data-testid="stToolbar"] svg {
            stroke: #ffffff !important;
            fill: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp { background-color: #ffffff !important; }
        .stApp, .stApp p, .stApp span, .stApp label, .stApp div { color: #1f1f1f !important; }
        h1, h2, h3, h4, h5, h6 { color: #1f1f1f !important; }
        [data-testid="stSidebar"] { background-color: #f8f9fa !important; border-right: 1px solid #e0e0e0 !important; }
        [data-testid="stSidebar"] * { color: #1f1f1f !important; }
        .stTextInput input, .stSelectbox > div > div, .stNumberInput input {
            background-color: #ffffff !important; color: #1f1f1f !important; border: 1px solid #dadce0 !important; border-radius: 8px !important;
        }
        .stButton > button { background-color: #1a73e8 !important; color: #ffffff !important; border: none !important; border-radius: 20px !important; }
        .stButton > button:hover { background-color: #1557b0 !important; }
        .stButton > button[kind="secondary"] { background-color: transparent !important; color: #1a73e8 !important; border: 1px solid #dadce0 !important; }
        [data-testid="stMetric"] { background-color: #f8f9fa !important; padding: 16px !important; border-radius: 12px !important; border: 1px solid #e0e0e0 !important; }
        [data-testid="stMetricLabel"] { color: #5f6368 !important; }
        [data-testid="stMetricValue"] { color: #1f1f1f !important; }
        .streamlit-expanderHeader { background-color: #f8f9fa !important; color: #1f1f1f !important; }
        hr { border-color: #e0e0e0 !important; }
        .user-card { background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 12px; padding: 20px; margin: 16px 0; }
        .user-card h4 { color: #1f1f1f !important; margin: 0 0 4px 0; }
        .user-card p { color: #5f6368 !important; margin: 0; font-size: 0.9rem; }
        .info-table { width: 100%; border-collapse: collapse; }
        .info-table td { padding: 12px 0; border-bottom: 1px solid #e0e0e0; color: #1f1f1f; }
        .info-table td:last-child { text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# ============== Sidebar ==============
with st.sidebar:
    st.markdown(f"### {t('app_title')}")
    
    # Language selector
    st.markdown(f"**{t('language')}**")
    lang_options = ["en", "zh", "it"]
    lang_labels = {"en": "English", "zh": "中文", "it": "Italiano"}
    current_lang_idx = lang_options.index(st.session_state.language) if st.session_state.language in lang_options else 0
    
    new_lang = st.selectbox(
        t("language"),
        options=lang_options,
        format_func=lambda x: lang_labels[x],
        index=current_lang_idx,
        key="lang_selector",
        label_visibility="collapsed"
    )
    
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        if st.session_state.user:
            api_patch(f"/api/users/{st.session_state.user['id']}/settings", {"language": new_lang})
        st.rerun()

# ============== Login Section ==============
if st.session_state.user is None:
    st.title(t("welcome"))
    st.markdown(f"### {t('welcome_subtitle')}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("---")
        username = st.text_input(t("enter_username"), placeholder="e.g., alice")
        
        if st.button(t("login_register"), use_container_width=True):
            if username.strip():
                result = api_post("/api/users", {"username": username.strip()})
                if result:
                    st.session_state.user = result
                    settings = api_get(f"/api/users/{result['id']}/settings")
                    if settings:
                        st.session_state.language = settings.get("language", "en")
                        st.session_state.dark_mode = settings.get("dark_mode", False)
                    st.rerun()
            else:
                st.warning(t("enter_username"))
        
        st.markdown("---")
        st.info(t("login_hint"))
    
    st.stop()

# ============== Main App (After Login) ==============
user = st.session_state.user
user_id = user["id"]

# Sidebar navigation
with st.sidebar:
    # User profile card
    st.markdown(f"""
    <div class="user-card">
        <h4>{user['username']}</h4>
        <p>{t('logged_in')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(t("logout"), use_container_width=True):
        st.session_state.user = None
        st.session_state.dark_mode = False
        st.session_state.language = "en"
        st.rerun()
    
    st.markdown("---")
    st.markdown(f"**{t('navigation')}**")
    
    # Navigation items without emoji
    nav_items = [
        ("dashboard", "Dashboard"),
        ("route_planning", "Route Planning"),
        ("segments", "Segments"),
        ("reports", "Reports"),
        ("trips", "Trips"),
        ("auto_detection", "Auto Detection"),
        ("settings", "Settings")
    ]
    
    for key, internal_name in nav_items:
        display_name = t(key)
        is_active = st.session_state.current_page == internal_name
        
        if st.button(
            display_name,
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = internal_name
            st.rerun()

menu = st.session_state.current_page

# ============== Dashboard ==============
if menu == "Dashboard":
    st.title(t("dashboard"))
    
    stats = api_get("/api/stats", {"user_id": user_id})
    
    if stats:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(t("total_segments"), stats.get("total_segments", 0))
        col2.metric(t("total_reports"), stats.get("total_reports", 0))
        col3.metric(t("total_trips"), stats.get("total_trips", 0))
        col4.metric(t("active_users"), stats.get("active_users", 0))
        
        st.markdown("---")
        
        st.subheader(t("current_weather"))
        weather = api_get("/api/weather", {"lat": 45.478, "lon": 9.227, "user_id": user_id})
        if weather:
            wcol1, wcol2, wcol3, wcol4 = st.columns(4)
            wcol1.metric(t("condition"), weather.get("condition_localized", "N/A"))
            wcol2.metric(t("temperature"), f"{weather.get('temperature_c', 'N/A')}C")
            wcol3.metric(t("wind"), f"{weather.get('wind_speed_kmh', 'N/A')} km/h")
            wcol4.metric(t("rain_chance"), f"{weather.get('rain_chance_percent', 'N/A')}%")
            
            if weather.get("is_cycling_friendly"):
                st.success(t("great_cycling"))
            else:
                st.warning(t("check_weather"))

# ============== Route Planning ==============
elif menu == "Route Planning":
    st.title(t("route_planning"))
    st.markdown(t("plan_route"))
    
    # Search boxes for origin and destination
    col_search1, col_search2 = st.columns(2)
    
    with col_search1:
        st.subheader(t("origin"))
        origin_query = st.text_input(t("search_origin"), placeholder=t("search_placeholder"), key="origin_search")
        if st.button(t("search"), key="search_origin_btn"):
            if origin_query:
                results = geocode_place(origin_query)
                if results:
                    st.session_state.origin_results = results
                else:
                    st.warning(t("no_results"))
        
        if "origin_results" in st.session_state and st.session_state.origin_results:
            options = {i: r.get("display_name", "")[:60] for i, r in enumerate(st.session_state.origin_results)}
            selected = st.selectbox(t("select_location"), options.keys(), format_func=lambda x: options[x], key="origin_select")
            if selected is not None:
                r = st.session_state.origin_results[selected]
                st.session_state.origin_lat = float(r["lat"])
                st.session_state.origin_lon = float(r["lon"])
        
        st.caption(f"{t('latitude')}: {st.session_state.origin_lat:.4f}, {t('longitude')}: {st.session_state.origin_lon:.4f}")
    
    with col_search2:
        st.subheader(t("destination"))
        dest_query = st.text_input(t("search_destination"), placeholder=t("search_placeholder"), key="dest_search")
        if st.button(t("search"), key="search_dest_btn"):
            if dest_query:
                results = geocode_place(dest_query)
                if results:
                    st.session_state.dest_results = results
                else:
                    st.warning(t("no_results"))
        
        if "dest_results" in st.session_state and st.session_state.dest_results:
            options = {i: r.get("display_name", "")[:60] for i, r in enumerate(st.session_state.dest_results)}
            selected = st.selectbox(t("select_location"), options.keys(), format_func=lambda x: options[x], key="dest_select")
            if selected is not None:
                r = st.session_state.dest_results[selected]
                st.session_state.dest_lat = float(r["lat"])
                st.session_state.dest_lon = float(r["lon"])
        
        st.caption(f"{t('latitude')}: {st.session_state.dest_lat:.4f}, {t('longitude')}: {st.session_state.dest_lon:.4f}")
    
    st.info(t("click_map_hint"))
    
    # Interactive map with draggable markers
    center_lat = (st.session_state.origin_lat + st.session_state.dest_lat) / 2
    center_lon = (st.session_state.origin_lon + st.session_state.dest_lon) / 2
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    # Add draggable markers
    folium.Marker(
        [st.session_state.origin_lat, st.session_state.origin_lon],
        popup=t("origin_marker"),
        icon=folium.Icon(color="green", icon="play"),
        draggable=True
    ).add_to(m)
    
    folium.Marker(
        [st.session_state.dest_lat, st.session_state.dest_lon],
        popup=t("dest_marker"),
        icon=folium.Icon(color="red", icon="stop"),
        draggable=True
    ).add_to(m)
    
    # Draw line between points
    folium.PolyLine(
        [[st.session_state.origin_lat, st.session_state.origin_lon],
         [st.session_state.dest_lat, st.session_state.dest_lon]],
        color="blue", weight=2, opacity=0.5, dash_array="5"
    ).add_to(m)
    
    map_data = st_folium(m, width=700, height=400, returned_objects=["last_clicked"])
    
    # Handle map clicks to update markers
    if map_data and map_data.get("last_clicked"):
        clicked = map_data["last_clicked"]
        click_lat = clicked["lat"]
        click_lon = clicked["lng"]
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button(f"{t('origin')}: {click_lat:.4f}, {click_lon:.4f}", key="set_origin"):
                st.session_state.origin_lat = click_lat
                st.session_state.origin_lon = click_lon
                st.rerun()
        with col_btn2:
            if st.button(f"{t('destination')}: {click_lat:.4f}, {click_lon:.4f}", key="set_dest"):
                st.session_state.dest_lat = click_lat
                st.session_state.dest_lon = click_lon
                st.rerun()
    
    st.markdown("---")
    
    mode = st.selectbox(
        t("optimization_mode"),
        ["safety_first", "shortest", "balanced"],
        format_func=lambda x: t(x)
    )
    
    if st.button(t("find_routes"), use_container_width=True):
        from_lat = st.session_state.origin_lat
        from_lon = st.session_state.origin_lon
        to_lat = st.session_state.dest_lat
        to_lon = st.session_state.dest_lon
        
        with st.spinner("..."):
            routes = api_post("/api/path/search", {
                "origin": {"lat": from_lat, "lon": from_lon},
                "destination": {"lat": to_lat, "lon": to_lon},
                "preferences": mode
            }, {"user_id": user_id})
            
            if routes and routes.get("routes"):
                st.success(f"{t('route_details')}: {len(routes['routes'])}")
                
                if routes.get("weather_summary"):
                    st.info(routes['weather_summary'])
                if routes.get("cycling_recommendation"):
                    st.write(routes['cycling_recommendation'])
                
                route_map = folium.Map(location=[(from_lat + to_lat)/2, (from_lon + to_lon)/2], zoom_start=14)
                folium.Marker([from_lat, from_lon], popup=t("origin"), icon=folium.Icon(color="green")).add_to(route_map)
                folium.Marker([to_lat, to_lon], popup=t("destination"), icon=folium.Icon(color="red")).add_to(route_map)
                
                colors = ["blue", "purple", "orange", "darkgreen", "darkred"]
                for i, route in enumerate(routes["routes"][:5]):
                    geojson = route.get("geometry_geojson", {})
                    coords = geojson.get("coordinates", [])
                    if coords:
                        latlon_coords = [[c[1], c[0]] for c in coords]
                        folium.PolyLine(
                            latlon_coords,
                            color=colors[i % len(colors)],
                            weight=4 if i == 0 else 3,
                            opacity=0.8 if i == 0 else 0.5,
                            popup=f"Route {route.get('route_id', i+1)}"
                        ).add_to(route_map)
                
                st_folium(route_map, width=700, height=500, returned_objects=[])
                
                st.subheader(t("route_details"))
                for i, route in enumerate(routes["routes"][:5]):
                    tags_display = ", ".join(route.get("tags_localized", route.get("tags", [])))
                    with st.expander(f"Route {route.get('route_id', i+1)}: {tags_display}", expanded=(i==0)):
                        rcol1, rcol2, rcol3 = st.columns(3)
                        distance_km = route.get('total_distance', 0) / 1000
                        rcol1.metric(t("distance"), f"{distance_km:.2f} km")
                        rcol2.metric(t("duration"), route.get("duration_display", "N/A"))
                        rcol3.metric(t("road_quality"), f"{route.get('road_quality_score', 0):.0f}/100")
                        
                        tags = route.get("tags", [])
                        if tags:
                            st.write(f"**{t('tags')}:** {', '.join(tags)}")
                        
                        warnings = route.get("segments_warning_localized", route.get("segments_warning", []))
                        if warnings:
                            st.warning(f"{len(warnings)} warnings")

# ============== Segments ==============
elif menu == "Segments":
    st.title(t("road_segments"))
    
    col_map, col_form = st.columns([2, 1])
    
    with col_map:
        segments = api_get("/api/segments", {"user_id": user_id})
        
        if segments and len(segments) > 0:
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
            
            st_folium(m, width=None, height=400, returned_objects=[])
            
            st.subheader(t("segment_list"))
            df = pd.DataFrame([{
                "ID": s["id"],
                t("road_name"): get_seg_name(s),
                t("status"): s.get("status_localized", s.get("status", "unknown")),
                t("obstacle"): s.get("obstacle", "-") or "-"
            } for s in segments])
            st.dataframe(df, use_container_width=True)
        else:
            st.info(t("no_segments"))
    
    with col_form:
        st.subheader(t("add_segment"))
        
        # Initialize segment coordinates in session state
        if "seg_start_lat" not in st.session_state:
            st.session_state.seg_start_lat = 45.478
        if "seg_start_lon" not in st.session_state:
            st.session_state.seg_start_lon = 9.227
        if "seg_end_lat" not in st.session_state:
            st.session_state.seg_end_lat = 45.479
        if "seg_end_lon" not in st.session_state:
            st.session_state.seg_end_lon = 9.228
        
        seg_name = st.text_input(t("road_name"), placeholder="e.g., Via Roma", key="seg_name_input")
        
        # Start point place search
        st.markdown(f"**{t('start_point')}**")
        seg_start_search = st.text_input(t("search_place"), key="seg_start_search", placeholder="e.g., Via Roma 1, Milano")
        if st.button(t("search"), key="seg_start_btn"):
            coords = geocode_place(seg_start_search)
            if coords:
                st.session_state.seg_start_lat = coords[0]
                st.session_state.seg_start_lon = coords[1]
                st.success(f"✓ {coords[0]:.4f}, {coords[1]:.4f}")
            else:
                st.error(t("place_not_found"))
        st.caption(f"{st.session_state.seg_start_lat:.4f}, {st.session_state.seg_start_lon:.4f}")
        
        # End point place search
        st.markdown(f"**{t('end_point')}**")
        seg_end_search = st.text_input(t("search_place"), key="seg_end_search", placeholder="e.g., Via Roma 100, Milano")
        if st.button(t("search"), key="seg_end_btn"):
            coords = geocode_place(seg_end_search)
            if coords:
                st.session_state.seg_end_lat = coords[0]
                st.session_state.seg_end_lon = coords[1]
                st.success(f"✓ {coords[0]:.4f}, {coords[1]:.4f}")
            else:
                st.error(t("place_not_found"))
        st.caption(f"{st.session_state.seg_end_lat:.4f}, {st.session_state.seg_end_lon:.4f}")
        
        status_options = ["optimal", "medium", "suboptimal", "maintenance"]
        seg_status = st.selectbox(t("status"), status_options, format_func=lambda x: t(x), key="seg_status_select")
        obstacle = st.text_input(t("obstacle"), placeholder="e.g., pothole", key="seg_obstacle_input")
        
        if st.button(t("create_segment"), use_container_width=True, type="primary"):
            result = api_post("/api/segments", {
                "user_id": user_id,
                "road_name": seg_name,
                "start_lat": st.session_state.seg_start_lat,
                "start_lon": st.session_state.seg_start_lon,
                "end_lat": st.session_state.seg_end_lat,
                "end_lon": st.session_state.seg_end_lon,
                "status": seg_status,
                "obstacle": obstacle if obstacle else None
            })
            if result:
                st.success(t("segment_created"))
                st.rerun()

# ============== Reports ==============
elif menu == "Reports":
    st.title(t("road_reports"))
    
    segments = api_get("/api/segments", {"user_id": user_id})
    
    if segments:
        segment_options = {s["id"]: f"{get_seg_name(s)} (ID: {s['id']})" for s in segments}
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(t("submit_report"))
            with st.form("submit_report_form"):
                segment_id = st.selectbox(
                    t("select_segment"),
                    options=list(segment_options.keys()),
                    format_func=lambda x: segment_options[x]
                )
                
                condition = st.select_slider(
                    t("road_condition"),
                    options=["suboptimal", "medium", "optimal"],
                    value="medium",
                    format_func=lambda x: t(x)
                )
                
                note = st.text_area(t("notes"), placeholder="...")
                
                if st.form_submit_button(t("submit")):
                    result = api_post(f"/api/segments/{segment_id}/reports", {
                        "user_id": user_id,
                        "note": note
                    })
                    if result:
                        st.success(t("report_submitted"))
                        st.rerun()
        
        with col2:
            st.subheader(t("recent_reports"))
            
            selected_seg = st.selectbox(
                t("select_segment"),
                options=list(segment_options.keys()),
                format_func=lambda x: segment_options[x],
                key="view_reports_seg"
            )
            
            reports = api_get(f"/api/segments/{selected_seg}/reports")
            if reports:
                for report in reports[:10]:
                    with st.container():
                        st.markdown(f"**{report.get('note', '-')}**")
                        rcol1, rcol2 = st.columns(2)
                        rcol1.write(f"ID: {report.get('id', 'N/A')}")
                        status = "Yes" if report.get('confirmed') else "No"
                        rcol2.write(f"{t('confirmed')}: {status}")
                        
                        if not report.get("confirmed"):
                            if st.button(f"{t('confirm_report')} #{report['id']}", key=f"confirm_{report['id']}"):
                                api_post(f"/api/reports/{report['id']}/confirm", {"user_id": user_id})
                                st.rerun()
                        st.markdown("---")
            else:
                st.info(t("no_reports"))

# ============== Trips ==============
elif menu == "Trips":
    st.title(t("trip_management"))
    
    # Initialize trip coordinates in session state
    if "trip_from_lat" not in st.session_state:
        st.session_state.trip_from_lat = 45.478
    if "trip_from_lon" not in st.session_state:
        st.session_state.trip_from_lon = 9.227
    if "trip_to_lat" not in st.session_state:
        st.session_state.trip_to_lat = 45.464
    if "trip_to_lon" not in st.session_state:
        st.session_state.trip_to_lon = 9.190
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(t("start_trip"))
        
        # Origin place search
        st.markdown(f"**{t('origin')}**")
        trip_origin_search = st.text_input(t("search_origin_place"), key="trip_origin_search", placeholder="e.g., Milano Centrale")
        if st.button(t("search"), key="trip_origin_btn"):
            coords = geocode_place(trip_origin_search)
            if coords:
                st.session_state.trip_from_lat = coords[0]
                st.session_state.trip_from_lon = coords[1]
                st.success(f"✓ {coords[0]:.4f}, {coords[1]:.4f}")
            else:
                st.error(t("place_not_found"))
        
        # Destination place search
        st.markdown(f"**{t('destination')}**")
        trip_dest_search = st.text_input(t("search_destination_place"), key="trip_dest_search", placeholder="e.g., Duomo Milano")
        if st.button(t("search"), key="trip_dest_btn"):
            coords = geocode_place(trip_dest_search)
            if coords:
                st.session_state.trip_to_lat = coords[0]
                st.session_state.trip_to_lon = coords[1]
                st.success(f"✓ {coords[0]:.4f}, {coords[1]:.4f}")
            else:
                st.error(t("place_not_found"))
        
        # Map for trip start/end with draggable markers
        st.markdown(f"**{t('map_instructions')}**")
        trip_map = folium.Map(
            location=[(st.session_state.trip_from_lat + st.session_state.trip_to_lat)/2, 
                      (st.session_state.trip_from_lon + st.session_state.trip_to_lon)/2], 
            zoom_start=12
        )
        
        # Origin marker (green)
        folium.Marker(
            [st.session_state.trip_from_lat, st.session_state.trip_from_lon],
            popup=t("origin"),
            icon=folium.Icon(color="green", icon="play"),
            draggable=True
        ).add_to(trip_map)
        
        # Destination marker (red)
        folium.Marker(
            [st.session_state.trip_to_lat, st.session_state.trip_to_lon],
            popup=t("destination"),
            icon=folium.Icon(color="red", icon="flag"),
            draggable=True
        ).add_to(trip_map)
        
        # Draw line between origin and destination
        folium.PolyLine(
            [[st.session_state.trip_from_lat, st.session_state.trip_from_lon],
             [st.session_state.trip_to_lat, st.session_state.trip_to_lon]],
            color="blue",
            weight=3,
            opacity=0.7,
            dash_array="5"
        ).add_to(trip_map)
        
        trip_map_data = st_folium(trip_map, width=None, height=300, returned_objects=["all_drawings"], key="trip_map")
        
        # Update coordinates if marker was dragged
        if trip_map_data and "last_object_clicked" in trip_map_data and trip_map_data["last_object_clicked"]:
            clicked = trip_map_data["last_object_clicked"]
            if "lat" in clicked and "lng" in clicked:
                # Update origin if click is closer to origin
                dist_to_origin = abs(clicked["lat"] - st.session_state.trip_from_lat) + abs(clicked["lng"] - st.session_state.trip_from_lon)
                dist_to_dest = abs(clicked["lat"] - st.session_state.trip_to_lat) + abs(clicked["lng"] - st.session_state.trip_to_lon)
                if dist_to_origin < dist_to_dest:
                    st.session_state.trip_from_lat = clicked["lat"]
                    st.session_state.trip_from_lon = clicked["lng"]
                else:
                    st.session_state.trip_to_lat = clicked["lat"]
                    st.session_state.trip_to_lon = clicked["lng"]
        
        # Show current coordinates
        st.caption(f"{t('origin')}: {st.session_state.trip_from_lat:.4f}, {st.session_state.trip_from_lon:.4f}")
        st.caption(f"{t('destination')}: {st.session_state.trip_to_lat:.4f}, {st.session_state.trip_to_lon:.4f}")
        
        if st.button(t("create_trip"), use_container_width=True, type="primary"):
            result = api_post("/api/trips", {
                "user_id": user_id,
                "from_lat": st.session_state.trip_from_lat,
                "from_lon": st.session_state.trip_from_lon,
                "to_lat": st.session_state.trip_to_lat,
                "to_lon": st.session_state.trip_to_lon
            })
            if result:
                st.success(t("trip_created"))
                st.rerun()
    
    with col2:
        st.subheader(t("your_trips"))
        trips = api_get("/api/trips", {"user_id": user_id})
        if trips:
            for trip in trips[:10]:
                created = trip.get('created_at', 'N/A')
                if created and len(created) >= 10:
                    created = created[:10]
                with st.expander(f"{t('trip')} #{trip['id']} - {created}"):
                    tcol1, tcol2, tcol3 = st.columns(3)
                    tcol1.metric(t("distance"), f"{trip.get('distance_km', 0):.2f} km")
                    tcol2.metric(t("duration"), trip.get("duration_str", "N/A"))
                    tcol3.metric(t("status"), trip.get("status", "N/A"))

# ============== Auto Detection ==============
elif menu == "Auto Detection":
    st.title(t("auto_detect_title"))
    st.markdown(t("auto_detect_desc"))
    
    st.subheader(t("current_location"))
    gps_html = """
    <div style="padding: 15px; border-radius: 8px; background: #f5f5f5; margin: 10px 0;">
        <div id="status">Requesting location...</div>
        <div id="data" style="display: none; margin-top: 10px;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div><strong>Lat:</strong> <span id="lat">--</span></div>
                <div><strong>Lon:</strong> <span id="lon">--</span></div>
                <div><strong>Speed:</strong> <span id="speed">--</span> km/h</div>
                <div><strong>Altitude:</strong> <span id="alt">--</span> m</div>
            </div>
        </div>
    </div>
    <script>
        if (navigator.geolocation) {
            navigator.geolocation.watchPosition(
                function(p) {
                    document.getElementById('status').innerHTML = '<span style="color:green;">GPS Active</span>';
                    document.getElementById('data').style.display = 'block';
                    document.getElementById('lat').textContent = p.coords.latitude.toFixed(6);
                    document.getElementById('lon').textContent = p.coords.longitude.toFixed(6);
                    document.getElementById('speed').textContent = p.coords.speed ? (p.coords.speed * 3.6).toFixed(1) : '0';
                    document.getElementById('alt').textContent = p.coords.altitude ? p.coords.altitude.toFixed(1) : 'N/A';
                },
                function(e) { document.getElementById('status').textContent = e.message; },
                { enableHighAccuracy: true, timeout: 10000 }
            );
        }
    </script>
    """
    st.components.v1.html(gps_html, height=130)
    
    st.markdown("---")
    st.subheader(t("sensor_data"))
    
    # Show axis legend
    st.markdown(f"""
    **{t('accel_x_label')}** | **{t('accel_y_label')}** | **{t('accel_z_label')}**
    """)
    
    # Fetch recorded sensor data from backend
    sensor_history = api_get("/api/sensor-readings", {"user_id": user_id})
    
    if sensor_history and len(sensor_history) > 0:
        # Use real recorded data
        recent_readings = sensor_history[-50:] if len(sensor_history) > 50 else sensor_history
        sensor_data = pd.DataFrame([{
            f'X ({t("accel_x_label")[:10]})': r.get('acceleration_x', 0),
            f'Y ({t("accel_y_label")[:10]})': r.get('acceleration_y', 0),
            f'Z ({t("accel_z_label")[:10]})': r.get('acceleration_z', 0)
        } for r in recent_readings])
        
        st.line_chart(sensor_data)
        max_accel = sensor_data.abs().max().max()
        
        # Show history table
        with st.expander(t("sensor_history")):
            history_df = pd.DataFrame([{
                t("recording_time"): r.get('timestamp', 'N/A')[:19] if r.get('timestamp') else 'N/A',
                'X': f"{r.get('acceleration_x', 0):.2f}",
                'Y': f"{r.get('acceleration_y', 0):.2f}",
                'Z': f"{r.get('acceleration_z', 0):.2f}",
                t("detection_result"): r.get('severity', '-')
            } for r in reversed(recent_readings[-20:])])
            st.dataframe(history_df, use_container_width=True)
    else:
        st.info(t("no_sensor_data"))
        # Generate sample data for demo if no recorded data
        np.random.seed(int(time.time()) % 1000)
        sensor_data = pd.DataFrame(np.random.randn(50, 3) * 0.5, columns=[
            f'X ({t("accel_x_label")[:10]})',
            f'Y ({t("accel_y_label")[:10]})',
            f'Z ({t("accel_z_label")[:10]})'
        ])
        st.line_chart(sensor_data)
        max_accel = sensor_data.abs().max().max()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(t("peak_acceleration"), f"{max_accel:.2f} m/s2")
    with col2:
        if max_accel > 25:
            st.error(t("severe_damage"))
            detected = "severe"
        elif max_accel > 15:
            st.warning(t("pothole_detected"))
            detected = "pothole"
        elif max_accel > 8:
            st.info(t("bump_detected"))
            detected = "bump"
        else:
            st.success(t("smooth_road"))
            detected = "smooth"
    
    st.markdown("---")
    st.subheader(t("submit_detection"))
    
    segments = api_get("/api/segments", {"user_id": user_id})
    if segments:
        segment_options = {s["id"]: f"{get_seg_name(s)} (ID: {s['id']})" for s in segments}
        segment_id = st.selectbox(t("apply_to_segment"), options=list(segment_options.keys()), format_func=lambda x: segment_options[x])
        
        if st.button(t("submit_detection"), key="submit_det_btn"):
            reading = {
                "acceleration_x": float(sensor_data["Accel_X"].iloc[-1]) if len(sensor_data) > 0 else 0,
                "acceleration_y": float(sensor_data["Accel_Y"].iloc[-1]) if len(sensor_data) > 0 else 0,
                "acceleration_z": float(sensor_data["Accel_Z"].iloc[-1]) if len(sensor_data) > 0 else 0,
                "speed_mps": 5.0,
                "gps_accuracy_m": 5.0
            }
            result = api_post(f"/api/segments/{segment_id}/auto-detect", reading)
            if result:
                st.success(f"{t('submit_detection')}: {result.get('severity', detected)}")

# ============== Settings ==============
elif menu == "Settings":
    st.title(t("settings"))
    
    # Fetch current settings from backend
    settings = api_get(f"/api/users/{user_id}/settings")
    if settings:
        # Sync session state with backend settings (but don't override language - that's controlled by sidebar)
        st.session_state.dark_mode = settings.get("dark_mode", False)
    
    # Note: Language selector is in the sidebar, not here to avoid duplication
    
    st.subheader(t("dark_mode"))
    dark_mode = st.toggle(t("dark_mode"), value=st.session_state.dark_mode)
    
    st.subheader(t("notifications"))
    notifications = st.toggle(t("notifications"), value=settings.get("notifications_enabled", True) if settings else True)
    
    if st.button(t("save_settings"), use_container_width=True):
        # Use PATCH to update settings - use current language from session state
        result = api_patch(f"/api/users/{user_id}/settings", {
            "language": st.session_state.language,
            "dark_mode": dark_mode,
            "notifications_enabled": notifications
        })
        if result:
            # Update session state immediately
            st.session_state.dark_mode = dark_mode
            st.success(t("settings_saved"))
            st.rerun()
        else:
            st.error(t("save_failed"))
    
    st.markdown("---")
    st.subheader(t("user_info"))
    
    # Display user info in a nice table format
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.markdown(f"**{t('user_id')}**")
        st.write(user.get('id', 'N/A'))
        
        st.markdown(f"**{t('username')}**")
        st.write(user.get('username', 'N/A'))
    
    with info_col2:
        st.markdown(f"**{t('member_since')}**")
        created = user.get('created_at', 'N/A')
        if created and len(created) >= 10:
            created = created[:10]
        st.write(created)
        
        st.markdown(f"**{t('account_status')}**")
        st.write(t("active"))

# ============== Footer ==============
st.sidebar.markdown("---")
st.sidebar.caption("BBP Road Monitor v2.0")
st.sidebar.caption(f"Backend: {BACKEND_URL}")
