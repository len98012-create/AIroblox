
import os
import time
import requests

def execute(agent):
    """Kích hoạt trạng thái đang chơi game Pls Donate"""
    place_id = "8737899170" # Pls Donate ID
    
    print(f"🚀 [LAUNCHER] Đang nạp phiên chơi cho PlaceID: {place_id}")
    
    # Sử dụng Selenium để vào trang game
    if agent.driver:
        agent.driver.get(f"https://www.roblox.com/games/{place_id}")
        time.sleep(5)
        
        # Chụp ảnh màn hình để xác nhận đã vào sảnh (Dùng method robust của agent)
        os.makedirs("logs/screenshots", exist_ok=True)
        screenshot_path = "logs/screenshots/lobby_check.png"
        agent.take_screenshot(screenshot_path)
        print(f"📸 [VISION] Đã lưu ảnh sảnh chờ tại {screenshot_path}")

        # Gửi tín hiệu về Brain để xác nhận Online
        try:
            requests.post(f"{agent.evolution.agent.brain_url}/evolve", json={
                "status": "In_Game_Lobby",
                "game": "Pls Donate"
            }, timeout=5)
        except:
            pass
