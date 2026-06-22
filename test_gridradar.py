import os, requests, time
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('GRIDRADAR_TOKEN')

print("🔌 Testing Gridradar - 3 calls with delay:")
for i in range(3):
    r = requests.post(
        'https://api.gridradar.net/query',
        json={'metric': 'frequency-ucte-median-1s'},
        headers={'Authorization': f'Bearer {token}'}
    )
    if r.status_code == 200:
        data = r.json()
        latest = data[0]['datapoints'][-1]
        print(f"Call {i+1}: {latest}")
    else:
        print(f"Call {i+1}: Error {r.status_code}")
    
    # ⬇️ ההבדל: ממתין 60 שניות בין קריאות
    if i < 2:  # לא צריך לחכות אחרי הקריאה האחרונה
        print("⏳ Waiting 60 seconds to avoid rate limit...")
        time.sleep(60)