import time
import random
import pyautogui

def execute(agent):
    """Kỹ năng chuyên biệt cho PLS DONATE tích hợp Ghost Humanizer"""
    print("🏪 [SKILL] Thực hiện chu kỳ chiếm quầy Pls Donate...")
    
    # 1. Di chuyển chuột ngẫu nhiên để quan sát (Human-like)
    agent.human.move_mouse_human(random.randint(400, 800), random.randint(300, 500))
    
    # 2. Giả lập đi tới quầy (Nhấn giữ W với delay biến thiên)
    pyautogui.keyDown('w')
    time.sleep(random.uniform(0.8, 2.2)) 
    pyautogui.keyUp('w')
    
    # 3. Tương tác nhấn E để nhận quầy
    # Dùng GhostHumanizer để di chuyển tới vị trí nút E giả định trên màn hình (nếu cần)
    pyautogui.press('e')
    
    # 4. Gõ chat cảm ơn bằng cơ chế Type Human (Anti-Ban)
    messages = [
        "Hi! Goal is 100 Robux for my AI project.",
        "Any donation helps! Have a great day.",
        "Thank you so much for visiting my stand!"
    ]
    
    pyautogui.press('/')
    time.sleep(0.5)
    agent.human.type_human(random.choice(messages))
    pyautogui.press('enter')
    
    print("✅ [SKILL] Chu kỳ hoàn tất. Đang chờ Donate...")
