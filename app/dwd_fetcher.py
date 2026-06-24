"""
DWD Open Data Fetcher – Real weather via Open-Meteo (DWD model)
"""

import pandas as pd
import requests
from datetime import datetime, timedelta

class DWDFetcher:
    def __init__(self):
        self.station_id = "01005"
        self.base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/"

    def get_weather_today(self):
        """Get weather data from Open-Meteo (DWD-powered)"""
        print("📡 Fetching DWD weather data (via Open-Meteo)...")
        return self._fallback_openmeteo()

    def _fallback_openmeteo(self):
        """Primary source: Open-Meteo with DWD model"""
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 51.0,
            "longitude": 10.0,
            "hourly": ["temperature_2m", "wind_speed_10m", "shortwave_radiation"],
            "timezone": "Europe/Berlin",
            "forecast_days": 1,
            "models": "dwd_icon"
        }

        try:
            response = requests.get(url, params=params, timeout=30)  # ✅ Timeout 30
            if response.status_code == 200:
                data = response.json()
                hourly = data['hourly']
                df = pd.DataFrame({
                    'timestamp': pd.to_datetime(hourly['time']),
                    'wind_speed': hourly['wind_speed_10m'],
                    'solar_radiation': hourly['shortwave_radiation'],
                    'temperature': hourly['temperature_2m']
                })
                print("✅ Got weather from Open-Meteo (DWD-powered)")
                return df
        except Exception as e:
            print(f"⚠️ Open-Meteo error: {e}")

        # Fallback to synthetic (only if both fail)
        print("⚠️ Using synthetic weather data")
        return self._synthetic_weather()

    def _synthetic_weather(self):
        """Synthetic weather data (fallback only)"""
        now = datetime.now()
        timestamps = [now + timedelta(hours=i) for i in range(24)]
        hour_of_day = [t.hour for t in timestamps]
        
        temps = [15 + 10 * (1 - abs(h - 12) / 12) for h in hour_of_day]
        winds = [3 + 3 * (1 - abs(h - 12) / 12) for h in hour_of_day]
        solar = [max(0, 800 * (1 - abs(h - 12) / 12)) for h in hour_of_day]

        df = pd.DataFrame({
            'timestamp': timestamps,
            'wind_speed': winds,
            'solar_radiation': solar,
            'temperature': temps
        })
        print("✅ Generated synthetic weather data")
        return df

def get_germany_weather():
    fetcher = DWDFetcher()
    return fetcher.get_weather_today()

if __name__ == "__main__":
    df = get_germany_weather()
    if df is not None and not df.empty:
        print(f"✅ Got {len(df)} hours of weather data")
        print(df[['timestamp', 'temperature', 'wind_speed']].head())