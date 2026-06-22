"""
ENTSO-E Fetcher – Real generation and load data for Germany
Using official entsoe-py library
"""

from entsoe import EntsoePandasClient
import pandas as pd
from datetime import datetime, timedelta
import os

class EntsoeFetcher:
    def __init__(self):
        self.token = os.getenv('ENTSOE_TOKEN')  # תשמור את הטוקן ב-.env
        self.client = EntsoePandasClient(api_key=self.token)
        self.germany_code = '10YCZ-CE-PS-SY'  # Germany bidding zone
        
    def get_current_load(self):
        """Get current load for Germany (MW)"""
        try:
            # Load data for last 24 hours
            end = datetime.now()
            start = end - timedelta(hours=24)
            load_df = self.client.query_load(self.germany_code, start=start, end=end)
            return load_df.iloc[-1] if not load_df.empty else None
        except Exception as e:
            print(f"Error fetching load: {e}")
            return None
    
    def get_generation_by_type(self):
        """Get generation by type (wind, solar, etc.)"""
        try:
            end = datetime.now()
            start = end - timedelta(hours=24)
            gen_df = self.client.query_generation(self.germany_code, start=start, end=end)
            return gen_df.iloc[-1] if not gen_df.empty else None
        except Exception as e:
            print(f"Error fetching generation: {e}")
            return None

if __name__ == "__main__":
    fetcher = EntsoeFetcher()
    load = fetcher.get_current_load()
    gen = fetcher.get_generation_by_type()
    print(f"Current Load: {load} MW")
    print(f"Generation: {gen}")