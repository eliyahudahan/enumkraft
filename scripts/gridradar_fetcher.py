import os
import requests
import pandas as pd
from datetime import datetime, timezone
import time
from dotenv import load_dotenv

# ==========================================================
# טוען טוקן מקובץ .env (לא ב‑GitHub)
# ==========================================================
load_dotenv()
TOKEN = os.getenv("GRIDRADAR_TOKEN")
if not TOKEN:
    raise Exception("GRIDRADAR_TOKEN not found in .env file")

URL = "https://api.gridradar.net/query"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def fetch_frequency_chunk(aggr="5s"):
    """מחזיר DataFrame של תדרים (frequency_ucte_median) עבור פרק זמן של כשעה"""
    payload = {
        "metric": "frequency-ucte-median-1s",
        "aggr": aggr,
        "format": "json"
    }
    resp = requests.post(URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f"API error {resp.status_code}: {resp.text}")
    data = resp.json()
    records = []
    for series in data:
        pmu = series["target"]
        for freq, ts_str in series["datapoints"]:
            records.append({
                "timestamp": pd.to_datetime(ts_str),
                "pmu": pmu,
                "frequency_hz": freq
            })
    df = pd.DataFrame(records)
    return df

def collect_frequency_hours(hours=3, aggr="5s", out_csv="data/frequency_ce.csv"):
    """אוסף נתונים למספר שעות (החשבון החינמי: קריאה אחת ≈ שעה)"""
    all_data = []
    for i in range(hours):
        print(f"Fetching hour {i+1}/{hours} (aggr={aggr})...")
        start = datetime.now(timezone.utc)
        df_chunk = fetch_frequency_chunk(aggr)
        all_data.append(df_chunk)
        elapsed = (datetime.now(timezone.utc) - start).total_seconds()
        wait = max(0, 3600 - elapsed)
        if hours > 1 and i < hours-1:
           time.sleep(wait)
           
    final_df = pd.concat(all_data, ignore_index=True)
    final_df = final_df.drop_duplicates(subset=["timestamp", "pmu"])
    final_df = final_df.sort_values("timestamp")

      
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    if os.path.exists(out_csv):
       print(f"Overwriting existing file: {out_csv}")

    final_df.to_csv(out_csv, index=False)
    print(f"Saved {len(final_df)} points to {out_csv}")
    print(f"Collected {len(final_df)} points from {len(all_data)} chunks")
   
    return final_df

if __name__ == "__main__":
    # איסוף 3 שעות (ניתן לשנות ל‑2 או 4 בהתאם לצורך)
    df = collect_frequency_hours(hours=1, aggr="5s")
    print(df.head())