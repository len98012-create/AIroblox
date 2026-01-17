import os, time, datetime, random, pyautogui, pytesseract, cv2, sys, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image

# --- [KEY 9] LOGGING & SYSTEM OPTIMIZATION ---
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

class DiscordLink:
    """Hệ thống báo cáo Discord tích hợp gửi ảnh"""
    def __init__(self):
        self.webhook_url = os.environ.get("DISCORD_WEBHOOK")

    def send(self, msg, image_path=None):
        print(f"📡 [DISCORD] {msg}")
        if not self.webhook_url:
            return
        
        data = {"content": f"🛡️ **[SENTINEL REPORT]** - {msg}"}
        
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    requests.post(self.webhook_url, data=data, files={"file": f}, timeout=10)
            else:
                requests.post(self.webhook_url, json=data, timeout=10)
        except Exception as e:
            print(f"❌ [DISCORD ERROR] {e}")

class GhostHumanizer:
    def __init__(self):
        pyautogui.FAILSAFE = False

    def move_human(self, x, y):
        """Di chuyển chuột theo đường cong để tránh bị phát hiện"""
        start = pyautogui.position()
        steps = random.randint(15, 25)
        for i in range(steps):
            t = i / steps
            # Logic đơn giản hóa Bezier
            curr_x = int(start[0] + (x - start[0]) * t)
            curr_y = int(start[1] + (y - start[1]) * t)
            pyautogui.moveTo(curr_x, curr_y)
            time.sleep(0.005)

class VisionSystem:
    def __init__(self, agent):
        self.agent = agent

    def find_unclaimed_stand(self):
        """[MỚI] Logic tìm gian hàng trống qua OCR"""
        print("🔍 [VISION] Scanning for 'Unclaimed' stands...")
        path = "logs/scan_stands.png"
        self.agent.take_screenshot(path)
        text = pytesseract.image_to_string(Image.open(path)).lower()
        
        if "unclaimed" in text or "claim" in text:
            return True
        return False

class SentinelAgent:
    def __init__(self):
        self.discord = DiscordLink()
        self.human = GhostHumanizer()
        self.vision = VisionSystem(self)
        self.driver = None
        self.cookie = os.environ.get("ROBLOX_COOKIE")

    def take_screenshot(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        pyautogui.screenshot(path)
        print(f"📸 Screenshot saved: {path}")

    def init_browser(self):
        print("🌐 [INIT] Starting Headless Chromium (SHM Patch Applied)...")
        opt = Options()
        opt.add_argument("--headless=new")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--window-size=1280,720")
        opt.binary_location = "/usr/bin/chromium-browser"
        
        try:
            self.driver = webdriver.Chrome(options=opt)
            print("✅ [DRIVER] Browser launched successfully!")
        except Exception as e:
            print(f"❌ [CRITICAL] Browser failed: {e}")
            sys.exit(1)

    def login_roblox(self):
        if not self.cookie:
            self.discord.send("⚠️ Login failed: No Cookie found!")
            return
        
        try:
            print("🍪 [LOGIN] Injecting Cookie...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(3)
            self.driver.add_cookie({"name": ".ROBLOSECURITY", "value": self.cookie, "domain": ".roblox.com"})
            self.driver.refresh()
            time.sleep(5)
            self.take_screenshot("logs/login_status.png")
            self.discord.send("✅ Roblox Session Restored Successfully!", "logs/login_status.png")
        except Exception as e:
            self.discord.send(f"❌ Login Error: {e}")

    def auto_stand_logic(self):
        """Hành động tự động tìm và chiếm gian hàng"""
        if self.vision.find_unclaimed_stand():
            self.discord.send("✨ Potential stand found! Attempting to claim...")
            # Nhấn giữ phím E giả lập trong 2 giây để Claim
            pyautogui.keyDown('e')
            time.sleep(2)
            pyautogui.keyUp('e')
            self.take_screenshot("logs/claim_attempt.png")
            self.discord.send("📸 Claim attempt finished.", "logs/claim_attempt.png")

    def run(self):
        self.init_browser()
        self.login_roblox()
        
        print("🚀 [AGENT] System active. Entering Main Loop...")
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"💓 [HEARTBEAT] {now} - Sentinel is watching.")
            
            # 1. Chống AFK
            self.human.move_human(random.randint(100, 600), random.randint(100, 600))
            pyautogui.press('space')
            
            # 2. Thực hiện tìm gian hàng mỗi 5 chu kỳ
            if random.random() < 0.2:
                self.auto_stand_logic()
            
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
