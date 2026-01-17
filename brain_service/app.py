import os, sys, json, datetime, time, traceback, random, shutil, ast
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

# --- CẤU HÌNH HỆ THỐNG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSION_SAVE_DIR = os.path.join(BASE_DIR, "../sentinel_agent/extensions") # Sửa đường dẫn cho đúng cấu trúc
os.makedirs(EXTENSION_SAVE_DIR, exist_ok=True)

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_KEY_9")
ai_client = None

# Khởi tạo Client thế hệ mới
if API_KEY:
    try:
        ai_client = genai.Client(api_key=API_KEY)
        print("✅ [BRAIN] Architect Online (Gemini 2.0 Flash - Anti-Ban Mode)")
    except Exception as e:
        print(f"❌ [BRAIN] Connection Failed: {e}")

def validate_python_code(code_str):
    try:
        ast.parse(code_str)
        return True, "Valid"
    except SyntaxError as e:
        return False, str(e)

@app.route('/evolve', methods=['POST'])
def evolve():
    print(f"🧬 [EVOLVE] Generating stealth features...")
    
    # Danh sách ý tưởng hành vi giống người (Anti-Ban)
    ideas = [
        "Check chat for 'hello' and reply with human-like typing delay.",
        "Move mouse randomly to simulate checking inventory or stats.",
        "If activity is low, press 'w' for 0.5 seconds to prevent AFK kick.",
        "Detect 'Disconnected' screen color and click Reconnect button.",
        "Log a random timestamp to a local file to simulate user activity logs.",
        "Press 'slash' key to open chat, wait 2s, then close it (act bored).",
        "Randomly rotate camera 90 degrees to look around."
    ]
    idea = random.choice(ideas)
    
    prompt = f"""
    Role: You are a Python Architect for a Stealth Roblox Bot.
    Goal: Write a NEW Python plugin (extension) for: "{idea}"
    
    CRITICAL SAFETY RULES (ANTI-BAN):
    1. NEVER use infinite loops without `time.sleep()`.
    2. Use `time.sleep(random.uniform(min, max))` for ALL delays. Never use fixed integers.
    3. Use `agent.human.move_mouse_human(x, y)` instead of raw move.
    4. Use `agent.human.type_human(text)` for typing.
    5. Function signature: `def execute(agent):`
    
    Return ONLY raw Python code. Do not use Markdown blocks.
    """

    result = {"status": "failed"}

    if ai_client:
        try:
            # Sử dụng Model mới nhất Gemini 2.0 Flash
            resp = ai_client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            raw_code = resp.text.replace("```python", "").replace("```", "").strip()
            
            is_valid, msg = validate_python_code(raw_code)
            if is_valid:
                feature_name = f"skill_stealth_{int(time.time())}_{random.randint(100,999)}.py"
                filepath = os.path.join(EXTENSION_SAVE_DIR, feature_name)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(raw_code)
                print(f"🚀 [EVOLVED] Stealth Skill Created: {feature_name}")
                result = {"status": "success", "file": feature_name}
            else:
                print(f"⚠️ Bad Code Generated: {msg}")
                
        except Exception as e:
            print(f"Evolve Error: {e}")

    return jsonify(result)

@app.route('/self_heal', methods=['POST'])
def self_heal():
    """Tính năng: Nhận log lỗi và trả về code sửa lỗi"""
    data = request.json
    error_trace = data.get("traceback", "")
    print(f"🚑 [HEAL] Analyzing Error: {error_trace[:100]}...")

    if not ai_client: return jsonify({"status": "no_brain"})

    prompt = f"""
    Analyze this Python traceback from a Roblox Bot:
    {error_trace}
    
    Provide a FIXED version of the function or logic that caused this.
    Return ONLY the Python code fix.
    """
    
    try:
        resp = ai_client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        fix_code = resp.text.replace("```python", "").replace("```", "").strip()
        # Lưu bản vá vào thư mục logs để Human review hoặc tự động apply (tuỳ cấu hình)
        with open("logs/last_fix.py", "w") as f: f.write(fix_code)
        return jsonify({"status": "healed", "patch": fix_code})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

@app.route('/research', methods=['POST'])
def research():
    """Tính năng: Tra cứu kiến thức Roblox (giá item, cách chơi game mới)"""
    data = request.json
    query = data.get("query", "")
    print(f"📚 [RESEARCH] Searching: {query}")

    if not ai_client: return jsonify({"status": "no_brain"})

    try:
        resp = ai_client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=f"You are a Roblox Expert. Answer briefly about: {query}"
        )
        return jsonify({"status": "success", "answer": resp.text})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
