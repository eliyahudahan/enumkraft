import requests

url = "https://www.smard.de/app/chart_data/410/DE/index_hour.json"
r = requests.get(url)
data = r.json()

print("Type:", type(data))
print("Keys:", data.keys() if isinstance(data, dict) else "Not a dict")

if isinstance(data, dict) and 'timestamps' in data:
    first_ts = data['timestamps'][0] if data['timestamps'] else None
    print(f"First timestamp: {first_ts}")
    
    ts_url = f"https://www.smard.de/app/chart_data/410/DE/410_DE_hour_{first_ts}.json"
    print(f"Trying: {ts_url}")
    r2 = requests.get(ts_url)
    print(f"Status: {r2.status_code}")
    
    if r2.status_code == 200:
        data2 = r2.json()
        # ✅ תיקון: גישה למפתח 'series'
        if 'series' in data2:
            print("First 3 data points:", data2['series'][:3])
        else:
            print("No 'series' key in response. Keys:", data2.keys())