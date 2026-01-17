import os, time, datetime, random, pyautogui, pytesseract, cv2, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image

# --- [KEY 9] LOGGING OPTIMIZATION ---
# Ép Python in log ngay lập tức để không bị treo console trên GitHub Actions
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

class DiscordLink:
    def send(self, msg):
        print(f"📡 [DISCORD] {msg}")

class GhostHumanizer:
    def __init__(self):
        pyautogui.FAILSAFE = False

    def move_mouse_human(self, x, y):
        self.move_human(x, y)

    def move_human(self, x, y):
        start = pyautogui.position()
        control_x = start[0] + random.randint(-100, 100)
        control_y = start[1] + random.randint(-100, 100)
        steps = random.randint(15, 25)
        for i in range(steps):
            t = i / steps
            bx = (1-t)**2 * start[0] + 2*(1-t)*t * control_x + t**2 * x
            by = (1-t)**2 * start[1] + 2*(1-t)*t * control_y + t**2 * y
            pyautogui.moveTo(bx, by)
            time.sleep(0.005)

class VisionSystem:
    def __init__(self, agent):
        self.agent = agent

    def read_text(self):
        path = "logs/ocr_temp.png"
        self.agent.take_screenshot(path)
        return pytesseract.image_to_string(Image.open(path)).lower()

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
        """[FIXED] Cấu hình vượt lỗi DevToolsActivePort trên GitHub Actions"""
        print("🌐 [INIT] Starting Headless Chromium (SHM Patch Applied)...")
        opt = Options()
        
        # Các tham số sống còn
        opt.add_argument("--headless=new")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage") # Quan trọng nhất: tránh crash SHM
        opt.add_argument("--disable-gpu")
        opt.add_argument("--window-size=1280,720")
        opt.add_argument("--remote-debugging-port=9222")
        
        # Chỉ định binary mặc định trên GitHub Runner
        opt.binary_location = "/usr/bin/chromium-browser" 
        
        try:
            self.driver = webdriver.Chrome(options=opt)
            self.driver.set_page_load_timeout(30)
            print("✅ [DRIVER] Browser launched successfully!")
        except Exception as e:
            print(f"❌ [CRITICAL] Browser failed: {e}")
            sys.exit(1)

    def login_roblox(self):
        if not self.cookie:
            print("⚠️ [LOGIN] No Cookie found!")
            return
        
        try:
            print("🍪 [LOGIN] Injecting Cookie...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(3)
            self.driver.add_cookie({
                "name": ".ROBLOSECURITY",
                "value": self.cookie,
                "domain": ".roblox.com"
            })
            self.driver.refresh()
            time.sleep(5)
            self.take_screenshot("logs/login_status.png")
            print("✅ [LOGIN] Roblox Session Restored.")
        except Exception as e:
            print(f"❌ [LOGIN] Failed: {e}")

    def run(self):
        self.init_browser()
        self.login_roblox()
        
        print("🚀 [AGENT] System is active. Entering Main Loop...")
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"💓 [HEARTBEAT] {now} - Sentinel is watching.")
            
            # Chống AFK cơ bản
            self.human.move_human(random.randint(100, 600), random.randint(100, 600))
            pyautogui.press('space')
            
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
