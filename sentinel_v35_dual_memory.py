import os, time, datetime, random, pyautogui, sys, requests, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

# --- [KEY 9] HỆ THỐNG TỰ ĐỘNG FIX LỖI 2026 ---
sys.stdout.reconfigure(line_buffering=True)

class DiscordLink:
    def __init__(self):
        self.webhook_url = os.environ.get("DISCORD_WEBHOOK")

    def send(self, msg, image_path=None):
        print(f"📡 [DISCORD] {msg}")
        if not self.webhook_url: return
        data = {"content": f"🛡️ **[SENTINEL REPORT]** - {msg}"}
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    requests.post(self.webhook_url, data=data, files={"file": f}, timeout=15)
            else:
                requests.post(self.webhook_url, json=data, timeout=15)
        except Exception as e:
            print(f"❌ [DISCORD ERROR] {e}")

class SentinelAgent:
    def __init__(self):
        self.discord = DiscordLink()
        self.driver = None
        self.cookie = os.environ.get("ROBLOX_COOKIE")

    def take_screenshot(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            # Chụp trực tiếp từ frame buffer để đảm bảo không bị đen
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screen Captured: {path}")
        except:
            if self.driver: self.driver.save_screenshot(path)

    def init_browser(self):
        print("🌐 [INIT] Deep Visual Reconstruction (v44)...")
        os.environ["DISPLAY"] = ":99"
        
        opt = Options()
        # --- FIX DEVTOOLS BẰNG PIPE (TUYỆT ĐỐI) ---
        opt.add_argument("--remote-debugging-pipe")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        
        # --- FIX MÀN HÌNH ĐEN BẰNG OSMESA ---
        opt.add_argument("--use-gl=osmesa") 
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-backgrounding-occluded-windows")
        
        # Cấu hình thư mục tạm ổn định
        opt.add_argument(f"--user-data-dir=/tmp/sentinel_user")
        opt.add_argument("--window-size=1280,720")
        opt.add_argument("--force-device-scale-factor=1")
        
        try:
            # Khởi tạo Google Chrome Stable
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=opt)
            
            # [KEY 9 TEST] Vẽ nền màu XANH DƯƠNG để xác nhận "Màn hình đã sáng"
            self.driver.get("data:text/html,<body style='background:blue; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0'><h1>SENTINEL LIGHT ON</h1></body>")
            time.sleep(5)
            
            print("✅ [DRIVER] Renderer active. System thắp sáng thành công!")
        except Exception as e:
            print(f"❌ [CRITICAL] Failed: {e}")
            os.system("pkill -9 chrome || true")
            sys.exit(1)

    def login_roblox(self):
        if not self.cookie:
            self.discord.send("⚠️ Cookie missing!")
            return
        try:
            print("🍪 [LOGIN] Injecting Cookie...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5)
            self.driver.add_cookie({"name": ".ROBLOSECURITY", "value": self.cookie, "domain": ".roblox.com"})
            self.driver.refresh()
            time.sleep(10)
            
            self.take_screenshot("logs/login_status.png")
            self.discord.send("🚀 Sentinel v44 Online!", "logs/login_status.png")
        except Exception as e:
            self.discord.send(f"❌ Login Error: {e}")

    def run(self):
        self.init_browser()
        self.login_roblox()
        while True:
            print(f"💓 [HEARTBEAT] {datetime.datetime.now().strftime('%H:%M:%S')} - Stable.")
            pyautogui.press('space')
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
