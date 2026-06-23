# streamlit_app.py
import streamlit as st
import requests

st.title("EnumKraft 2.0 – Grid Stability Dashboard")

# קריאה ל-API
response = requests.get("http://localhost:8000/api/v1/grid/stability")
data = response.json()

col1, col2, col3 = st.columns(3)
col1.metric("Frequency", f"{data['frequency_hz']} Hz")
col2.metric("Load", f"{data['load_mw']} MW")
col3.metric("CF", f"{data['cf_48h']:.4f}")

st.line_chart([data['frequency_hz']])