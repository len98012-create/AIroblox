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
        self.cookie_secret = os.environ.get("ROBLOX_COOKIE")
        self.game_url = "https://www.roblox.com/vi/games/8737602449/PLS-DONATE"

    def take_screenshot(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screen Captured: {path}")
        except:
            if self.driver: self.driver.save_screenshot(path)

    def init_browser(self):
        """BẢN V44 - GIỮ NGUYÊN HIỂN THỊ ỔN ĐỊNH"""
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
        
        # [KEY 9] Giả lập User Agent để khớp với trình duyệt của bạn
        opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=opt)
            self.driver.get("data:text/html,<body style='background:blue; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0'><h1>SENTINEL LIGHT ON</h1></body>")
            time.sleep(5)
            print("✅ [DRIVER] Renderer active.")
        except Exception as e:
            print(f"❌ [CRITICAL] Failed: {e}")
            sys.exit(1)

    def login_roblox(self):
        """[KEY 9] Nạp Cookie từ file JSON hoặc Secret"""
        try:
            print("🍪 [LOGIN] Bắt đầu quá trình nạp Session...")
            self.driver.get("https://www.roblox.com/")
            time.sleep(5)

            # Ưu tiên 1: Nạp từ file cookies.json (nếu bạn đã upload)
            if os.path.exists("cookies.json"):
                print("📂 Tìm thấy cookies.json. Đang nạp toàn bộ Session...")
                with open("cookies.json", "r") as f:
                    cookies_list = json.load(f)
                    for c in cookies_list:
                        if 'sameSite' in c and c['sameSite'] not in ["Strict", "Lax", "None"]:
                            c['sameSite'] = "Lax"
                        try: self.driver.add_cookie(c)
                        except: pass
            # Ưu tiên 2: Nạp mã .ROBLOSECURITY từ Secret
            elif self.cookie_secret:
                print("🔑 Nạp .ROBLOSECURITY từ Secret...")
                self.driver.add_cookie({"name": ".ROBLOSECURITY", "value": self.cookie_secret, "domain": ".roblox.com"})
            
            self.driver.refresh()
            time.sleep(12)
            
            self.take_screenshot("logs/login_final.png")
            if "login" not in self.driver.current_url.lower():
                self.discord.send("🚀 Sentinel Login thành công!", "logs/login_final.png")
                return True
            else:
                self.discord.send("❌ Đăng nhập thất bại. Hãy kiểm tra lại Cookie JSON/Secret.", "logs/login_final.png")
                return False
        except Exception as e:
            self.discord.send(f"❌ Login Error: {e}")
            return False

    def enter_game(self):
        try:
            print(f"🎮 [GAME] Đang truy cập PLS DONATE...")
            self.driver.get(self.game_url)
            time.sleep(10)
            self.take_screenshot("logs/game_page.png")
            
            print("🕹️ [ACTION] Đang nhấn nút Play...")
            self.driver.execute_script("""
                var playBtn = document.querySelector('.btn-common-play-main') || 
                              document.querySelector('[data-testid="play-button"]');
                if(playBtn) { playBtn.click(); }
            """)
            time.sleep(15)
            self.take_screenshot("logs/after_play.png")
            self.discord.send("🎮 Đã nhấn nút Play!", "logs/after_play.png")
        except Exception as e:
            print(f"❌ [GAME ERROR] {e}")

    def run(self):
        self.init_browser()
        if self.login_roblox():
            self.enter_game()
        
        while True:
            print(f"💓 [HEARTBEAT] {datetime.datetime.now().strftime('%H:%M:%S')} - Stable.")
            pyautogui.press('space')
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
