"""
DWD Open Data Fetcher - Deutscher Wetterdienst (Official German Weather Service)
Real weather data for Germany - 21.06.2026
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import io

class DWDFetcher:
    def __init__(self):
        # DWD Open Data base URL - working endpoint
        self.base_url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/"
        self.station_id = "01005"  # Berlin-Dahlem
        
    def get_recent_weather(self):
        """
        Get recent weather data using DWD's actual data structure
        """
        print("📡 Fetching DWD weather data...")
        
        # DWD provides data in ZIP files, we need to read the latest
        # For now, we'll use DWD's text files which are updated daily
        
        # Get temperature data
        temp_url = f"{self.base_url}air_temperature/historical/TU_Stundenwerte_Beschreibung_Stationen.txt"
        
        try:
            response = requests.get(temp_url, timeout=15)
            if response.status_code == 200:
                print("✅ DWD temperature data received")
                
                # Parse the text file
                lines = response.text.split('\n')
                station_info = lines[:10]  # First lines are metadata
                
                return {
                    "source": "DWD",
                    "type": "temperature",
                    "data": response.text[:1000],  # Sample
                    "timestamp": datetime.now().isoformat(),
                    "stations": len(lines) if lines else 0
                }
            else:
                print(f"❌ DWD error: {response.status_code}")
                return self._fallback_weather()
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._fallback_weather()
    
    def _fallback_weather(self):
        """
        Fallback: Open-Meteo but with DWD data source
        """
        print("⚠️ Using Open-Meteo (DWD-powered) as fallback")
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 51.0,
            "longitude": 10.0,
            "hourly": ["temperature_2m", "wind_speed_10m", "shortwave_radiation"],
            "timezone": "Europe/Berlin",
            "forecast_days": 1,
            "models": "dwd_icon"  # Explicitly use DWD model
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "DWD (via Open-Meteo)",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }
        except Exception as e:
            print(f"❌ Fallback error: {e}")
        
        return {
            "source": "DWD",
            "error": "No data available",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_weather_today(self):
        """
        Get today's weather data (24 hours)
        """
        fallback_data = self._fallback_weather()
        
        if fallback_data and 'data' in fallback_data:
            hourly = fallback_data['data']['hourly']
            
            # Create DataFrame with today's data
            df = pd.DataFrame({
                'timestamp': pd.to_datetime(hourly['time']),
                'wind_speed': hourly['wind_speed_10m'],
                'solar_radiation': hourly['shortwave_radiation'],
                'temperature': hourly['temperature_2m']
            })
            
            return df
        
        return None

# Simple function for easy import
def get_germany_weather():
    """
    Get current DWD weather data for Germany (21.06.2026)
    Returns DataFrame with hourly data
    """
    fetcher = DWDFetcher()
    return fetcher.get_weather_today()

if __name__ == "__main__":
    print("🌤️ Testing DWD Fetcher...")
    df = get_germany_weather()
    
    if df is not None:
        print(f"✅ Got {len(df)} hours of weather data")
        print(f"   Date: {df['timestamp'].iloc[0].date()}")
        print(f"   Wind: {df['wind_speed'].mean():.1f} m/s")
        print(f"   Solar: {df['solar_radiation'].mean():.0f} W/m²")
        print(f"   Temp: {df['temperature'].mean():.1f}°C")
        
        # Save to CSV
        filename = f"data/weather_{datetime.now().strftime('%Y%m%d')}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved to {filename}")
    else:
        print("❌ Failed to get weather data")
