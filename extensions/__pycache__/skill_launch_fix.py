def execute(agent):
    correct_place_id = "8737602449" 
    if hasattr(agent, '_pls_donate_launched'): return
    
    print(f"🚀 [LAUNCHER] Đang sửa lỗi và nạp lại PlaceID: {correct_place_id}")
    if agent.driver:
        try:
            agent.driver.get(f"https://www.roblox.com/games/{correct_place_id}")
            time.sleep(5)
            agent.take_screenshot("logs/screenshots/correct_lobby_check.png")
            agent._pls_donate_launched = True
        except Exception as e:
            print(f"❌ Error: {e}")
