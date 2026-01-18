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
            # Chụp từ frame buffer để đảm bảo ảnh có màu
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screen Captured: {path}")
        except:
            if self.driver: self.driver.save_screenshot(path)

    def init_browser(self):
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
        opt.add_argument("--window-size=1280x720")
        opt.add_argument("--force-device-scale-factor=1")
        # Giả lập User Agent để Roblox không nghi ngờ
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
        """[KEY 9] Ưu tiên đọc file cookies.json bạn vừa tạo"""
        try:
            print("🍪 [LOGIN] Đang nạp Session...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5)

            # Trường hợp 1: Có file cookies.json
            if os.path.exists("cookies.json"):
                print("📂 Phát hiện cookies.json. Đang nạp toàn bộ danh sách...")
                with open("cookies.json", "r") as f:
                    cookies = json.load(f)
                    self.driver.delete_all_cookies() # Dọn dẹp trước khi nạp
                    for c in cookies:
                        # Chuẩn hóa SameSite để tránh lỗi Selenium
                        if 'sameSite' in c and c['sameSite'] not in ["Strict", "Lax", "None"]:
                            c['sameSite'] = "Lax"
                        try:
                            self.driver.add_cookie(c)
                        except:
                            pass
            
            # Trường hợp 2: Không có file nhưng có mã trong Environment (Dự phòng)
            elif self.cookie_env:
                print("🔑 Nạp .ROBLOSECURITY từ Secret...")
                self.driver.add_cookie({"name": ".ROBLOSECURITY", "value": self.cookie_env, "domain": ".roblox.com"})

            self.driver.refresh()
            time.sleep(12)
            
            self.take_screenshot("logs/login_final_check.png")
            if "login" not in self.driver.current_url.lower():
                self.discord.send("🚀 Sentinel Login thành công (JSON)!", "logs/login_final_check.png")
                return True
            else:
                self.discord.send("❌ Login thất bại. Kiểm tra lại nội dung file cookies.json", "logs/login_final_check.png")
                return False
        except Exception as e:
            self.discord.send(f"❌ Lỗi xử lý Cookie: {e}")
            return False

    def enter_game(self):
        try:
            print(f"🎮 [GAME] Truy cập game: {self.game_url}")
            self.driver.get(self.game_url)
            time.sleep(10)
            self.take_screenshot("logs/game_page.png")
            
            print("🕹️ [ACTION] Nhấn nút Play...")
            self.driver.execute_script("""
                var btn = document.querySelector('.btn-common-play-main') || 
                          document.querySelector('[data-testid="play-button"]');
                if(btn) { btn.click(); }
            """)
            time.sleep(15)
            self.take_screenshot("logs/game_launched.png")
            self.discord.send("🎮 Đã kích hoạt Play. Đang chờ vào Server!", "logs/game_launched.png")
        except Exception as e:
            print(f"❌ [GAME ERROR] {e}")

    def run(self):
        self.init_browser()
        if self.login_roblox():
            self.enter_game()
        
        while True:
            now = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"💓 [HEARTBEAT] {now} - Stable.")
            pyautogui.press('space') # Chống AFK
            time.sleep(120)

if __name__ == "__main__":
    agent = SentinelAgent()
    agent.run()
