
#!/usr/bin/env python3
"""
Sentinel Infinite Engine v7.5 (Ghost Protocol - Anti Ban)
=========================================================
Features:
1. Human Motor Control: Mouse overshoot, jitter, variable speed.
2. Typing Simulator: Variable WPM, micro-pauses.
3. Admin Watchdog: Auto-disconnect on threat detection.
4. Evolution Loop: Self-coding capabilities.

Author: Sentinel SRE Team
"""

import sys
import os
import subprocess
import time
import importlib
import traceback
import random
import threading
import glob
import math
from pathlib import Path

# --- 1. SMART LOADER ---
class SmartLoader:
    def __init__(self, lib_path="libs"):
        self.lib_path = os.path.abspath(lib_path)
        if self.lib_path not in sys.path:
            sys.path.insert(0, self.lib_path)
        os.makedirs(self.lib_path, exist_ok=True)

    def ensure(self, package_name, import_name=None):
        import_name = import_name or package_name
        try:
            importlib.import_module(import_name)
        except ImportError:
            print(f"📦 [LOADER] Installing {package_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--target", self.lib_path, package_name], stdout=subprocess.DEVNULL)

loader = SmartLoader()
loader.ensure("requests")
loader.ensure("psutil")
loader.ensure("opencv-python-headless", "cv2")
loader.ensure("pytesseract")
loader.ensure("numpy")
loader.ensure("pyautogui")

import requests
import psutil
import cv2
import numpy as np
import pytesseract
import pyautogui

# --- CONFIG ---
BRAIN_URL = "http://localhost:5000"
EXTENSION_DIR = "extensions"
os.makedirs(EXTENSION_DIR, exist_ok=True)
DANGER_KEYWORDS = ["admin", "mod", "banned", "report", "hacking", "bot"]

def log_console(msg):
    print(f"[{time.strftime('%H:%M:%S')}] 👻 {msg}")

# --- MODULE: GHOST PROTOCOL (HUMAN BEHAVIOR) ---
class GhostHumanizer:
    def __init__(self):
        pyautogui.FAILSAFE = False
        self.screen_w, self.screen_h = pyautogui.size()

    def _ease_out_quad(self, n):
        return -n * (n - 2)

    def move_mouse_human(self, x, y, speed_factor=1.0):
        """Di chuyển chuột với độ trượt và run tay giả lập"""
        start_x, start_y = pyautogui.position()
        
        # 1. Randomize target slightly (Pixel perfect is robotic)
        target_x = x + random.randint(-3, 3)
        target_y = y + random.randint(-3, 3)

        # 2. Add "Overshoot" (Di chuyển quá đà rồi kéo lại)
        if random.random() < 0.3:
            overshoot_x = target_x + random.randint(-20, 20)
            overshoot_y = target_y + random.randint(-20, 20)
            self._move_curve(start_x, start_y, overshoot_x, overshoot_y, speed_factor)
            time.sleep(random.uniform(0.05, 0.15)) # Reaction time
            start_x, start_y = overshoot_x, overshoot_y

        self._move_curve(start_x, start_y, target_x, target_y, speed_factor)

    def _move_curve(self, x1, y1, x2, y2, speed):
        dist = math.hypot(x2 - x1, y2 - y1)
        duration = (random.uniform(0.2, 0.5) + (dist / 2000)) / speed
        
        steps = int(duration * 60)
        if steps == 0: steps = 1
        
        # Bezier Control Points
        cp1_x = x1 + random.randint(-100, 100)
        cp1_y = y1 + random.randint(-100, 100)
        
        for i in range(steps):
            t = i / steps
            t_smooth = self._ease_out_quad(t)
            
            # Cubic Bezier Formula
            bx = (1-t_smooth)**3*x1 + 3*(1-t_smooth)**2*t_smooth*cp1_x + t_smooth**3*x2
            by = (1-t_smooth)**3*y1 + 3*(1-t_smooth)**2*t_smooth*cp1_y + t_smooth**3*y2
            
            # Add micro-jitter (Run tay)
            bx += random.uniform(-1, 1)
            by += random.uniform(-1, 1)
            
            pyautogui.moveTo(bx, by)
            time.sleep(duration / steps)

    def type_human(self, text):
        """Gõ phím như người, có delay, có sai sót"""
        for char in text:
            pyautogui.typewrite(char)
            # Tốc độ gõ biến thiên
            time.sleep(random.uniform(0.05, 0.15))
            
            # Giả lập suy nghĩ giữa câu
            if char in [' ', ',', '.']:
                time.sleep(random.uniform(0.1, 0.3))
                
            # Random typo (1% chance) - Gõ sai rồi xóa
            if random.random() < 0.01:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                pyautogui.typewrite(wrong_char)
                time.sleep(0.1)
                pyautogui.press('backspace')
                time.sleep(0.1)

