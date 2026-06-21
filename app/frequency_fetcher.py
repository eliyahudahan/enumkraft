"""
Frequency fetcher - Using DWD + Swing Equation
"""

import pandas as pd
import numpy as np
from datetime import datetime

def calculate_frequency_from_weather(wind_speed_m_s, solar_radiation_w_m2):
    """
    Calculate grid frequency using Swing Equation
    """
    # Simplified power calculation
    wind_power = (wind_speed_m_s ** 3) * 10  # MW (simplified)
    solar_power = solar_radiation_w_m2 * 0.5  # MW (simplified)
    total_generation = wind_power + solar_power
    
    # Germany typical values
    base_load = 50000  # MW
    H = 5.0  # Inertia constant
    f0 = 50.0  # Nominal frequency
    P_base = 50000  # Base power
    
    # Power imbalance
    delta_p = total_generation - base_load
    
    # Frequency deviation (Swing Equation simplified)
    # df/dt = (f0/(2*H)) * (delta_p/P_base)
    # For steady-state: df ≈ (f0/(2*H)) * (delta_p/P_base)
    df = (f0 / (2 * H)) * (delta_p / P_base)
    frequency = f0 + df
    
    # Clamp to realistic range (49.5 - 50.5 Hz)
    frequency = max(49.5, min(50.5, frequency))
    
    return round(frequency, 4)

def get_current_frequency():
    """Get current frequency from DWD weather data"""
    try:
        # Load today's weather
        df = pd.read_csv('data/weather_20260621.csv')
        
        if len(df) > 0:
            # Use most recent hour
            latest = df.iloc[-1]
            freq = calculate_frequency_from_weather(
                latest['wind_speed'],
                latest['solar_radiation']
            )
            
            return {
                'frequency': freq,
                'timestamp': datetime.now().isoformat(),
                'source': 'DWD + Swing Equation',
                'wind_speed': latest['wind_speed'],
                'solar_radiation': latest['solar_radiation'],
                'temperature': latest.get('temperature', 0)
            }
    except Exception as e:
        print(f"Error: {e}")
    
    return {
        'frequency': 50.0,
        'timestamp': datetime.now().isoformat(),
        'source': 'fallback'
    }

if __name__ == "__main__":
    freq = get_current_frequency()
    print(f"🔌 Grid Frequency")
    print(f"   Frequency: {freq['frequency']} Hz")
    print(f"   Source: {freq['source']}")
    if 'wind_speed' in freq:
        print(f"   Wind: {freq['wind_speed']:.1f} m/s")
        print(f"   Solar: {freq['solar_radiation']:.0f} W/m²")
        print(f"   Temperature: {freq.get('temperature', 0):.1f}°C")
