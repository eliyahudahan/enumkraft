from fastapi import FastAPI
from app.dwd_fetcher import get_germany_weather
from app.dunkelflaute import check_dunkelflaute_today
from app.macro_tier import MacroTier
from app.micro_tier import MicroTier
from app.physics_bridge import PhysicsBridge
from datetime import datetime
import pandas as pd

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
    
    # ✅ תיקון: בדיקה נכונה ל-DataFrame
    if weather is not None and not weather.empty:
        cf = macro.compute_cf(weather)
    else:
        cf = 0
    
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
    
    # ✅ תיקון: בדיקה נכונה ל-DataFrame
    if weather is not None and not weather.empty:
        df = pd.DataFrame({
            'timestamp': pd.date_range('2026-06-22', periods=48, freq='h'),
            'wind_speed': [weather['wind_speed'].iloc[0] if 'wind_speed' in weather else 3] * 48,
            'solar_radiation': [weather['solar_radiation'].iloc[0] if 'solar_radiation' in weather else 200] * 48
        })
        dunkelflaute_result, cf = check_dunkelflaute_today(df)
    else:
        dunkelflaute_result = False
        cf = 0
    
    return {
        "stability_status": "EMERGENCY" if dunkelflaute_result else "NORMAL",
        "dunkelflaute_detected": dunkelflaute_result,
        "frequency_hz": freq.get('frequency', 50.0),
        "load_mw": load,
        "cf_48h": cf,
        "timestamp": datetime.now().isoformat()
    }