# --- MODULE: VISION & SAFETY ---
class VisionEngine:
    def capture_screen(self):
        return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
    
    def read_text(self):
        try:
            # Preprocess for better OCR
            img = np.array(pyautogui.screenshot())
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            return pytesseract.image_to_string(gray).strip().lower()
        except: return ""

class AdminWatchdog:
    def __init__(self, agent):
        self.agent = agent
        
    def scan_threats(self):
        """Quét màn hình tìm từ khóa Admin/Report"""
        text = self.agent.vision.read_text()
        for kw in DANGER_KEYWORDS:
            if kw in text:
                log_console(f"🚨 THREAT DETECTED: '{kw}' found on screen!")
                self.emergency_shutdown()
                
    def emergency_shutdown(self):
        """Thoát game ngay lập tức"""
        log_console("⚡ ACTIVATING KILL SWITCH...")
        pyautogui.hotkey('alt', 'f4')
        time.sleep(1)
        # Nếu cần thiết, đóng luôn trình duyệt bằng lệnh hệ thống
        os.system("pkill chrome")
        sys.exit(0)

# --- EVOLUTION MANAGER ---
class EvolutionManager:
    def __init__(self, agent):
        self.agent = agent
        self.loaded_skills = set()
        self.last_evolve_time = time.time() # Delay start

    def load_new_skills(self):
        sys.path.append(os.path.abspath(EXTENSION_DIR))
        files = glob.glob(os.path.join(EXTENSION_DIR, "skill_*.py"))
        for f in files:
            name = Path(f).stem
            if name not in self.loaded_skills:
                try:
                    if name in sys.modules: importlib.reload(sys.modules[name])
                    else: importlib.import_module(name)
                    mod = sys.modules[name]
                    if hasattr(mod, 'execute'):
                        log_console(f"✨ Learned: {name}")
                        mod.execute(self.agent)
                        self.loaded_skills.add(name)
                except Exception as e:
                    print(f"Skill error: {e}")

    def trigger_evolution(self):
        # Chỉ tạo code mới khi an toàn và rảnh rỗi (mỗi 5 phút)
        if time.time() - self.last_evolve_time > 300: 
            threading.Thread(target=self._async_evolve).start()
            self.last_evolve_time = time.time()

    def _async_evolve(self):
        try: requests.post(f"{BRAIN_URL}/evolve", json={}, timeout=20)
        except: pass

# --- MAIN AGENT ---
class SentinelAgent:
    def __init__(self):
        self.human = GhostHumanizer() # Thay thế chuột cũ
        self.vision = VisionEngine()
        self.watchdog = AdminWatchdog(self)
        self.evolution = EvolutionManager(self)
        self.pg = pyautogui

    def run(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        opts = Options()
        opts.add_argument("--mute-audio")
        driver = webdriver.Chrome(options=opts)
        driver.set_window_size(1280, 720)
        
        try:
            log_console("🚀 Sentinel v7.5 Ghost Protocol Active.")
            driver.get("https://www.roblox.com")
            
            while True:
                # 1. Safety Check (Highest Priority)
                self.watchdog.scan_threats()
                
                # 2. Evolution
                self.evolution.load_new_skills()
                self.evolution.trigger_evolution()
                
                # 3. Human-like Idle Behavior
                if random.random() < 0.05:
                    # Random "Looking around"
                    x = random.randint(200, 1000)
                    y = random.randint(200, 600)
                    self.human.move_mouse_human(x, y)
                
                # 4. Anti-AFK Humanized
                if random.random() < 0.02:
                    pyautogui.press('space')
                    time.sleep(random.uniform(0.5, 1.5)) # Dừng lại sau khi nhảy
                
                time.sleep(random.uniform(2.0, 5.0)) # Random loop delay
                
        except SystemExit:
            log_console("🛡️ Safe Exit Completed.")
        except Exception as e:
            log_console(f"🔥 CRASH: {e}")
            requests.post(f"{BRAIN_URL}/self_heal", json={"traceback": traceback.format_exc()})
        finally:
            try: driver.quit()
            except: pass

if __name__ == "__main__":
    if not os.environ.get("DISPLAY"):
        subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1280x720x24", "-ac"])
        os.environ["DISPLAY"] = ":99"
    SentinelAgent().run()
