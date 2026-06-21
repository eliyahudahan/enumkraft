"""
Dunkelflaute Detection based on Strnad et al. (2026)
Definition: 48h average CF (wind + solar) < 0.06
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def compute_capacity_factor(wind_speed_m_s, solar_radiation_w_m2):
    """
    Calculate Capacity Factor (CF) for wind + solar
    Based on Strnad et al. (2026)
    
    CF = (wind_power + solar_power) / total_installed_capacity
    
    Germany installed capacity (2026):
    - Wind: ~100 GW (onshore + offshore)
    - Solar: ~100 GW
    - Total: ~200 GW
    """
    # Simplified power calculation
    # Wind: P ≈ 0.5 * ρ * A * v³ (simplified to v³ * 10 MW)
    wind_power = (wind_speed_m_s ** 3) * 10  # MW
    
    # Solar: P ≈ irradiance * efficiency * area
    # Simplified: 1 W/m² ≈ 0.5 MW
    solar_power = solar_radiation_w_m2 * 0.5  # MW
    
    total_power = wind_power + solar_power
    total_capacity = 200000  # 200 GW in MW
    
    cf = total_power / total_capacity
    return min(cf, 1.0)  # Cap at 1.0

def detect_dunkelflaute(weather_df):
    """
    Detect Dunkelflaute from weather DataFrame
    Returns: (is_dunkelflaute, cf_48h, details)
    """
    if len(weather_df) < 48:
        return False, None, "Not enough data (need 48 hours)"
    
    # Calculate CF for each hour
    weather_df['cf'] = weather_df.apply(
        lambda row: compute_capacity_factor(row['wind_speed'], row['solar_radiation']),
        axis=1
    )
    
    # Calculate 48-hour rolling average
    cf_48h = weather_df['cf'].rolling(48).mean()
    
    # Check latest 48h
    latest_cf = cf_48h.iloc[-1] if not pd.isna(cf_48h.iloc[-1]) else None
    
    if latest_cf is not None:
        is_dunkelflaute = latest_cf < 0.06
        return is_dunkelflaute, latest_cf, {
            'cf_48h': latest_cf,
            'wind_avg': weather_df['wind_speed'].iloc[-48:].mean(),
            'solar_avg': weather_df['solar_radiation'].iloc[-48:].mean(),
            'threshold': 0.06
        }
    
    return False, None, "No valid CF calculation"

def check_dunkelflaute_today(weather_df):
    """
    Check if today has Dunkelflaute conditions
    """
    result, cf, details = detect_dunkelflaute(weather_df)
    
    print("\n" + "="*50)
    print("📊 DUNKELFLAUTE DETECTION (Strnad et al. 2026)")
    print("="*50)
    print(f"Status: {'⚠️ DUNKELFLAUTE DETECTED!' if result else '✅ No Dunkelflaute'}")
    print(f"48h CF: {cf:.4f}")
    print(f"Threshold: 0.06")
    print(f"Wind avg: {details.get('wind_avg', 0):.1f} m/s")
    print(f"Solar avg: {details.get('solar_avg', 0):.0f} W/m²")
    print("="*50)
    
    return result, cf

if __name__ == "__main__":
    # Test with sample data
    print("🧪 Testing Dunkelflaute Detection...")
    
    # Create 48 hours of sample data
    sample_df = pd.DataFrame({
        'timestamp': pd.date_range('2026-06-21', periods=48, freq='h'),
        'wind_speed': [3.0] * 48,  # Low wind
        'solar_radiation': [150] * 48  # Low solar
    })
    
    result, cf = check_dunkelflaute_today(sample_df)
