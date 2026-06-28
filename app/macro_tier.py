"""
Macro Tier – Load forecasting with LightGBM + SMARD + DWD
"""

import joblib
import pandas as pd
from datetime import datetime, timedelta
from app.dwd_fetcher import get_germany_weather
from app.smard_fetcher import SMARDFetcher
import sklearn  # ✅ הוסף את זה

class MacroTier:
    def __init__(self):
        try:
            # ✅ טען עם sklearn compatibility
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
        """Forecast load using LightGBM, fallback to SMARD if fails"""
        # ✅ ניסיון ראשון – LightGBM
        if self.model is not None:
            try:
                if target_time is None:
                    target_time = datetime.now() + timedelta(hours=24)
                
                # ✅ יצירת תכונות
                features = pd.DataFrame([{
                    'Pm': 50000,
                    'hour': target_time.hour,
                    'day_of_week': target_time.weekday(),
                    'month': target_time.month,
                    'is_weekend': 1 if target_time.weekday() >= 5 else 0
                }])
                
                # ✅ סדר העמודות הנכון
                feature_order = ['Pm', 'hour', 'day_of_week', 'month', 'is_weekend']
                features = features[feature_order]
                
                # ✅ ניסיון תחזית
                forecast = self.model.predict(features)[0]
                return round(forecast, 0)
                
            except Exception as e:
                print(f"⚠️ LightGBM forecast error: {e}")
                # ✅ ניפול ל-fallback
        
        # ✅ Fallback – העומס האחרון מ-SMARD
        print("⚠️ Using SMARD fallback for forecast")
        return self.predict_load()
    
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