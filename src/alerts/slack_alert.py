import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

COOLDOWN_SECONDS = 300
_last_sent = {}


def send_slack_alert(message: str):
    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL not set — skipping alert.")
        return

    payload = {"text": f"🚨 *PulseWatch Alert*\n{message}"}

    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"Slack alert sent: {message}")
        else:
            print(f"Slack alert failed ({response.status_code}): {response.text}")
    except Exception as e:
        print(f"Failed to send Slack alert: {e}")


def send_alert_with_cooldown(alert_key: str, message: str):
    now = time.time()
    last_time = _last_sent.get(alert_key, 0)

    if now - last_time < COOLDOWN_SECONDS:
        print(f"Skipping alert (cooldown active): {alert_key}")
        return

    send_slack_alert(message)
    _last_sent[alert_key] = now
