# app/alerting.py
import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(state, cf, load, freq, action):
    """
    Sends a Slack alert for critical grid states.
    Only sends for DUNKELFLAUTE, CRITICAL, or EMERGENCY.
    """
    critical_states = ["⚠️ DUNKELFLAUTE", "🔴 CRITICAL", "🔴🔴 EMERGENCY"]
    if state not in critical_states:
        return

    if not SLACK_WEBHOOK_URL:
        print("⚠️ SLACK_WEBHOOK_URL not set. Alert not sent.")
        return

    emojis = {
        "⚠️ DUNKELFLAUTE": "⚠️",
        "🔴 CRITICAL": "🚨",
        "🔴🔴 EMERGENCY": "🔥"
    }
    colors = {
        "⚠️ DUNKELFLAUTE": "#FFA500",
        "🔴 CRITICAL": "#FF0000",
        "🔴🔴 EMERGENCY": "#8B0000"
    }

    message = {
        "attachments": [{
            "color": colors.get(state, "#000000"),
            "title": f"{emojis.get(state, '📢')} EnumKraft Alert: {state}",
            "text": (
                f"• CF (48h): {cf:.4f}\n"
                f"• Load: {load} MW\n"
                f"• Frequency: {freq} Hz\n"
                f"• Action: {action}"
            ),
            "footer": "EnumKraft 2.0 – Grid Stability Monitor",
            "ts": int(time.time())  # ✅ timestamp אמיתי
        }]
    }

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=message, timeout=5)
        if response.status_code == 200:
            print("✅ Slack alert sent successfully")
        else:
            print(f"⚠️ Slack error: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Slack error: {e}")