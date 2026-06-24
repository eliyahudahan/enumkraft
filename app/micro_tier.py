"""
Micro Tier – Frequency calculation with Swing Equation + Gridradar
"""

from app.physics_bridge import PhysicsBridge
from app.gridradar_client import get_current_frequency
from app.smard_fetcher import SMARDFetcher

class MicroTier:
    def __init__(self):
        self.bridge = PhysicsBridge()
        self.smard = SMARDFetcher()
        
    def get_frequency(self):
        """Try Gridradar first, fallback to Swing Equation"""
        # ✅ נסה את Gridradar
        gridradar_freq = get_current_frequency()
        
        # ✅ אם Gridradar החזיר תוצאה תקינה – השתמש בה
        if gridradar_freq and gridradar_freq.get('source') in ['Gridradar (Live)', 'Gridradar (Cached)']:
            return gridradar_freq
        
        # ❌ אם Gridradar נכשל – השתמש ב-Swing Equation
        print("⚠️ Gridradar failed, using Swing Equation fallback")
        load = self.smard.get_current_load()
        if load is None:
            load = 50000
        
        # חישוב Swing Equation (פשטני)
        P_imbalance = 0  # נדרוש נתוני רוח/שמש
        f = self.bridge.swing_step(50.0, P_imbalance)
        
        return {
            "frequency": f,
            "timestamp": None,
            "source": "Swing Equation (fallback)"
        }