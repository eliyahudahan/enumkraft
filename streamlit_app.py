import streamlit as st
import requests
import time
import pandas as pd
import pydeck as pdk
import os
from dotenv import load_dotenv

# Load .env (only if it exists)
load_dotenv()

st.set_page_config(page_title="EnumKraft 2.0", layout="wide")

st.title("⚡ EnumKraft 2.0 – Grid Stability Dashboard")
st.caption("Live data from FastAPI + Gridradar + Swing Equation")

# ============================================
# Demo Data – Fallback
# ============================================
def get_demo_data():
    """Fallback data when API is unavailable"""
    return {
        "frequency_hz": 49.98,
        "load_mw": 52000,
        "cf_48h": 0.05,
        "temperature": 18.1,
        "stability_status": "⚠️ DUNKELFLAUTE",
        "action": "Standby backup",
        "source": "Demo Mode (No API)"
    }

# ============================================
# API URL – Local or Cloud
# ============================================
API_URL = os.getenv("API_URL", None)

# ============================================
# Data Decoding – Live or Demo
# ============================================
def fetch_data():
    if API_URL:
        try:
            response = requests.get(f"{API_URL}/api/v1/grid/stability", timeout=5)
            if response.status_code == 200:
                return response.json(), "Live API"
        except:
            pass
    
    # Fallback to Demo
    return get_demo_data(), "Demo Mode (No API)"

# ============================================
# Display the dashboard
# ============================================
placeholder = st.empty()

while True:
    data, source_label = fetch_data()
    
    with placeholder.container():
        st.caption(f"📡 Data source: {source_label}")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("📡 Frequency", f"{data.get('frequency_hz', 50.0):.3f} Hz")
        col2.metric("⚡ Load", f"{data.get('load_mw', 50000):.0f} MW")
        col3.metric("🌤️ CF", f"{data.get('cf_48h', 0.0):.4f}")
        col4.metric("🌡️ Temperature", f"{data.get('temperature', 18.1)}°C")
        col5.metric("📈 Forecast (24h)", "57,000 MW")
        
        status = data.get('stability_status', 'NORMAL')
        if "EMERGENCY" in status:
            st.error(f"🚨 {status}")
        elif "CRITICAL" in status:
            st.warning(f"⚠️ {status}")
        elif "DUNKELFLAUTE" in status:
            st.warning(f"⚠️ {status}")
        else:
            st.success(f"✅ {status}")
        
        # 🗺️ Germany Map
        st.subheader("📍 Germany – Wind vs Load")
        locations = pd.DataFrame({
            'lat': [52.52, 48.14, 53.55, 50.11, 51.34, 54.32, 51.05, 49.01],
            'lon': [13.41, 11.58, 9.99, 8.68, 12.37, 10.13, 13.74, 8.40],
            'city': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Leipzig', 'Kiel', 'Dresden', 'Karlsruhe']
        })
        locations['color'] = locations['city'].apply(
            lambda x: [255, 0, 0, 160] if x in ['Munich', 'Frankfurt', 'Karlsruhe'] else [0, 0, 255, 160]
        )
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=locations,
            get_position=["lon", "lat"],
            get_radius=10000,
            get_fill_color="color",
            get_line_color=[0, 0, 0, 50]
        )
        
        st.pydeck_chart(pdk.Deck(
            layers=[layer],
            initial_view_state=pdk.ViewState(latitude=51.0, longitude=10.0, zoom=5, pitch=0)
        ))
        
        st.caption("🔵 North = Wind Generation | 🔴 South = Industrial Load | ⚡ Kupferzell = Grid Booster")
        
        with st.expander("📋 Full Response"):
            st.json(data)
    
    time.sleep(15)