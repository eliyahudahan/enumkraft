import requests

url = "https://www.smard.de/app/chart_data/410/DE/index_hour.json"
r = requests.get(url)
data = r.json()

print("Type:", type(data))
print("Keys:", data.keys() if isinstance(data, dict) else "Not a dict")

# אם יש timestamps – תראה את הראשון
if isinstance(data, dict) and 'timestamps' in data:
    first_ts = data['timestamps'][0] if data['timestamps'] else None
    print(f"First timestamp: {first_ts}")
    
    # נסה לבקש את הערך עבור timestamp ספציפי
    ts_url = f"https://www.smard.de/app/chart_data/410/DE/410_DE_hour_{first_ts}.json"
    print(f"Trying: {ts_url}")
    r2 = requests.get(ts_url)
    print(f"Status: {r2.status_code}")
    if r2.status_code == 200:
        print("Data for first timestamp:", r2.json()[:3])