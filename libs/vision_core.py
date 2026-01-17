import cv2
import numpy as np
import pytesseract
import os
from PIL import Image

class SentinelVision:
    def __init__(self):
        self.screenshot_path = "/tmp/check.jpg"
        self.action_dir = "sentinel_agent/actions"
        os.makedirs(self.action_dir, exist_ok=True)

    def capture_low_res(self):
        """Chụp ảnh chất lượng thấp để tiết kiệm CPU theo quy tắc Turbo"""
        os.system(f"scrot -q 1 {self.screenshot_path}")

    def scan_for_text(self):
        """Dùng OCR để đọc tin nhắn chat hoặc số tiền donate"""
        try:
            img = Image.open(self.screenshot_path)
            text = pytesseract.image_to_string(img)
            return text.lower()
        except:
            return ""

    def detect_whale_color(self):
        """Phát hiện màu sắc đặc biệt của các item hiếm (Dominus/Valk)"""
        img = cv2.imread(self.screenshot_path)
        # Logic nhận diện dải màu vàng (Gold) hoặc xanh (Cyan) của Whales
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_gold = np.array([18, 40, 90])
        upper_gold = np.array([27, 255, 255])
        mask = cv2.inRange(hsv, lower_gold, upper_gold)
        return np.sum(mask) > 500 # Trả về True nếu thấy nhiều màu vàng

    def auto_screenshot_on_donate(self, amount):
        """Tính năng: Chụp ảnh lưu niệm khi nhận donate lớn >= 500 R$"""
        if amount >= 500:
            ts = os.popen("date +%H%M%S").read().strip()
            save_path = f"{self.action_dir}/victory_{ts}.jpg"
            os.system(f"cp {self.screenshot_path} {save_path}")
            return save_path
        return None

# Tích hợp logic học tập: Lưu tọa độ màu sắc mới vào command.txt
