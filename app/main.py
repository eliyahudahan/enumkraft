from fastapi import FastAPI
from app.dwd_fetcher import get_germany_weather
from app.dunkelflaute import check_dunkelflaute_today, classify_grid_state
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

@app.get("/api/v1/macro/forecast/future")
async def macro_forecast_future(hours_ahead: int = 24):
    """
    Forecast load X hours ahead using LightGBM.
    Default: 24 hours ahead.
    """
    target_time = datetime.now() + pd.Timedelta(hours=hours_ahead)
    forecast = macro.forecast_load(target_time)
    
    if forecast is None:
        return {"error": "Forecast not available", "model": "LightGBM", "mae": 261}
    
    return {
        "forecast_load_mw": forecast,
        "target_time": target_time.isoformat(),
        "model": "LightGBM",
        "mae": 261,
        "hours_ahead": hours_ahead
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

    dunkelflaute_result = False
    cf = 0.0
    if weather is not None and not weather.empty:
        today = datetime.now().strftime("%Y-%m-%d")
        df = pd.DataFrame({
            'timestamp': pd.date_range(today, periods=48, freq='h'),
            'wind_speed': [weather['wind_speed'].iloc[0] if 'wind_speed' in weather else 3] * 48,
            'solar_radiation': [weather['solar_radiation'].iloc[0] if 'solar_radiation' in weather else 200] * 48
        })
        dunkelflaute_result, cf = check_dunkelflaute_today(df)
        dunkelflaute_result = bool(dunkelflaute_result) if dunkelflaute_result is not None else False
        cf = float(cf) if cf is not None else 0.0
    
    grid_state = classify_grid_state(cf, load)
    
    return {
        "stability_status": grid_state["state"],
        "dunkelflaute_detected": dunkelflaute_result,
        "frequency_hz": float(freq.get('frequency', 50.0)),
        "load_mw": int(load),
        "cf_48h": cf,
        "temperature": temperature,
        "action": grid_state["action"],
        "timestamp": datetime.now().isoformat()
    }