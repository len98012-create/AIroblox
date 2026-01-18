import os, time, datetime, random, pyautogui, sys, requests, subprocess, json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask
from threading import Thread

# --- [WEB SERVER CHỐNG NGỦ GẬT] ---
app = Flask('')
@app.route('/')
def home():
    return "Sentinel is Alive! 🛡️"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- [KEY 9] HỆ THỐNG TỰ ĐỘNG FIX LỖI 2026 ---
sys.stdout.reconfigure(line_buffering=True)

class DiscordLink:
    def __init__(self):
        self.webhook_url = os.environ.get("DISCORD_WEBHOOK")

    def send(self, msg, image_path=None):
        print(f"📡 [DISCORD] {msg}")
        if not self.webhook_url: return
        data = {"content": f"🛡️ **[SENTINEL REPLIT]** - {msg}"}
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    requests.post(self.webhook_url, data=data, files={"file": f}, timeout=15)
            else:
                requests.post(self.webhook_url, json=data, timeout=15)
        except: pass

class SentinelAgent:
    def __init__(self):
        self.discord = DiscordLink()
        self.driver = None
        self.game_url = "https://www.roblox.com/vi/games/8737602449/PLS-DONATE"

    def take_screenshot(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            subprocess.run(["scrot", "-z", path], check=True)
        except:
            if self.driver: self.driver.save_screenshot(path)

    def init_browser(self):
        """GIỮ NGUYÊN HIỂN THỊ V44"""
        print("🌐 [INIT] Replit Deep Visual (v44)...")
        opt = Options()
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--use-gl=osmesa") 
        opt.add_argument("--window-size=1280,720")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=opt)
            print("✅ Trình duyệt Replit đã sẵn sàng.")
        except Exception as e:
            print(f"❌ [CRITICAL] {e}")
            sys.exit(1)

    def login_roblox(self):
        try:
            print("🍪 Đang nạp cookies.json...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5)
            if os.path.exists("cookies.json"):
                with open("cookies.json", "r") as f:
                    cookies = json.load(f)
                self.driver.delete_all_cookies()
                for c in cookies:
                    clean = {k: v for k, v in c.items() if k in ['name', 'value', 'domain', 'path', 'secure', 'httpOnly']}
                    try: self.driver.add_cookie(clean)
                    except: pass
                self.driver.refresh()
                time.sleep(10)
                self.take_screenshot("logs/login_final.png")
                return "login" not in self.driver.current_url.lower()
            return False
        except: return False

    def enter_game(self):
        """POPUP KILLER TRÊN REPLIT"""
        try:
            self.driver.get(self.game_url)
            time.sleep(10)
            self.driver.execute_script("""
                document.querySelectorAll('.modal-backdrop, .modal-dialog, .cookie-banner, .pdp-login-overlay').forEach(el => el.remove());
                var btn = document.querySelector('.btn-common-play-main, [data-testid="play-button"]');
                if(btn) { btn.click(); }
            """)
            time.sleep(15)
            self.take_screenshot("logs/after_play.png")
            self.discord.send("🎮 Đã dọn dẹp và nhấn Play trên Replit!", "logs/after_play.png")
        except: pass

    def run(self):
        keep_alive() # Khởi động Web Server song song
        self.init_browser()
        if self.login_roblox():
            self.enter_game()
        while True:
            pyautogui.press('space')
            time.sleep(120)

if __name__ == "__main__":
    SentinelAgent().run()
