# app/gridradar_client.py - קובץ חדש
import requests
import os
from datetime import datetime
# app/frequency.py - כבר עובד, צריך רק לעדכן
from gridradar_fetcher import get_current_frequency

GRIDRADAR_TOKEN = os.getenv("GRIDRADAR_TOKEN")
BASE_URL = "https://api.gridradar.net/v1"

def get_current_frequency():
    """Get real frequency from Gridradar API"""
    if not GRIDRADAR_TOKEN:
        return {"error": "No token", "frequency": 50.0}
    
    try:
        response = requests.get(
            f"{BASE_URL}/frequency/current",
            headers={"Authorization": f"Bearer {GRIDRADAR_TOKEN}"}
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "frequency": data.get("frequency", 50.0),
                "timestamp": datetime.now().isoformat(),
                "source": "Gridradar"
            }
    except Exception as e:
        return {"error": str(e), "frequency": 50.0}
    
    return {"frequency": 50.0, "source": "fallback"}