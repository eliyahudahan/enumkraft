"""
Macro Tier – Load forecasting with LightGBM + SMARD + DWD
"""

import joblib
import pandas as pd
from app.dwd_fetcher import get_germany_weather
from app.smard_fetcher import SMARDFetcher  # ✅ חובה!

class MacroTier:
    def __init__(self):
        try:
            self.model = joblib.load('models/lightgbm_model.pkl')
            print("✅ LightGBM model loaded")
        except Exception as e:
            print(f"⚠️ Could not load model: {e}")
            self.model = None
        
        self.smard = SMARDFetcher()  # ✅ הוסף את זה!
        
    def predict_load(self):
        """Get current load from SMARD (with fallback)"""
        try:
            load = self.smard.get_current_load()
            if load is not None:
                print(f"✅ Load from SMARD: {load} MW")
                return load
            else:
                print("⚠️ SMARD returned None, using fallback")
                return 50000
        except Exception as e:
            print(f"⚠️ SMARD error: {e}")
            return 50000