import requests
from datetime import datetime, timedelta
import pandas as pd

def get_germany_generation():
    """Get real generation data for Germany from ENTSO-E"""
    # Register for free token: https://transparency.entsoe.eu/
    TOKEN = "YOUR_TOKEN_HERE"  # תצטרך להחליף בטוקן אמיתי
    
    url = "https://transparency.entsoe.eu/api"
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    
    params = {
        'securityToken': TOKEN,
        'documentType': 'A75',  # Generation
        'in_Domain': '10YCZ-CE-PS-SY',  # Germany
        'periodStart': yesterday.strftime('%Y%m%d%H%M'),
        'periodEnd': now.strftime('%Y%m%d%H%M')
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            print("✅ ENTSO-E data fetched successfully")
            # Parse XML response
            # Note: ENTSO-E returns XML, need to parse
            return response.text
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error fetching ENTSO-E data: {e}")
        return None

if __name__ == "__main__":
    data = get_germany_generation()
    if data:
        print("Data received (first 200 chars):")
        print(data[:200])
