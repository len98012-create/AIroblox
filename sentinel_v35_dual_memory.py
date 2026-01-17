
#!/usr/bin/env python3
"""
Sentinel Infinite Engine v7.6.1 (Ghost Protocol - Robust Vision)
=========================================================
Features:
1. Robust Screenshot: PyAutoGUI + Scrot fallback.
2. Fixed Driver Injection: Skills now have access to self.driver.
3. Human Motor Control: Mouse overshoot, jitter, variable speed.

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
loader.ensure("selenium")

import requests
import psutil
import cv2
import numpy as np
import pytesseract
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

    def _ease_out_quad(self, n):
        return -n * (n - 2)

    def move_mouse_human(self, x, y, speed_factor=1.0):
        start_x, start_y = pyautogui.position()
        target_x = x + random.randint(-3, 3)
        target_y = y + random.randint(-3, 3)

        if random.random() < 0.3:
            overshoot_x = target_x + random.randint(-20, 20)
            overshoot_y = target_y + random.randint(-20, 20)
            self._move_curve(start_x, start_y, overshoot_x, overshoot_y, speed_factor)
            time.sleep(random.uniform(0.05, 0.15))
            start_x, start_y = overshoot_x, overshoot_y

        self._move_curve(start_x, start_y, target_x, target_y, speed_factor)

    def _move_curve(self, x1, y1, x2, y2, speed):
        dist = math.hypot(x2 - x1, y2 - y1)
        duration = (random.uniform(0.2, 0.5) + (dist / 2000)) / speed
        steps = max(1, int(duration * 60))
        cp1_x = x1 + random.randint(-100, 100)
        cp1_y = y1 + random.randint(-100, 100)
        
        for i in range(steps):
            t = i / steps
            t_smooth = self._ease_out_quad(t)
            bx = (1-t_smooth)**3*x1 + 3*(1-t_smooth)**2*t_smooth*cp1_x + t_smooth**3*x2
            by = (1-t_smooth)**3*y1 + 3*(1-t_smooth)**2*t_smooth*cp1_y + t_smooth**3*y2
            bx += random.uniform(-1, 1)
            by += random.uniform(-1, 1)
            pyautogui.moveTo(bx, by)
            time.sleep(duration / steps)

    def type_human(self, text):
        for char in text:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.05, 0.15))
            if char in [' ', ',', '.']:
                time.sleep(random.uniform(0.1, 0.3))
            if random.random() < 0.01:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                pyautogui.typewrite(wrong_char)
                time.sleep(0.1)
                pyautogui.press('backspace')
                time.sleep(0.1)

# --- MODULE: VISION & SAFETY ---
class VisionEngine:
    def __init__(self, agent):
        self.agent = agent

    def capture_screen(self, save_path="/tmp/sentinel_vision.png"):
        self.agent.take_screenshot(save_path)
        return cv2.imread(save_path)
    
    def read_text(self):
        try:
            save_path = "/tmp/ocr_capture.png"
            self.agent.take_screenshot(save_path)
            img = cv2.imread(save_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            return pytesseract.image_to_string(gray).strip().lower()
        except Exception as e: 
            return ""

class AdminWatchdog:
    def __init__(self, agent):
        self.agent = agent
        
    def scan_threats(self):
        text = self.agent.vision.read_text()
        for kw in DANGER_KEYWORDS:
            if kw in text:
                log_console(f"🚨 THREAT DETECTED: '{kw}' found on screen!")
                self.emergency_shutdown()
                
    def emergency_shutdown(self):
        log_console("⚡ ACTIVATING KILL SWITCH...")
        pyautogui.hotkey('alt', 'f4')
        time.sleep(1)
        os.system("pkill chrome")
        sys.exit(0)

# --- EVOLUTION MANAGER ---
class EvolutionManager:
    def __init__(self, agent):
        self.agent = agent
        self.loaded_skills = set()
        self.last_evolve_time = time.time()

    def load_new_skills(self):
        if not os.path.abspath(EXTENSION_DIR) in sys.path:
            sys.path.append(os.path.abspath(EXTENSION_DIR))
        files = glob.glob(os.path.join(EXTENSION_DIR, "skill_*.py"))
        for f in files:
            name = Path(f).stem
            if name not in self.loaded_skills:
                try:
                    if name in sys.modules: 
                        mod = importlib.reload(sys.modules[name])
                    else: 
                        mod = importlib.import_module(name)
                    
                    if hasattr(mod, 'execute'):
                        log_console(f"✨ Learned: {name}")
                        mod.execute(self.agent)
                        self.loaded_skills.add(name)
                except Exception as e:
                    log_console(f"Skill error in {name}: {e}")

    def trigger_evolution(self):
        if time.time() - self.last_evolve_time > 300: 
            threading.Thread(target=self._async_evolve).start()
            self.last_evolve_time = time.time()

    def _async_evolve(self):
        try: requests.post(f"{BRAIN_URL}/evolve", json={}, timeout=20)
        except: pass

# --- MAIN AGENT ---
class SentinelAgent:
    def __init__(self):
        self.human = GhostHumanizer()
        self.vision = VisionEngine(self)
        self.watchdog = AdminWatchdog(self)
        self.evolution = EvolutionManager(self)
        self.pg = pyautogui
        self.driver = None

    def take_screenshot(self, path):
        """Robust screenshot with scrot fallback for Linux environments"""
        try:
            # Try PyAutoGUI/Pillow first
            self.pg.screenshot(path)
        except Exception:
            # Fallback to scrot system command
            try:
                os.system(f"scrot -q 100 {path} > /dev/null 2>&1")
            except Exception as e:
                log_console(f"Screenshot Fail: {e}")

    def run(self):
        opts = Options()
        opts.add_argument("--mute-audio")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--window-size=1280,720")
        
        try:
            log_console("🚀 Sentinel v7.6.1 Ghost Protocol Active.")
            self.driver = webdriver.Chrome(options=opts)
            self.driver.set_window_size(1280, 720)
            self.driver.get("https://www.roblox.com")
            
            while True:
                self.watchdog.scan_threats()
                self.evolution.load_new_skills()
                self.evolution.trigger_evolution()
                
                if random.random() < 0.05:
                    x = random.randint(200, 1000)
                    y = random.randint(200, 600)
                    self.human.move_mouse_human(x, y)
                
                if random.random() < 0.02:
                    pyautogui.press('space')
                    time.sleep(random.uniform(0.5, 1.5))
                
                time.sleep(random.uniform(2.0, 5.0))
                
        except SystemExit:
            log_console("🛡️ Safe Exit Completed.")
        except Exception as e:
            log_console(f"🔥 CRASH: {e}")
            trace = traceback.format_exc()
            try: requests.post(f"{BRAIN_URL}/self_heal", json={"traceback": trace})
            except: pass
        finally:
            if self.driver:
                try: self.driver.quit()
                except: pass

if __name__ == "__main__":
    if not os.environ.get("DISPLAY"):
        subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1280x720x24", "-ac"])
        os.environ["DISPLAY"] = ":99"
    SentinelAgent().run()
