import os, time, datetime, random, pyautogui, pytesseract, cv2, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PIL import Image

# --- FIX: Ép in log ngay lập tức để không bị treo console ---
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
        steps = random.randint(15, 25) # Giảm bước để chạy mượt hơn trên Runner
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
        print("🌐 [INIT] Starting Headless Chromium...")
        opt = Options()
        opt.add_argument("--headless=new")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--window-size=1280,720")
        opt.binary_location = "/usr/bin/chromium-browser"
        
        try:
            self.driver = webdriver.Chrome(options=opt)
            print("✅ [DRIVER] Browser launched successfully!")
        except Exception as e:
            print(f"❌ [ERROR] Browser failed: {e}")
            sys.exit(1)

    def login_roblox(self):
        if not self.cookie:
            print("⚠️ [LOGIN] No Cookie found in Environment!")
            return
        
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

    def run(self):
        self.init_browser()
        self.login_roblox()
        
        print("🚀 [AGENT] System is active. Entering Main Loop...")
        # Vòng lặp duy trì sự sống
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"💓 [HEARTBEAT] {now} - Bot is standing by.")
            
            # Giả lập thao tác chống AFK mỗi 2 phút
            self.human.move_human(random.randint(0, 500), random.randint(0, 500))
            pyautogui.press('space')
            
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
