"""
ENTSO-E Transparency Platform Fetcher
Source: https://transparency.entsoe.eu/
"""

import requests
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

class EntsoeFetcher:
    def __init__(self):
        # Get token from environment or use placeholder
        self.token = os.getenv('ENTSOE_TOKEN', '')
        self.base_url = "https://transparency.entsoe.eu/api"
        self.germany_code = "10YCZ-CE-PS-SY"  # Germany bidding zone
        
        if not self.token:
            print("⚠️ No ENTSO-E token found. Get one at: https://transparency.entsoe.eu/")
    
    def get_generation(self, days_back=1):
        """Get actual generation data for Germany"""
        end = datetime.now()
        start = end - timedelta(days=days_back)
        
        params = {
            'securityToken': self.token,
            'documentType': 'A75',  # Generation
            'in_Domain': self.germany_code,
            'out_Domain': self.germany_code,
            'periodStart': start.strftime('%Y%m%d%H%M'),
            'periodEnd': end.strftime('%Y%m%d%H%M')
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                print("✅ ENTSO-E generation data received")
                return self._parse_xml(response.text)
            else:
                print(f"❌ ENTSO-E error: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ ENTSO-E timeout")
            return None
        except Exception as e:
            print(f"❌ ENTSO-E error: {e}")
            return None
    
    def get_load(self, days_back=1):
        """Get actual load data for Germany"""
        end = datetime.now()
        start = end - timedelta(days=days_back)
        
        params = {
            'securityToken': self.token,
            'documentType': 'A65',  # Load
            'in_Domain': self.germany_code,
            'periodStart': start.strftime('%Y%m%d%H%M'),
            'periodEnd': end.strftime('%Y%m%d%H%M')
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                print("✅ ENTSO-E load data received")
                return self._parse_xml(response.text)
            else:
                print(f"❌ ENTSO-E error: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ ENTSO-E error: {e}")
            return None
    
    def _parse_xml(self, xml_text):
        """Parse ENTSO-E XML response"""
        try:
            root = ET.fromstring(xml_text)
            
            # Extract time series data
            time_series = []
            for ts in root.findall('.//TimeSeries'):
                # Get values
                points = ts.findall('.//Point')
                for point in points:
                    position = point.find('position')
                    quantity = point.find('quantity')
                    if position is not None and quantity is not None:
                        time_series.append({
                            'position': position.text,
                            'quantity': float(quantity.text)
                        })
            
            return {
                'source': 'ENTSO-E',
                'data': time_series,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"❌ XML parsing error: {e}")
            return None
    
    def get_available_data(self):
        """Get list of available data types"""
        return {
            'generation': self.get_generation,
            'load': self.get_load
        }

# Simple function for API
def get_germany_generation():
    fetcher = EntsoeFetcher()
    return fetcher.get_generation()

if __name__ == "__main__":
    print("Testing ENTSO-E Fetcher...")
    fetcher = EntsoeFetcher()
    data = fetcher.get_generation(days_back=1)
    
    if data:
        print(f"Data points: {len(data.get('data', []))}")
    else:
        print("⚠️ ENTSO-E data not available (requires token)")