
import os
import time
import requests

def execute(agent):
    """Kích hoạt trạng thái đang chơi game Pls Donate"""
    place_id = "8737899170" 
    
    # Pre-check to avoid spamming the driver
    if hasattr(agent, '_pls_donate_launched'):
        return
    
    print(f"🚀 [LAUNCHER] Đang nạp phiên chơi cho PlaceID: {place_id}")
    
    if agent.driver:
        try:
            agent.driver.get(f"https://www.roblox.com/games/{place_id}")
            time.sleep(10)
            
            screenshot_path = "logs/screenshots/lobby_check.png"
            agent.take_screenshot(screenshot_path)
            
            agent.discord.send(
                title="🏪 PLS DONATE ACTIVE",
                description="Successfully loaded game page and confirmed lobby visuals.",
                color=0x34c759,
                fields=[
                    {"name": "PlaceID", "value": place_id, "inline": True},
                    {"name": "Status", "value": "Waiting for Booth", "inline": True}
                ]
            )
            agent._pls_donate_launched = True
        except Exception as e:
            print(f"Error launching: {e}")
