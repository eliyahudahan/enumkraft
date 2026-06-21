import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_current_frequency():
    token = os.getenv('GRIDRADAR_TOKEN')
    
    if not token:
        print("No Gridradar token found")
        return {"frequency": 50.0, "source": "no_token"}
    
    # Try all possible endpoints
    endpoints = [
        "https://api.gridradar.net/v1/frequency/current",
        "https://api.gridradar.net/v1/frequency/latest",
        "https://gridradar.net/api/frequency/current",
    ]
    
    for url in endpoints:
        try:
            r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=5)
            if r.status_code == 200:
                data = r.json()
                return {
                    "frequency": data.get("frequency", 50.0),
                    "timestamp": datetime.now().isoformat(),
                    "source": "Gridradar"
                }
        except:
            continue
    
    return {"frequency": 50.0, "source": "fallback"}

if __name__ == "__main__":
    freq = get_current_frequency()
    print(f"Frequency: {freq.get('frequency')} Hz")
    print(f"Source: {freq.get('source')}")
