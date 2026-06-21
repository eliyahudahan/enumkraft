"""
Gridradar API Client - Real grid frequency data
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_current_frequency():
    """Get real-time grid frequency from Gridradar"""
    token = os.getenv('GRIDRADAR_TOKEN')
    
    if not token:
        print("⚠️ No Gridradar token")
        return {"frequency": 50.0, "source": "no_token"}
    
    # Try different endpoints
    endpoints = [
        "https://api.gridradar.net/v1/frequency/current",
        "https://api.gridradar.net/v1/frequency/latest",
        "https://gridradar.net/api/frequency/current"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(
                endpoint,
                headers={"Authorization": f"Bearer {token}"},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Gridradar connected: {endpoint}")
                return {
                    "frequency": data.get("frequency", 50.0),
                    "timestamp": datetime.now().isoformat(),
                    "source": "Gridradar"
                }
        except Exception as e:
            print(f"⚠️ Endpoint failed: {endpoint} - {e}")
            continue
    
    print("❌ All Gridradar endpoints failed")
    return {
        "frequency": 50.0,
        "timestamp": datetime.now().isoformat(),
        "source": "fallback",
        "error": "No working endpoint"
    }

if __name__ == "__main__":
    print("🔌 Testing Gridradar...")
    freq = get_current_frequency()
    print(f"Frequency: {freq.get('frequency')} Hz")
    print(f"Source: {freq.get('source')}")
