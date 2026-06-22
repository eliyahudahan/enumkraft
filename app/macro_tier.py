"""
Macro Tier – Load forecasting with LightGBM + DWD
"""

import joblib
import pandas as pd
from app.dwd_fetcher import get_germany_weather

class MacroTier:
    def __init__(self):
        try:
            self.model = joblib.load('models/lightgbm_model.pkl')
            print("✅ LightGBM model loaded")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            self.model = None
        
    def predict_load(self):
        """Get current load – fallback to 50,000 MW"""
        return 50000
    
    def compute_cf(self, weather_data):
        """
        Compute Capacity Factor from weather data
        weather_data: DataFrame from DWD or None
        """
        # בדיקה אם weather_data תקין
        if weather_data is None:
            return 0
        
        # אם זה DataFrame, בודקים שהוא לא ריק
        if isinstance(weather_data, pd.DataFrame):
            if weather_data.empty:
                return 0
            # לוקחים את השורה הראשונה
            row = weather_data.iloc[0]
            wind_speed = row.get('wind_speed', 0) if hasattr(row, 'get') else 0
            solar_radiation = row.get('solar_radiation', 0) if hasattr(row, 'get') else 0
        else:
            # אם זה dict
            wind_speed = weather_data.get('wind_speed', 0)
            solar_radiation = weather_data.get('solar_radiation', 0)
        
        # חישוב
        wind_power = (wind_speed ** 3) * 10
        solar_power = solar_radiation * 0.5
        cf = (wind_power + solar_power) / 200000
        return min(cf, 1.0)  # מגבילים ל-1
    
    def get_forecast(self):
        """Get load forecast"""
        return self.predict_load()