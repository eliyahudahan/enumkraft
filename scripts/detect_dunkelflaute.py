# scripts/detect_dunkelflaute.py
def detect_dunkelflaute(weather_df, threshold_wind=5, threshold_solar=200):
    """
    Dunkelflaute: low wind (<5 m/s) AND low solar (<200 W/m²)
    Based on Li (2025) - TU Delft
    """
    df = weather_df.copy()
    df['dunkelflaute'] = (
        (df['wind_speed_10m'] < threshold_wind) & 
        (df['solar_radiation'] < threshold_solar)
    )
    
    # Check today
    today = pd.Timestamp.now().date()
    today_data = df[df['timestamp'].dt.date == today]
    
    if len(today_data) > 0:
        dunkelflaute_hours = today_data['dunkelflaute'].sum()
        total_hours = len(today_data)
        print(f"Today ({today}): {dunkelflaute_hours}/{total_hours} hours are Dunkelflaute")
        return today_data
    
    return df

# Run it
weather = get_germany_weather()
dunkelflaute_today = detect_dunkelflaute(weather)