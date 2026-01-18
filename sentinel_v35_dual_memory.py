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
            subprocess.run(["scrot", "-z", path], check=True)
            print(f"📸 Screen Captured: {path}")
        except:
            if self.driver: self.driver.save_screenshot(path)

    def init_browser(self):
        """GIỮ NGUYÊN V44 - ĐẢM BẢO HIỂN THỊ"""
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
            self.driver.get("data:text/html,<body style='background:blue; color:white; display:flex; justify-content:center; align-items:center; height:100vh; margin:0'><h1>SENTINEL LIGHT ON</h1></body>")
            time.sleep(5)
            print("✅ [DRIVER] Renderer active.")
        except Exception as e:
            print(f"❌ [CRITICAL] Failed: {e}")
            sys.exit(1)

    def login_roblox(self):
        """NẠP COOKIE JSON TỪ VPN"""
        try:
            print("🍪 [LOGIN] Đang nạp Session từ file cookies.json...")
            self.driver.get("https://www.roblox.com/home")
            time.sleep(5)
            if os.path.exists("cookies.json"):
                with open("cookies.json", "r") as f:
                    cookies = json.load(f)
                    self.driver.delete_all_cookies()
                    for c in cookies:
                        clean_cookie = {k: v for k, v in c.items() if k in ['name', 'value', 'domain', 'path', 'secure', 'httpOnly']}
                        clean_cookie['sameSite'] = c.get('sameSite', 'Lax') if c.get('sameSite') in ["Strict", "Lax", "None"] else "Lax"
                        try: self.driver.add_cookie(clean_cookie)
                        except: pass
                self.driver.refresh()
                time.sleep(10)
                self.take_screenshot("logs/login_final.png")
                return "login" not in self.driver.current_url.lower()
            return False
        except Exception as e:
            self.discord.send(f"❌ Lỗi Login: {e}")
            return False

    def enter_game(self):
        """[KEY 9] TÍCH HỢP POPUP KILLER & AUTO PLAY"""
        try:
            print(f"🎮 [GAME] Đang truy cập PLS DONATE...")
            self.driver.get(self.game_url)
            time.sleep(10)
            
            # KÍCH HOẠT POPUP KILLER: Xóa các bảng overlay chặn màn hình
            print("🛡️ [POPUP KILLER] Đang quét dọn các bảng thông báo chặn nút Play...")
            self.driver.execute_script("""
                var selectors = [
                    '.modal-backdrop', '.modal-dialog', '#modal-confirmation',
                    '.fc-ab-root', '.cookie-banner', '.pdp-login-overlay',
                    '.dark-theme-update-notice'
                ];
                selectors.forEach(s => {
                    var el = document.querySelector(s);
                    if(el) { el.remove(); console.log('Removed: ' + s); }
                });
                // Ép nút Play hiện lên nếu bị ẩn ngầm
                var playBtn = document.querySelector('.btn-common-play-main') || 
                              document.querySelector('[data-testid="play-button"]');
                if(playBtn) { 
                    playBtn.style.zIndex = '9999'; 
                    playBtn.style.opacity = '1';
                    playBtn.click(); 
                }
            """)
            
            time.sleep(15)
            self.take_screenshot("logs/after_popup_killer.png")
            self.discord.send("🎮 Đã dọn dẹp Popup và nhấn Play thành công!", "logs/after_popup_killer.png")
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
