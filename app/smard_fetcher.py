"""
SMARD Fetcher – German electricity load data
Source: Bundesnetzagentur – SMARD (Strommarktdaten)
Two-step API: 1) Get timestamps, 2) Get load values
"""

import requests
from datetime import datetime
import pandas as pd

class SMARDFetcher:
    def __init__(self):
        self.base_url = "https://www.smard.de/app/chart_data"
        self.load_id = "410"  # Germany total load
        
    def _get_timestamps(self):
        """Get list of available timestamps"""
        url = f"{self.base_url}/{self.load_id}/DE/index_hour.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('timestamps', [])
        return []
    
    def _get_load_for_timestamp(self, timestamp):
        """Get load data for a specific timestamp"""
        url = f"{self.base_url}/{self.load_id}/DE/{self.load_id}_DE_hour_{timestamp}.json"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # 'series' is a list of [timestamp, load_mw]
            # load_mw can be None (null) for missing values
            return data.get('series', [])
        return []
    
    def get_current_load(self):
        """
        Get the latest load value for Germany (MW)
        Returns: float or None if no data
        """
        timestamps = self._get_timestamps()
        if not timestamps:
            return None
        
        # Get the most recent timestamp
        latest_ts = timestamps[-1]
        series = self._get_load_for_timestamp(latest_ts)
        
        if series:
            # Find the last non-null value
            for ts, load in reversed(series):
                if load is not None:
                    return load
        return None
    
    def get_load_timeseries(self, hours=48):
        """
        Get load timeseries for the last N hours
        Returns: list of [timestamp, load_mw] for the most recent hours
        """
        timestamps = self._get_timestamps()
        if not timestamps:
            return []
        
        # Get the most recent hours (limited by available data)
        recent_timestamps = timestamps[-hours:] if len(timestamps) >= hours else timestamps
        
        all_data = []
        for ts in recent_timestamps:
            series = self._get_load_for_timestamp(ts)
            if series:
                # Take the last value from each series (should be the most recent hour)
                if series and series[-1][1] is not None:
                    all_data.append(series[-1])
        
        return all_data
    
    def get_load_dataframe(self, hours=48):
        """
        Get load data as Pandas DataFrame
        Returns: DataFrame with columns ['timestamp', 'load_mw']
        """
        data = self.get_load_timeseries(hours)
        if not data:
            return pd.DataFrame(columns=['timestamp', 'load_mw'])
        
        df = pd.DataFrame(data, columns=['timestamp', 'load_mw'])
        # Convert milliseconds to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

if __name__ == "__main__":
    fetcher = SMARDFetcher()
    
    # Test current load
    current = fetcher.get_current_load()
    print(f"Current Load: {current} MW")
    
    # Test timeseries
    df = fetcher.get_load_dataframe(24)
    print(f"Last 24 hours load data:\n{df.head()}")
    if not df.empty:
        print(f"Latest load: {df['load_mw'].iloc[-1]} MW")