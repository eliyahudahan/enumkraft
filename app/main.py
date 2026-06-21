# app/main.py - קוד מינימלי שעובד
from fastapi import FastAPI
from datetime import datetime
import pandas as pd
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="EnumKraft 2.0", version="2.0")

# טעינת מודל LightGBM (אם קיים)
MODEL_PATH = "models/lightgbm_model.pkl"
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

@app.get("/")
async def root():
    return {
        "project": "EnumKraft 2.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/frequency/current")
async def get_frequency():
    """Get current grid frequency from Gridradar"""
    # TODO: connect to Gridradar
    return {
        "frequency": 50.02,
        "timestamp": datetime.now().isoformat(),
        "source": "Gridradar (mock)"
    }

@app.post("/predict/load")
async def predict_load(data: dict):
    """Predict load from generation"""
    generation = data.get("generation_mw", 0)
    # TODO: use LightGBM
    return {
        "generation_mw": generation,
        "predicted_load_mw": generation * 0.95,  # placeholder
        "timestamp": datetime.now().isoformat()
    }

@app.get("/dunkelflaute/detect")
async def detect_dunkelflaute():
    """Detect Dunkelflaute conditions"""
    # TODO: implement logic
    return {
        "dunkelflaute_detected": False,
        "wind_speed": 3.5,
        "solar_irradiance": 200,
        "timestamp": datetime.now().isoformat()
    }