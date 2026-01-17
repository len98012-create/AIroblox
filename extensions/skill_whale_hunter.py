# -*- coding: utf-8 -*-
import random
import time

def execute(agent):
    """
    Skill: Whale Hunter & Dynamic Socializer
    Tích hợp tính năng: Nhận diện Donator lớn và nhảy theo đám đông.
    """
    # 1. Quét văn bản trên màn hình tìm thông tin Donate
    screen_text = agent.vision.read_text()
    
    # 2. Logic Phân loại Donator: Whale / Loyal / First-time
    if "donated" in screen_text:
        # Giả lập việc nhận diện số tiền (Cần regex hoặc logic từ Brain)
        agent.human.type_human("/e cheers") # Ăn mừng
        agent.human.move_mouse_human(640, 360) # Nhìn vào trung tâm
        
    # 3. Logic Dynamic Dance: Nhảy khi thấy người khác nhảy
    if "dance" in screen_text or "lol" in screen_text:
        dance_moves = ["/e dance", "/e dance2", "/e dance3"]
        move = random.choice(dance_moves)
        agent.human.type_human(move)
        
    # 4. Logic Nhận diện Begger (Xin xỏ)
    begger_keywords = ["pls", "give", "free", "robux"]
    if any(kw in screen_text for kw in begger_keywords):
        # Lờ đi bằng cách di chuyển chuột ra chỗ khác
        agent.human.move_mouse_human(random.randint(0, 100), random.randint(0, 100))
