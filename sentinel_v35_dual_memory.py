import os, time, datetime, random, pyautogui, pytesseract, cv2, sys, subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

# --- [KEY 9] LOGGING OPTIMIZATION ---
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

class DiscordLink:
    def send(self, msg):
        print(f"📡 [DISCORD] {msg}")

class GhostHumanizer:
    def __init__(self):
        pyautogui.FAILSAFE = False

    def move_human(self, x, y):
        start = pyautogui.position()
        steps = random.randint(10, 20)
        for i in range(steps):
            t = i / steps
            curr_x = int(start[0] + (x - start[0]) * t)
            curr_y = int(start[1] + (y - start[1]) * t)
            pyautogui.moveTo(curr_x, curr_y)
            time.sleep(0.01)

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
        """Sử dụng Scrot để chụp ảnh trực tiếp từ màn hình ảo Xvfb"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            # Chụp toàn bộ màn hình :99
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screenshot saved via Scrot: {path}")
        except:
            # Fallback nếu scrot lỗi
            pyautogui.screenshot(path)
            print(f"📸 Screenshot saved via PyAutoGUI: {path}")

    def init_browser(self):
        """[FIXED] Cấu hình chống màn hình đen trên GitHub Actions"""
        print("🌐 [INIT] Fixing Black Screen (Force Rendering)...")
        opt = Options()
        
        # Tham số quan trọng để ép render
        opt.add_argument("--headless=old") # Đôi khi 'old' ổn định hơn 'new' trên Ubuntu cũ
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--disable-gpu")
        opt.add_argument("--window-size=1280,720")
        opt.add_argument("--force-device-scale-factor=1")
        opt.add_argument("--hide-scrollbars")
        
        opt.binary_location = "/usr/bin/chromium-browser" 
        
        try:
            self.driver = webdriver.Chrome(options=opt)
            # Ép trình duyệt mở trang trắng để kích hoạt render engine
            self.driver.get("about:blank")
            time.sleep(2)
            print("✅ [DRIVER] Browser engine is active.")
        except Exception as e:
            print(f"❌ [CRITICAL] Browser failed: {e}")
            sys.exit(1)

    def login_roblox(self):
        if not self.cookie:
            print("⚠️ [LOGIN] No Cookie found!")
            return
        
        try:
            print("🍪 [LOGIN] Injecting Cookie & Redirecting...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5) # Đợi trang load hẳn
            self.driver.add_cookie({
                "name": ".ROBLOSECURITY",
                "value": self.cookie,
                "domain": ".roblox.com"
            })
            self.driver.get("https://www.roblox.com/home")
            time.sleep(10) # Đợi render sau khi login
            self.take_screenshot("logs/login_status.png")
            print("✅ [LOGIN] Session restored. Checking visibility...")
        except Exception as e:
            print(f"❌ [LOGIN] Failed: {e}")

    def run(self):
        self.init_browser()
        self.login_roblox()
        
        print("🚀 [AGENT] System active. Entering Main Loop...")
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            # Cứ mỗi 10 phút lại chụp một ảnh để kiểm tra "màn hình đen"
            if int(time.time()) % 600 < 120:
                self.take_screenshot(f"logs/monitor_{now}.png")
                
            self.human.move_human(random.randint(100, 600), random.randint(100, 600))
            pyautogui.press('space')
            print(f"💓 [HEARTBEAT] {now} - Monitoring...")
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
