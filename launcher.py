# -*- coding: utf-8 -*-
"""
SENTINEL V35 - LAUNCHER CORE
Developed for: GitHub Sentinel Project
Rules: Always create new files & log every action.
"""

import os
import sys
import time
import subprocess
from libs import logger_module

# Khởi tạo thông tin từ bộ nhớ AI đã lưu
ROBLOX_COOKIE = "DISCORD_WEBHOOK_ROBLOX_COOKIE_PLACEHOLDER"
WEBHOOK_URL = "DISCORD_WEBHOOK_PLACEHOLDER"

class SentinelLauncher:
    def __init__(self):
        self.version = "V35.0.1"
        self.start_time = time.time()
        self.check_directories()

    def check_directories(self):
        dirs = [".github/workflows", "accroblox", "brain_service", "libs", "logs", "memory", "sentinel_agent"]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
                print(f"[SYSTEM] Created directory: {d}")

    def boot(self):
        print(f"--- STARTING SENTINEL SYSTEM {self.version} ---")
        # Ghi log khởi động
        with open("SENTINEL_V35_LOGS.txt", "a", encoding="utf-8") as f:
            f.write(f"[{time.ctime()}] System Booted using Launcher.py\n")
        
        # Kích hoạt Dual Memory
        try:
            from sentinel_v35_dual_memory import memory_engine
            memory_engine.sync_long_term()
        except ImportError:
            print("[ERROR] sentinel_v35_dual_memory.py not found!")

if __name__ == "__main__":
    app = SentinelLauncher()
    app.boot()
