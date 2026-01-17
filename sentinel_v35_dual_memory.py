
#!/usr/bin/env python3
"""
Sentinel Cyber-Wraith v7.7.0
============================
Features:
1. RecoveryEngine: Detects frozen screens and refreshes.
2. Discord Link: Rich embeds for monitoring.
3. Ghost Protocol: Human-like mouse spline movement.
4. Dual Memory: Local logs + Cloud Sync.
"""

import sys, os, subprocess, time, importlib, traceback, random, threading, glob, math, shutil
from datetime import datetime
from pathlib import Path

# --- BOOTSTRAP LOADER ---
class SmartLoader:
    def __init__(self, lib_path="libs"):
        self.lib_path = os.path.abspath(lib_path)
        if self.lib_path not in sys.path: sys.path.insert(0, self.lib_path)
        os.makedirs(lib_path, exist_ok=True)
    
    def ensure_import(self):
        global requests, psutil, cv2, np, pytesseract, pyautogui, webdriver, Options
        import requests, psutil, cv2, pytesseract, pyautogui
        import numpy as np
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

loader = SmartLoader()
loader.ensure_import()

# --- CONFIGURATION ---
BRAIN_URL = "http://localhost:5000"
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
EXTENSION_DIR = "extensions"
SCREENSHOT_DIR = "logs/screenshots"
os.makedirs(EXTENSION_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# --- UTILITIES ---
def log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    print(f"[{ts}] 👻 {msg}")

class DiscordLink:
    def __init__(self):
        self.url = DISCORD_WEBHOOK
        self.queue = []
        self.start_worker()

    def start_worker(self):
        def worker():
            while True:
                if self.queue:
                    payload = self.queue.pop(0)
                    try: requests.post(self.url, json=payload, timeout=5)
                    except: pass
                time.sleep(1)
        threading.Thread(target=worker, daemon=True).start()

    def send(self, title, desc, color=0x00f2ff, fields=None):
        if not self.url: return
        embed = {
            "title": title,
            "description": desc,
            "color": color,
            "footer": {"text": "Sentinel v7.7.0"},
            "timestamp": datetime.utcnow().isoformat()
        }
        if fields: embed["fields"] = fields
        self.queue.append({"embeds": [embed]})

# --- CORE MODULES ---
class GhostHumanizer:
    def __init__(self):
        pyautogui.FAILSAFE = False

    def move_human(self, x, y):
        start = pyautogui.position()
        control_x = start[0] + random.randint(-100, 100)
        control_y = start[1] + random.randint(-100, 100)
        
        steps = random.randint(20, 40)
        for i in range(steps):
            t = i / steps
            bx = (1-t)**2 * start[0] + 2*(1-t)*t * control_x + t**2 * x
            by = (1-t)**2 * start[1] + 2*(1-t)*t * control_y + t**2 * y
            pyautogui.moveTo(bx, by)
            time.sleep(random.uniform(0.001, 0.01))

class VisionSystem:
    def __init__(self, agent):
        self.agent = agent
        self.last_screen_hash = 0
        self.stuck_counter = 0

    def get_screen(self, path="logs/view.png"):
        self.agent.screenshot(path)
        return cv2.imread(path)

    def check_frozen(self):
        """Checks if the screen hasn't changed in a while (Crash detection)"""
        img = self.get_screen("/tmp/freeze_check.png")
        if img is None: return False
        
        current_hash = hash(img.tobytes())
        if current_hash == self.last_screen_hash:
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0
            self.last_screen_hash = current_hash
            
        return self.stuck_counter > 20 # ~5-10 mins stuck

class SentinelAgent:
    def __init__(self):
        self.discord = DiscordLink()
        self.human = GhostHumanizer()
        self.vision = VisionSystem(self)
        self.driver = None
        self.start_time = time.time()

    def screenshot(self, path):
        try:
            pyautogui.screenshot(path)
        except:
            os.system(f"scrot -q 90 {path} >/dev/null 2>&1")

    def recover_session(self):
        log("🔄 RecoveryEngine: Refreshing Session...")
        self.discord.send("⚠️ STUCK DETECTED", "Screen frozen. Triggering refresh.", 0xffcc00)
        try:
            self.driver.refresh()
            time.sleep(15)
        except:
            pass

    def load_extensions(self):
        sys.path.append(os.path.abspath(EXTENSION_DIR))
        for f in glob.glob(f"{EXTENSION_DIR}/skill_*.py"):
            try:
                name = Path(f).stem
                mod = importlib.import_module(name)
                importlib.reload(mod)
                if hasattr(mod, 'execute'):
                    mod.execute(self)
            except Exception as e:
                log(f"Skill Error ({name}): {e}")

    def run(self):
        log("🚀 Sentinel v7.7.0 Cyber-Wraith Initialized.")
        self.discord.send("🚀 ONLINE", "Sentinel Agent v7.7.0 started.", 0x00ff00)
        
        opts = Options()
        opts.add_argument("--mute-audio")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--window-size=1280,720")
        opts.add_argument("--disable-gpu")
        
        self.driver = webdriver.Chrome(options=opts)
        self.driver.get("https://www.roblox.com")
        
        try:
            while True:
                # 1. Vision Check
                if self.vision.check_frozen():
                    self.recover_session()
                
                # 2. Extensions
                self.load_extensions()
                
                # 3. Evolution Call
                if random.random() < 0.05:
                    threading.Thread(target=lambda: requests.post(f"{BRAIN_URL}/evolve")).start()
                
                # 4. Anti-AFK
                if random.random() < 0.1:
                    self.human.move_human(random.randint(100, 1100), random.randint(100, 600))
                
                time.sleep(15)
                
        except KeyboardInterrupt:
            log("🛑 Manual Stop")
        except Exception as e:
            log(f"🔥 CRITICAL: {e}")
            self.discord.send("🔥 CRITICAL FAIL", str(e)[:200], 0xff0000)
            with open("logs/crash.log", "w") as f: f.write(traceback.format_exc())
            # Attempt self-heal
            requests.post(f"{BRAIN_URL}/self_heal", json={"traceback": str(e)})
        finally:
            if self.driver: self.driver.quit()

if __name__ == "__main__":
    if not os.environ.get("DISPLAY"):
        subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1280x720x24", "-ac"])
        os.environ["DISPLAY"] = ":99"
    SentinelAgent().run()
