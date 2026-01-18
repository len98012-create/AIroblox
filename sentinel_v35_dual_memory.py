import os, time, datetime, random, pyautogui, sys, requests, subprocess, json
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
        self.cookie_env = os.environ.get("ROBLOX_COOKIE")
        self.game_url = "https://www.roblox.com/vi/games/8737602449/PLS-DONATE"

    def take_screenshot(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            # GIỮ NGUYÊN: Cách chụp scrot của v44 để ảnh không bị đen
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screen Captured: {path}")
        except:
            if self.driver: self.driver.save_screenshot(path)

    def init_browser(self):
        """HÀM INIT V44 - KHÔNG THAY ĐỔI MÀN HÌNH"""
        print("🌐 [INIT] Deep Visual Reconstruction (v44)...")
        os.environ["DISPLAY"] = ":99"
        
        opt = Options()
        opt.add_argument("--remote-debugging-pipe")
        opt.add_argument("--no-sandbox")
        opt.add_argument("--disable-dev-shm-usage")
        opt.add_argument("--use-gl=osmesa") 
        opt.add_argument("--disable-gpu")
        opt.add_argument("--disable-backgrounding-occluded-windows")
        opt.add_argument(f"--user-data-dir=/tmp/sentinel_user")
        opt.add_argument("--window-size=1280,720")
        opt.add_argument("--force-device-scale-factor=1")
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=opt)
            
            # GIỮ NGUYÊN: Test màn hình xanh để kích hoạt renderer
            self.driver.get("data:text/html,<body style='background:blue; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0'><h1>SENTINEL LIGHT ON</h1></body>")
            time.sleep(5)
            print("✅ [DRIVER] Renderer active. System thắp sáng thành công!")
        except Exception as e:
            print(f"❌ [CRITICAL] Failed: {e}")
            os.system("pkill -9 chrome || true")
            sys.exit(1)

    def login_roblox(self):
        """CẬP NHẬT: Chỉ sửa logic nạp Cookie để đọc file cookies.json"""
        try:
            print("🍪 [LOGIN] Đang nạp Session từ file cookies.json...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5)

            if os.path.exists("cookies.json"):
                with open("cookies.json", "r") as f:
                    cookies = json.load(f)
                    self.driver.delete_all_cookies()
                    for c in cookies:
                        # Chỉ lấy các trường cần thiết để Selenium không báo lỗi
                        clean_cookie = {}
                        for key in ['name', 'value', 'domain', 'path', 'secure', 'httpOnly']:
                            if key in c: clean_cookie[key] = c[key]
                        
                        # Chuẩn hóa SameSite
                        if 'sameSite' in c and c['sameSite'] in ["Strict", "Lax", "None"]:
                            clean_cookie['sameSite'] = c['sameSite']
                        else:
                            clean_cookie['sameSite'] = "Lax"
                            
                        try: self.driver.add_cookie(clean_cookie)
                        except: pass
                
                self.driver.refresh()
                time.sleep(10)
                
                self.take_screenshot("logs/login_final.png")
                if "login" not in self.driver.current_url.lower():
                    self.discord.send("🚀 Sentinel Login thành công (JSON)!", "logs/login_final.png")
                    return True
            
            # Dự phòng: Nếu không có file JSON, dùng Cookie môi trường
            if self.cookie_env:
                self.driver.add_cookie({"name": ".ROBLOSECURITY", "value": self.cookie_env, "domain": ".roblox.com"})
                self.driver.refresh()
                time.sleep(10)
                return "login" not in self.driver.current_url.lower()

            return False
        except Exception as e:
            self.discord.send(f"❌ Lỗi Login: {e}")
            return False

    def enter_game(self):
        """GIỮ NGUYÊN: Logic vào game V44"""
        try:
            print(f"🎮 [GAME] Đang truy cập PLS DONATE...")
            self.driver.get(self.game_url)
            time.sleep(10)
            self.take_screenshot("logs/game_page.png")
            
            print("🕹️ [ACTION] Đang nhấn nút Play...")
            self.driver.execute_script("""
                var btn = document.querySelector('.btn-common-play-main') || 
                          document.querySelector('[data-testid="play-button"]');
                if(btn) { btn.click(); }
            """)
            time.sleep(15)
            self.take_screenshot("logs/after_play.png")
            self.discord.send("🎮 Đã thực hiện nhấn Play.", "logs/after_play.png")
        except Exception as e:
            print(f"❌ [GAME ERROR] {e}")

    def run(self):
        self.init_browser()
        if self.login_roblox():
            self.enter_game()
        
        while True:
            now = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"💓 [HEARTBEAT] {now} - Sentinel đang hoạt động.")
            pyautogui.press('space')
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
