import requests
import pandas as pd
from datetime import datetime

def get_germany_weather():
    """Get real weather data for Germany from Open-Meteo"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.0,
        "longitude": 10.0,
        "hourly": ["temperature_2m", "wind_speed_10m", "solar_radiation"],
        "timezone": "Europe/Berlin",
        "forecast_days": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code != 200:
        print(f"❌ API Error {response.status_code}: {data.get('reason', 'Unknown')}")
        return None
    
    print("✅ Weather API connected successfully")
    return data

def detect_dunkelflaute(weather_data):
    """Detect Dunkelflaute conditions (low wind + low solar)"""
    if weather_data is None:
        return None
    
    hourly = weather_data['hourly']
    
    df = pd.DataFrame({
        'timestamp': pd.to_datetime(hourly['time']),
        'wind_speed': hourly['wind_speed_10m'],
        'solar_radiation': hourly['solar_radiation'],
        'temperature': hourly['temperature_2m']
    })
    
    # Dunkelflaute: wind < 5 m/s AND solar < 200 W/m² (Li 2025)
    df['dunkelflaute'] = (df['wind_speed'] < 5) & (df['solar_radiation'] < 200)
    
    # Today's summary
    today = datetime.now().date()
    today_data = df[df['timestamp'].dt.date == today]
    
    print(f"\n📊 Weather Data for {today}:")
    print(f"  Total hours: {len(today_data)}")
    
    if len(today_data) > 0:
        dunkelflaute_hours = today_data['dunkelflaute'].sum()
        print(f"  Dunkelflaute hours: {dunkelflaute_hours}")
        print(f"  Avg wind speed: {today_data['wind_speed'].mean():.1f} m/s")
        print(f"  Avg solar radiation: {today_data['solar_radiation'].mean():.0f} W/m²")
        print(f"  Avg temperature: {today_data['temperature'].mean():.1f}°C")
        
        if dunkelflaute_hours > 0:
            print(f"  ⚠️ DUNKELFLAUTE DETECTED: {dunkelflaute_hours} hours today!")
            dunkelflaute_times = today_data[today_data['dunkelflaute']]['timestamp'].dt.strftime('%H:%M')
            print(f"  Hours: {', '.join(dunkelflaute_times)}")
        else:
            print(f"  ✅ No Dunkelflaute conditions today")
    else:
        print("  No data for today yet")
    
    return df

if __name__ == "__main__":
    print("🌤️ Fetching real weather data for Germany (21.06.2026)...")
    weather = get_germany_weather()
    
    if weather:
        df = detect_dunkelflaute(weather)
        if df is not None:
            filename = f"data/weather_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filename, index=False)
            print(f"\n✅ Weather data saved to {filename}")
            print("\n📋 Sample data (first 3 hours):")
            print(df[['timestamp', 'wind_speed', 'solar_radiation', 'dunkelflaute']].head(3))
    else:
        print("❌ Failed to get weather data")
