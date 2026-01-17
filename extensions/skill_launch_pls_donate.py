def execute(agent):
    # ID CHÍNH XÁC CỦA PLS DONATE
    correct_place_id = "8737602449" 
    
    if hasattr(agent, '_pls_donate_launched'):
        return
    
    print(f"🚀 [LAUNCHER] Đang sửa lỗi và nạp lại PlaceID: {correct_place_id}")
    
    if agent.driver:
        try:
            # Điều hướng đến đúng game
            agent.driver.get(f"https://www.roblox.com/games/{correct_place_id}")
            time.sleep(5)
            
            # Kiểm tra đăng nhập trước khi nhấn Play
            agent.take_screenshot("logs/screenshots/correct_lobby_check.png")
            
            # Logic nhấn nút Play (nếu đã đăng nhập)
            # agent.driver.find_element(...).click()
            
            agent._pls_donate_launched = True
        except Exception as e:
            print(f"❌ Error launching: {e}")
