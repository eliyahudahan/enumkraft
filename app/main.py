from fastapi import FastAPI
from app.dwd_fetcher import get_germany_weather
from app.dunkelflaute import check_dunkelflaute_today
from app.macro_tier import MacroTier
from app.micro_tier import MicroTier
from app.physics_bridge import PhysicsBridge
from datetime import datetime
import pandas as pd
import numpy as np

app = FastAPI(title="EnumKraft 2.0", version="2.0.0")
macro = MacroTier()
micro = MicroTier()

@app.get("/")
async def root():
    return {
        "project": "EnumKraft 2.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/macro/forecast")
async def macro_forecast():
    load = macro.predict_load()
    weather = get_germany_weather()
    cf = macro.compute_cf(weather) if weather is not None and not weather.empty else 0
    return {
        "load_mw": load,
        "cf_48h": cf,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/micro/frequency")
async def micro_frequency():
    freq = micro.get_frequency()
    return freq

@app.get("/api/v1/grid/stability")
async def grid_stability():
    load = macro.predict_load()
    weather = get_germany_weather()
    freq = micro.get_frequency()
    
    temperature = None
    if weather is not None and not weather.empty:
        temperature = weather['temperature'].iloc[0] if 'temperature' in weather.columns else None

    
    if weather is not None and not weather.empty:
        df = pd.DataFrame({
            'timestamp': pd.date_range('2026-06-23', periods=48, freq='h'),
            'wind_speed': [weather['wind_speed'].iloc[0] if 'wind_speed' in weather else 3] * 48,
            'solar_radiation': [weather['solar_radiation'].iloc[0] if 'solar_radiation' in weather else 200] * 48
        })
        dunkelflaute_result, cf = check_dunkelflaute_today(df)
        dunkelflaute_result = bool(dunkelflaute_result) if dunkelflaute_result is not None else False
        cf = float(cf) if cf is not None else 0.0
    else:
        dunkelflaute_result = False
        cf = 0.0
    
    return {
        "stability_status": "EMERGENCY" if dunkelflaute_result else "NORMAL",
        "dunkelflaute_detected": dunkelflaute_result,
        "frequency_hz": float(freq.get('frequency', 50.0)),
        "load_mw": int(load),
        "cf_48h": cf,
        "temperature": temperature,
        "timestamp": datetime.now().isoformat()
    }