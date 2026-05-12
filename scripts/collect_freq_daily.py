#!/usr/bin/env python3
import subprocess
import os
from datetime import datetime

# Ensure you are in the project directory
os.chdir("/home/framg/dev/enumkraft")

# Activate virtual environment and run fetcher
subprocess.run(["bash", "-c", "source venv/bin/activate && python scripts/gridradar_fetcher.py"])

# Create backup with timestamp
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
src = "data/frequency_ce.csv"
dst = f"data/frequency_ce_{current_time}.csv"
if os.path.exists(src):
    subprocess.run(["cp", src, dst])
    print(f"Backup saved: {dst}")
else:
    print("No frequency_ce.csv found – check API token or connection")