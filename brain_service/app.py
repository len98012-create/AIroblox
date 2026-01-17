
import os, sys, json, datetime, time, traceback, random, shutil, ast
from flask import Flask, request, jsonify

# --- DYNAMIC LIB LOADING ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_PATH = os.path.join(BASE_DIR, "../libs")
if LIBS_PATH not in sys.path:
    sys.path.insert(0, LIBS_PATH)

import google.generativeai as genai

# --- CONFIGURATION ---
EXTENSION_SAVE_DIR = os.path.join(BASE_DIR, "../extensions")
os.makedirs(EXTENSION_SAVE_DIR, exist_ok=True)

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_KEY_9")

# Initialize Gemini Client
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-exp') # Using flash for high-speed generation
        print("✅ [BRAIN] Architect Online (Gemini Flash - Anti-Ban Mode)")
    except Exception as e:
        print(f"❌ [BRAIN] Connection Failed: {e}")
else:
    print("❌ [BRAIN] No API Key found in environment variables.")

def validate_python_code(code_str):
    try:
        ast.parse(code_str)
        return True, "Valid"
    except SyntaxError as e:
        return False, str(e)

@app.route('/evolve', methods=['POST'])
def evolve():
    print(f"🧬 [EVOLVE] Generating stealth features...")
    
    ideas = [
        "Check chat for 'hello' and reply with human-like typing delay.",
        "Move mouse randomly to simulate checking inventory or stats.",
        "If activity is low, press 'w' for 0.5 seconds to prevent AFK kick.",
        "Detect 'Disconnected' screen color and click Reconnect button.",
        "Press 'slash' key to open chat, wait 2s, then close it (act bored).",
        "Randomly rotate camera 90 degrees to look around."
    ]
    idea = random.choice(ideas)
    
    prompt = f"""
    Role: You are a Python Architect for a Stealth Roblox Bot.
    Goal: Write a NEW Python plugin (extension) for: "{idea}"
    
    CRITICAL SAFETY RULES (ANTI-BAN):
    1. NEVER use infinite loops without `time.sleep()`.
    2. Use `time.sleep(random.uniform(min, max))` for ALL delays.
    3. Use `agent.human.move_mouse_human(x, y)` instead of raw move.
    4. Use `agent.human.type_human(text)` for typing.
    5. Function signature: `def execute(agent):`
    
    Return ONLY raw Python code. Do not use Markdown blocks.
    """

    result = {"status": "failed"}

    try:
        resp = model.generate_content(prompt)
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
    data = request.json
    error_trace = data.get("traceback", "")
    print(f"🚑 [HEAL] Analyzing Error...")

    prompt = f"Analyze this Python traceback and provide a FIXED version of the function:\n{error_trace}\nReturn ONLY Python code."
    
    try:
        resp = model.generate_content(prompt)
        fix_code = resp.text.replace("```python", "").replace("```", "").strip()
        return jsonify({"status": "healed", "patch": fix_code})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
