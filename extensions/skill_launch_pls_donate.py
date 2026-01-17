import os
import time
import requests

def execute(agent):
    """Kích hoạt trạng thái đang chơi game Pls Donate"""
    place_id = "8737899170" # Pls Donate ID
    cookie = os.getenv("ROBLOX_COOKIE")
    
    print(f"🚀 [LAUNCHER] Đang nạp phiên chơi cho PlaceID: {place_id}")
    
    # Sử dụng Selenium (đã có trong Engine v7.5) để vào trang game
    agent.driver.get(f"https://www.roblox.com/games/{place_id}")
    time.sleep(5)
    
    # Chụp ảnh màn hình để xác nhận đã vào sảnh
    screenshot_path = "logs/screenshots/lobby_check.png"
    agent.pg.screenshot(screenshot_path)
    print(f"📸 [VISION] Đã lưu ảnh sảnh chờ tại {screenshot_path}")

    # Gửi tín hiệu về Brain (Key 9) để xác nhận Online
    requests.post(f"{agent.evolution.agent.brain_url}/evolve", json={
        "status": "In_Game_Lobby",
        "game": "Pls Donate"
    })
