"""
Macro Tier – Load forecasting with LightGBM + SMARD + DWD
"""

import joblib
import pandas as pd
from datetime import datetime, timedelta
from app.dwd_fetcher import get_germany_weather
from app.smard_fetcher import SMARDFetcher

class MacroTier:
    def __init__(self):
        try:
            self.model = joblib.load('models/lightgbm_model.pkl')
            print("✅ LightGBM model loaded")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            self.model = None
        
        self.smard = SMARDFetcher()
        
    def predict_load(self):
        """Get current load from SMARD (with fallback)"""
        try:
            load = self.smard.get_current_load()
            if load is not None:
                return load
        except Exception as e:
            print(f"⚠️ SMARD error: {e}")
        return 50000  # Fallback
    
    def forecast_load(self, target_time=None):
        """
        Forecast load for a future time using LightGBM.
        target_time: datetime object (default: 24 hours from now)
        Returns: forecast load in MW, or None if unavailable
        """
        if self.model is None:
            print("⚠️ LightGBM model not available")
            return None
        
        if target_time is None:
            target_time = datetime.now() + timedelta(hours=24)
        
        # Create features for the target time
        features = pd.DataFrame([{
            'hour': target_time.hour,
            'day_of_week': target_time.weekday(),
            'month': target_time.month,
            'is_weekend': 1 if target_time.weekday() >= 5 else 0,
            'Pm': 50000  # Estimated generation (can be improved with DWD)
        }])
        
        try:
            forecast = self.model.predict(features)[0]
            return round(forecast, 0)
        except Exception as e:
            print(f"⚠️ Forecast error: {e}")
            return None
    
    def compute_cf(self, weather_data):
        """Compute Capacity Factor from weather data"""
        if weather_data is None or weather_data.empty:
            return 0
        
        wind_speed = weather_data['wind_speed'].iloc[0] if 'wind_speed' in weather_data else 0
        solar_radiation = weather_data['solar_radiation'].iloc[0] if 'solar_radiation' in weather_data else 0
        
        wind_power = (wind_speed ** 3) * 10
        solar_power = solar_radiation * 0.5
        cf = (wind_power + solar_power) / 200000
        return min(cf, 1.0)
    
    def get_forecast(self):
        """Get load forecast (placeholder)"""
        return self.predict_load()