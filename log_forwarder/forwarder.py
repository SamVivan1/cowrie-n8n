import os, json, time, requests

LOG_FILE = "/logs/cowrie.json"
WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

print(f"📡 Cowrie Log Forwarder aktif. Mengirim ke: {WEBHOOK_URL}")

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

if not WEBHOOK_URL:
    raise SystemExit("❌ N8N_WEBHOOK_URL belum diset!")

while True:
    try:
        with open(LOG_FILE, "r") as f:
            for line in follow(f):
                try:
                    data = json.loads(line.strip())
                    requests.post(WEBHOOK_URL, json=data, timeout=3)
                    print("📤", data.get("eventid", "unknown"))
                except Exception as e:
                    print("⚠️ Error kirim log:", e)
    except FileNotFoundError:
        print("⏳ Menunggu file log muncul...")
        time.sleep(5)
