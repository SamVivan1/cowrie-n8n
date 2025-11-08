import os
import json
import time
import requests

LOG_FILE = "/logs/cowrie.json"
WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

if not WEBHOOK_URL:
    raise ValueError("❌ Environment variable N8N_WEBHOOK_URL is not set!")

print(f"✅ Cowrie log forwarder started. Sending logs to: {WEBHOOK_URL}")

def follow(file):
    file.seek(0, 2)  # move to end of file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

try:
    with open(LOG_FILE, "r") as logfile:
        loglines = follow(logfile)
        for line in loglines:
            try:
                data = json.loads(line.strip())
                requests.post(WEBHOOK_URL, json=data, timeout=5)
                print(f"📤 Sent log event: {data.get('eventid', 'unknown')}")
            except json.JSONDecodeError:
                print("⚠️ Skipping invalid JSON line.")
            except requests.RequestException as e:
                print(f"❌ Failed to send log: {e}")
except FileNotFoundError:
    print(f"❌ Log file not found at {LOG_FILE}. Check Cowrie volume mapping.")
