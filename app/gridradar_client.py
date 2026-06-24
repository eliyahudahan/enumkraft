"""
Gridradar API Client – Real grid frequency data
Source: https://gridradar.net/api
"""

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

GRIDRADAR_TOKEN = os.getenv('GRIDRADAR_TOKEN')

# 🔑 בדיקה אקטיבית – הטוקן מודפס לצורך ניפוי (ללא תוכן מלא)
if GRIDRADAR_TOKEN:
    print(f"✅ GRIDRADAR_TOKEN loaded (length: {len(GRIDRADAR_TOKEN)})")
else:
    print("❌ GRIDRADAR_TOKEN NOT found in environment!")

# משתני מטמון גלובליים
_cached_frequency = None
_last_fetch_time = 0
FETCH_INTERVAL_SECONDS = 60  # מרווח בטיחות - דקה אחת

def get_current_frequency():
    """
    מביא תדר מ-Gridradar עם מנגנון הגנה מובנה:
    - קריאה לשרת רק אם עברו 60 שניות.
    - מחזיר ערך שמור (Cached) אם לא.
    - מחזיר מידע על מקור הנתון (Live/Cached).
    """
    global _cached_frequency, _last_fetch_time
    
    current_time = time.time()
    time_passed = current_time - _last_fetch_time
    
    # 🔒 הגנה: אם עברו פחות מ-60 שניות – החזר ערך שמור
    if time_passed < FETCH_INTERVAL_SECONDS and _cached_frequency is not None:
        return {
            "frequency": _cached_frequency,
            "source": "Gridradar (Cached)",
            "seconds_until_refresh": int(FETCH_INTERVAL_SECONDS - time_passed)
        }
    
    # אם אין טוקן – חזור ל-Swing Equation מיד
    if not GRIDRADAR_TOKEN:
        print("❌ No Gridradar token, using Swing Equation")
        return {
            "frequency": 50.0,
            "source": "Swing Equation (No Token)",
            "seconds_until_refresh": FETCH_INTERVAL_SECONDS
        }
    
    # 🌐 קריאה אמיתית ל-API (רק אם עבר מספיק זמן)
    try:
        response = requests.post(
            'https://api.gridradar.net/query',
            json={'metric': 'frequency-ucte-median-1s'},
            headers={'Authorization': f'Bearer {GRIDRADAR_TOKEN}'},
            timeout=60  # הגנה מפני תגובה איטית
        )
        
        if response.status_code == 200:
            data = response.json()
            latest = data[0]['datapoints'][-1]
            _cached_frequency = latest[0]
            _last_fetch_time = current_time
            
            return {
                "frequency": _cached_frequency,
                "source": "Gridradar (Live)",
                "seconds_until_refresh": FETCH_INTERVAL_SECONDS
            }
        else:
            print(f"⚠️ Gridradar error {response.status_code}. Using fallback.")
            return {
                "frequency": _cached_frequency if _cached_frequency is not None else 50.0,
                "source": f"Gridradar (Error {response.status_code})",
                "seconds_until_refresh": FETCH_INTERVAL_SECONDS
            }
            
    except requests.exceptions.Timeout:
        print("🔌 Gridradar timeout. Using cached/fallback.")
        return {
            "frequency": _cached_frequency if _cached_frequency is not None else 50.0,
            "source": "Gridradar (Timeout)",
            "seconds_until_refresh": FETCH_INTERVAL_SECONDS
        }
    except Exception as e:
        print(f"🔌 Gridradar error: {e}. Using fallback.")
        return {
            "frequency": _cached_frequency if _cached_frequency is not None else 50.0,
            "source": "Gridradar (Connection Error)",
            "seconds_until_refresh": FETCH_INTERVAL_SECONDS
        }

if __name__ == "__main__":
    print("🔌 Testing protected Gridradar client:")
    print(get_current_frequency())
    time.sleep(60)
    print(get_current_frequency())  # אמור להחזיר Cached