import os, sys, json, datetime, time, traceback, random, ast
from flask import Flask, request, jsonify

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_PATH = os.path.join(BASE_DIR, "../libs")
if LIBS_PATH not in sys.path:
    sys.path.insert(0, LIBS_PATH)

# --- NEW 2026 SDK IMPORT (FIX FUTUREWARNING) ---
from google import genai

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_KEY_9")
EXTENSION_SAVE_DIR = os.path.join(BASE_DIR, "../extensions")
os.makedirs(EXTENSION_SAVE_DIR, exist_ok=True)

# --- BRAIN INITIALIZATION ---
client = None
if API_KEY:
    try:
        # Sử dụng Client mới của GenAI SDK 2026
        client = genai.Client(api_key=API_KEY)
        print("✅ [BRAIN] Neural Link Established (Gemini 2.0 via GenAI SDK)")
    except Exception as e:
        print(f"❌ [BRAIN] API Error: {e}")
else:
    print("⚠️ [BRAIN] Running in Offline Mode (No API Key)")

def clean_python_code(text):
    """Bóc tách code từ Markdown"""
    return text.replace("```python", "").replace("```", "").strip()

@app.route('/evolve', methods=['POST'])
def evolve():
    if not client: return jsonify({"status": "offline"})
    
    strategies = [
        "Detect 'AFK' text on screen and press Space.",
        "If mouse hasn't moved for 1 min, draw a circle.",
        "Check chat for 'admin' and log out immediately.",
        "Move to a random booth in Pls Donate.",
        "Reply 'ty' if screen text contains 'donated'."
    ]
    strategy = random.choice(strategies)
    print(f"🧬 [EVOLVE] Synthesizing: {strategy}")
    
    prompt = f"Write a Python extension for a Roblox Bot using PyAutoGUI/Selenium.\nTask: {strategy}\nRequirements:\n1. Function: `def execute(agent):` \n2. Move: `agent.human.move_mouse_human(x, y)`\n3. Vision: `agent.take_screenshot(path)`\nReturn ONLY code."
    
    try:
        # Cú pháp GenAI SDK 2026
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=prompt
        )
        code = clean_python_code(response.text)
        ast.parse(code) # Kiểm tra lỗi cú pháp
        
        filename = f"skill_auto_{int(time.time())}.py"
        path = os.path.join(EXTENSION_SAVE_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)
            
        return jsonify({"status": "evolved", "file": filename})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

@app.route('/self_heal', methods=['POST'])
def self_heal():
    if not client: return jsonify({"status": "offline"})
    data = request.json
    trace = data.get("traceback", "")
    print(f"🚑 [HEAL] Diagnosing Crash...")
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Fix this Python error for a Selenium/PyAutoGUI bot:\n{trace}\nReturn full fixed code."
        )
        return jsonify({"status": "healed", "fix": clean_python_code(response.text)})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

if __name__ == "__main__":
    # Đảm bảo Flask chạy trên đúng port mà Sentinel SRE Turbo kỳ vọng
    app.run(host='0.0.0.0', port=5000)
