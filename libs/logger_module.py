import requests

class SentinelLogger:
    def __init__(self, webhook_url):
        self.webhook = webhook_url

    def send_discord(self, msg):
        if self.webhook and "PLACEHOLDER" not in self.webhook:
            data = {"content": f"📡 **Sentinel Log**: {msg}"}
            requests.post(self.webhook, json=data)

    def write_file_log(self, msg):
        with open("SENTINEL_V35_LOGS.txt", "a", encoding="utf-8") as f:
            f.write(f"[LOG] {msg}\n")
