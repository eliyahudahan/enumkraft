import streamlit as st
import requests
import time

st.set_page_config(page_title="EnumKraft 2.0", layout="wide")
st.title("⚡ EnumKraft 2.0 – Grid Stability Dashboard")
st.caption("Live data from FastAPI + Gridradar + Swing Equation")

# ⬇️ כתובת ה-API
API_URL = "http://localhost:8000"

# ✅ מיכל לנתונים (מוגדר פעם אחת)
placeholder = st.empty()

while True:
    try:
        response = requests.get(f"{API_URL}/api/v1/grid/stability", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        with placeholder.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("📡 Frequency", f"{data.get('frequency_hz', 50.0):.3f} Hz")
            col2.metric("⚡ Load", f"{data.get('load_mw', 50000):.0f} MW")
            col3.metric("🌤️ CF", f"{data.get('cf_48h', 0.0):.4f}")
            col4.metric("🌡️ Temperature", f"{data.get('temperature', 'N/A')}°C")
            
            status = data.get('stability_status', 'NORMAL')
            if status == "EMERGENCY":
                col5.error(f"🚨 {status}")
            elif status == "CRITICAL":
                col5.warning(f"⚠️ {status}")
            else:
                col5.success(f"✅ {status}")
            
            st.line_chart([data.get('frequency_hz', 50.0)], height=150)
            
            with st.expander("📋 Full Response"):
                st.json(data)
    
    except requests.exceptions.ConnectionError:
        with placeholder.container():
            st.error("❌ Cannot connect to API. Is Docker running?")
            st.code("docker run -p 8000:8000 --env-file .env enumkraft:2.0")
    
    except Exception as e:
        with placeholder.container():
            st.error(f"⚠️ Error: {e}")
    
    time.sleep(15)