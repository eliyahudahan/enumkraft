import requests
from datetime import datetime

class SMARDFetcher:
    def __init__(self):
        self.base_url = "https://www.smard.de/app/chart_data"
        self.load_id = "410"  # ייתכן שצריך ID אחר
        
    def get_current_load(self):
        """Get current load - alternative approach"""
        # נשתמש ב-API של SMARD לקבלת נתונים אחרונים
        url = f"{self.base_url}/{self.load_id}/DE/index_hour.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # ✅ פורמט חדש: יש 'timestamps' אבל צריך למצוא את העומס
            # ננסה מקור אחר - אפשר להשתמש ב-SMARD CSV export
            return self._get_load_from_alternative()
        return None
    
    def _get_load_from_alternative(self):
        """Fallback: Use ENTSO-E or return None"""
        # במקרה חירום - נחזיר None ונייצר נתונים מה-DWD
        return None

if __name__ == "__main__":
    smard = SMARDFetcher()
    load = smard.get_current_load()
    print(f"Load: {load} MW (if None - need to fix SMARD endpoint)")