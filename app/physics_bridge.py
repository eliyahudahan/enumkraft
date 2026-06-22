"""
Physics Bridge – Resampling and interpolation
Connects SMARD (1h) → Gridradar (5s)
"""

import pandas as pd
import numpy as np

class PhysicsBridge:
    def __init__(self, H=5.0, f_nominal=50.0):
        self.H = H
        self.f_nominal = f_nominal
        
    def resample_to_5s(self, df_hourly):
        """Resample hourly data to 5-second intervals"""
        df_hourly.index = pd.to_datetime(df_hourly['timestamp'])
        df_5s = df_hourly.resample('5S').interpolate(method='linear')
        return df_5s
    
    def compute_boundary(self, load_mw, wind_mw, solar_mw):
        """Calculate boundary conditions for Swing Equation"""
        P_mech = wind_mw + solar_mw
        P_elec = load_mw
        return {
            "P_mech": P_mech,
            "P_elec": P_elec,
            "P_imbalance": P_mech - P_elec,
            "H": self.H,
            "f_nominal": self.f_nominal
        }
    
    def swing_step(self, f_prev, P_imbalance, dt=5.0):
        """Single step of Swing Equation"""
        P_base = 50000  # MW
        df_dt = (self.f_nominal / (2 * self.H)) * (P_imbalance / P_base)
        f_new = f_prev + df_dt * dt
        return max(49.0, min(51.0, f_new))