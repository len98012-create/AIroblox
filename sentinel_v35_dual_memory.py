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
        """[KEY 9 FIX] Sử dụng SCROT thay thế PyAutoGUI để tránh lỗi gnome-screenshot"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            # Chụp trực tiếp từ Buffer của Xvfb (:99)
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screenshot saved via Scrot: {path}")
        except Exception as e:
            print(f"⚠️ Scrot failed, trying Selenium fallback: {e}")
            if self.driver:
                self.driver.save_screenshot(path)
                print(f"📸 Screenshot saved via Driver.")

    def init_browser(self):
        print("🌐 [INIT] Switching to HEADED mode on Xvfb...")
        opt = Options()
        
        # [QUAN TRỌNG] XÓA DÒNG --headless ĐỂ CHROME HIỆN LÊN XVFB
        # opt.add_argument("--headless=new") <--- ĐÃ XÓA
        
        # Cấu hình để chạy ổn định trên Linux
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--disable-gpu")
        
        # Cấu hình hiển thị
        opt.add_argument("--start-maximized")
        opt.add_argument("--window-size=1280,720")
        opt.add_argument("--window-position=0,0") # Ép cửa sổ về góc để chắc chắn lọt vào khung hình
        opt.add_argument("--hide-scrollbars")
        
        # Giả lập người dùng thật
        opt.add_argument("--disable-infobars")
        opt.add_argument("--excludeSwitches=['enable-automation']")
        
        opt.add_argument(f"--user-data-dir=/tmp/sentinel_{random.randint(1000, 9999)}")
        opt.binary_location = "/usr/bin/chromium-browser"
        
        try:
            # Tự động tải Driver
            service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
            self.driver = webdriver.Chrome(service=service, options=opt)
            
            # [Trick] Mở browser xong, đợi 1 chút rồi maximize lại lần nữa để chắc chắn
            print("✅ [DRIVER] Browser launched in DISPLAY :99")
            time.sleep(2)
            self.driver.maximize_window()
            
        except Exception as e:
            print(f"❌ [CRITICAL] Browser failed: {e}")
            sys.exit(1)
            
            print("✅ [DRIVER] Success! Port issue bypassed & Renderer active.")
        except Exception as e:
            print(f"❌ [CRITICAL] Browser still failed: {e}")
            sys.exit(1)

    def login_roblox(self):
        if not self.cookie:
            self.discord.send("⚠️ No Cookie found!")
            return
        try:
            print("🍪 [LOGIN] Injecting Cookie...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5) # Đợi tải trang
            self.driver.add_cookie({"name": ".ROBLOSECURITY", "value": self.cookie, "domain": ".roblox.com"})
            self.driver.refresh()
            time.sleep(10) # [FIX] Tăng thời gian đợi để Roblox load hết giao diện
            
            self.take_screenshot("logs/login_status.png")
            self.discord.send("🚀 Sentinel Online! (Check Image for Black Screen Fix)", "logs/login_status.png")
        except Exception as e:
            self.discord.send(f"❌ Login Error: {e}")

    def run(self):
        self.init_browser()
        self.login_roblox()
        while True:
            now = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"💓 [HEARTBEAT] {now} - System Stable.")
            
            # Di chuyển chuột ngẫu nhiên
            pyautogui.moveTo(random.randint(100, 800), random.randint(100, 500))
            pyautogui.press('space')
            
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
