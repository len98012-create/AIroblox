# -*- coding: utf-8 -*-
import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify

# Khởi tạo Gemini với Key 9 đặc biệt của bạn
genai.configure(api_key=os.getenv("GEMINI_KEY_9"))
model = genai.GenerativeModel('gemini-1.5-pro')

app = Flask(__name__)

# --- BỘ NHỚ TRI THỨC ---
KNOWLEDGE_FILE = "memory/long_term.json"
COMMAND_FILE = "sentinel_agent/actions/command.txt"

class BrainEvolution:
    def __init__(self):
        self.history_context = []

    def scholar_search(self, query):
        """Tính năng: Giả lập học hỏi từ các nguồn AI (Gemini/ChatGPT)"""
        prompt = f"Tra cứu kiến thức nâng cao về: {query}. Trả về đoạn code Python tối ưu cho Roblox Automation."
        response = model.generate_content(prompt)
        return response.text

    def generate_skill(self, task_description):
        """Tính năng: Tự viết file skill_*.py mới cho Agent"""
        skill_id = f"skill_{int(os.popen('date +%s').read())}"
        prompt = f"Viết một module Python có hàm execute(agent) để thực hiện: {task_description}. Chỉ trả về code."
        code = model.generate_content(prompt).text
        
        with open(f"extensions/{skill_id}.py", "w", encoding="utf-8") as f:
            f.write(code.replace("```python", "").replace("```", ""))
        return skill_id

@app.route('/self_heal', methods=['POST'])
def self_heal():
    """Tính năng: Tự sửa lỗi code khi Agent bị Crash"""
    data = request.json
    error_log = data.get("traceback")
    
    prompt = f"Hệ thống Sentinel bị lỗi:\n{error_log}\nHãy viết bản vá lỗi (hotfix) dưới dạng một hàm Python."
    fix_code = model.generate_content(prompt).text
    
    # Lưu vào nhật ký học tập
    with open("logs/healed_reports.log", "a") as f:
        f.write(f"\n[{os.popen('date').read().strip()}] Fixed error.")
        
    return jsonify({"status": "success", "patch": fix_code})

@app.route('/evolve', methods=['POST'])
def evolve():
    """Tính năng: Tự động nâng cấp khi rảnh rỗi"""
    be = BrainEvolution()
    new_skill = be.generate_skill("Tự động nhảy theo nhạc và phản hồi chat cực nhanh")
    return jsonify({"new_skill": new_skill})

if __name__ == "__main__":
    # Đảm bảo các thư mục tồn tại
    os.makedirs("extensions", exist_ok=True)
    os.makedirs("memory", exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
