import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def check_session(agent):
    """Kiểm tra trạng thái Cookie trước khi bắt đầu Heartbeat"""
    cookie = os.environ.get("ROBLOX_COOKIE")
    webhook = os.environ.get("DISCORD_WEBHOOK")
    
    if not cookie:
        print("❌ [AUTH] Thiếu ROBLOX_COOKIE trong biến môi trường!")
        return False

    print("🔍 [AUTH] Đang kiểm tra hiệu lực Cookie...")
    
    # Nạp cookie vào driver
    agent.driver.get("https://www.roblox.com")
    agent.driver.add_cookie({
        'name': '.ROBLOSECURITY',
        'value': cookie,
        'domain': '.roblox.com'
    })
    agent.driver.refresh()
    time.sleep(5)
    
    # Kiểm tra xem có còn nút "Log In" không
    current_url = agent.driver.current_url
    agent.take_screenshot("logs/screenshots/session_check.png")
    
    if "home" in current_url or "games" in current_url:
        print("✅ [AUTH] Cookie hợp lệ. Đang tiến hành vào game...")
        return True
    else:
        print("🚨 [AUTH] Cookie đã hết hạn hoặc không hợp lệ!")
        return False

if __name__ == "__main__":
    # Test độc lập nếu cần
    pass
