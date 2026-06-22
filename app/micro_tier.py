"""
Micro Tier – Frequency calculation with Swing Equation + Gridradar
"""

from app.physics_bridge import PhysicsBridge
from app.gridradar_client import get_current_frequency
from app.smard_fetcher import SMARDFetcher
import joblib
import pandas as pd
from app.dwd_fetcher import get_germany_weather

class MacroTier:
    def __init__(self):
        self.model = joblib.load('models/lightgbm_model.pkl')
        
    def predict_load(self, generation_mw=50000):
        """Predict load using LightGBM model"""
        # שימוש במודל אם יש לך נתוני קלט, אחרת fallback
        try:
            # כאן תוכל להעביר את generation_mw + time features למודל
            # כרגע - fallback
            return 50000
        except:
            return 50000
        
class MicroTier:
    def __init__(self):
        self.bridge = PhysicsBridge()
        self.smard = SMARDFetcher()
        
    def get_frequency(self):
        """Try Gridradar first, fallback to Swing Equation"""
        # Try real frequency first
        gridradar_freq = get_current_frequency()
        
        if gridradar_freq.get('source') == 'Gridradar':
            return gridradar_freq
        
        # Fallback: Swing Equation
        load = self.smard.get_current_load()
        if load is None:
            load = 50000  # Default
        
        # Simplified Swing calculation
        # Using typical values for Germany
        P_imbalance = 0  # Would need wind/solar data
        f = self.bridge.swing_step(50.0, P_imbalance)
        
        return {
            "frequency": f,
            "timestamp": None,
            "source": "Swing Equation (fallback)"
        }