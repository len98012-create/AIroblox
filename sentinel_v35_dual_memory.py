import os, time, datetime, random, pyautogui, pytesseract, cv2, sys, requests, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from PIL import Image

# --- [KEY 9] HỆ THỐNG TỰ ĐỘNG FIX LỖI 2026 ---
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

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
        """[KEY 9] Chụp ảnh từ buffer Xvfb"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screenshot saved: {path}")
        except Exception as e:
            print(f"⚠️ Scrot failed: {e}")
            if self.driver: self.driver.save_screenshot(path)

    def init_browser(self):
        print("🌐 [INIT] Total Visual Reconstruction (SwiftShader + Forced Paint)...")
        # [KEY 9] Đảm bảo môi trường Display được thiết lập chính xác
        os.environ["DISPLAY"] = ":99"
        
        opt = Options()
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--use-gl=swiftshader") # Render bằng CPU
        
        # --- FLAG CHỐNG MÀN HÌNH ĐEN (OCULUSION) ---
        opt.add_argument("--disable-backgrounding-occluded-windows")
        opt.add_argument("--disable-renderer-backgrounding")
        opt.add_argument("--disable-background-timer-throttling")
        
        opt.add_argument("--window-size=1280,720")
        opt.add_argument("--window-position=0,0")
        opt.add_argument("--force-device-scale-factor=1")
        opt.binary_location = "/usr/bin/chromium-browser"
        
        try:
            service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            self.driver = webdriver.Chrome(service=service, options=opt)
            
            # Ép trình duyệt vẽ một trang có màu sắc mạnh để kích hoạt buffer
            self.driver.get("data:text/html,<body style='background:blue; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0'><h1>SENTINEL RENDERING TEST</h1></body>")
            time.sleep(5) 
            
            print("✅ [DRIVER] Renderer active and buffer initialized.")
        except Exception as e:
            print(f"❌ [CRITICAL] Connection Failed: {e}")
            os.system("fuser -k 9222/tcp || true")
            sys.exit(1)

    def login_roblox(self):
        if not self.cookie:
            self.discord.send("⚠️ No Cookie!")
            return
        try:
            print("🍪 [LOGIN] Injecting Cookie...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5)
            self.driver.add_cookie({"name": ".ROBLOSECURITY", "value": self.cookie, "domain": ".roblox.com"})
            self.driver.refresh()
            time.sleep(12) # Tăng thời gian đợi để render giao diện hoàn tất
            
            self.take_screenshot("logs/login_status.png")
            self.discord.send("🚀 Sentinel Online & Rendering!", "logs/login_status.png")
        except Exception as e:
            self.discord.send(f"❌ Login Error: {e}")

    def run(self):
        self.init_browser()
        self.login_roblox()
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"💓 [HEARTBEAT] {now} - System Stable.")
            pyautogui.moveTo(random.randint(100, 800), random.randint(100, 500))
            pyautogui.press('space')
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
