import streamlit as st
import requests
import time
import pandas as pd
import pydeck as pdk

# ✅ set_page_config MUST be the first Streamlit command
st.set_page_config(page_title="EnumKraft 2.0", layout="wide")

st.title("⚡ EnumKraft 2.0 – Grid Stability Dashboard")
st.caption("Live data from FastAPI + Gridradar + Swing Equation")

API_URL = "http://localhost:8000"
placeholder = st.empty()

while True:
    try:
        response = requests.get(f"{API_URL}/api/v1/grid/stability", timeout=60)
        response.raise_for_status()
        data = response.json()

        forecast_response = requests.get(f"{API_URL}/api/v1/macro/forecast/future", timeout=60)
        forecast_data = forecast_response.json() if forecast_response.status_code == 200 else None

        with placeholder.container():
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.metric("📡 Frequency", f"{data.get('frequency_hz', 50.0):.3f} Hz")
            col2.metric("⚡ Load", f"{data.get('load_mw', 50000):.0f} MW")
            col3.metric("🌤️ CF", f"{data.get('cf_48h', 0.0):.4f}")
            col4.metric("🌡️ Temperature", f"{data.get('temperature', 'N/A')}°C")
            
            if forecast_data and 'forecast_load_mw' in forecast_data:
                col5.metric("📈 Forecast (24h)", f"{forecast_data['forecast_load_mw']:.0f} MW")
            else:
                col5.metric("📈 Forecast (24h)", "N/A")

            status = data.get('stability_status', 'NORMAL')
            if "EMERGENCY" in status:
                col6.error(f"🚨 {status}")
            elif "CRITICAL" in status:
                col6.warning(f"⚠️ {status}")
            else:
                col6.success(f"✅ {status}")

            st.line_chart([data.get('frequency_hz', 50.0)], height=150)

            # 🗺️ Germany Map (PyDeck)
            st.subheader("📍 Germany – Wind vs Load")
            
            # ✅ Define locations HERE (before using it)
            locations = pd.DataFrame({
                'lat': [52.52, 48.14, 53.55, 50.11, 51.34, 54.32, 51.05, 49.01],
                'lon': [13.41, 11.58, 9.99, 8.68, 12.37, 10.13, 13.74, 8.40],
                'city': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Leipzig', 'Kiel', 'Dresden', 'Karlsruhe']
            })

            # ✅ Add colors: red for south, blue for north
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
                if forecast_data:
                    st.json(forecast_data)

    except requests.exceptions.ConnectionError:
        with placeholder.container():
            st.error("❌ Cannot connect to API. Is Docker running?")
            st.code("docker run -p 8000:8000 --env-file .env enumkraft:2.0")
    except Exception as e:
        with placeholder.container():
            st.error(f"⚠️ Error: {e}")

    time.sleep(15)