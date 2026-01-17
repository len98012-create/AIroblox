
import os, sys, json, datetime, time, traceback, random, shutil, ast
from flask import Flask, request, jsonify
from google import genai
from google.genai import types

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSION_SAVE_DIR = os.path.join(BASE_DIR, "../extensions")
os.makedirs(EXTENSION_SAVE_DIR, exist_ok=True)

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_KEY_9")
ai_client = None

if API_KEY:
    try:
        ai_client = genai.Client(api_key=API_KEY)
        print("✅ [BRAIN] Architect Online (Anti-Ban Mode)")
    except: pass

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
        "Move mouse randomly to simulate checking inventory.",
        "If activity is low, press 'w' for 0.5 seconds to act alive.",
        "Detect 'Disconnected' screen and click Reconnect.",
        "Log a random timestamp to simulate user activity.",
        "Press 'slash' key to open chat but don't type anything (act bored)."
    ]
    idea = random.choice(ideas)
    
    # Prompt được tối ưu cho Anti-Ban
    prompt = f"""
    Role: You are a Python Architect for a Stealth Roblox Bot.
    Goal: Write a NEW Python plugin (extension) for: "{idea}"
    
    CRITICAL SAFETY RULES (ANTI-BAN):
    1. NEVER use infinite loops without `time.sleep()`.
    2. Use `time.sleep(random.uniform(min, max))` for ALL delays. Never use fixed integers.
    3. Use `agent.human.move_mouse_human(x, y)` instead of raw move.
    4. Use `agent.human.type_human(text)` for typing.
    5. Function signature: `def execute(agent):`
    
    Return ONLY raw Python code.
    """

    result = {"status": "failed"}

    if ai_client:
        try:
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
                print(f"🚀 [EVOLVED] Stealth Skill: {idea}")
                result = {"status": "success", "file": feature_name}
            else:
                print(f"⚠️ Bad Code: {msg}")
                
        except Exception as e:
            print(f"Evolve Error: {e}")

    return jsonify(result)

@app.route('/self_heal', methods=['POST'])
def self_heal():
    return jsonify({"status": "healed"})

@app.route('/research', methods=['POST'])
def research():
    return jsonify({"status": "skipped"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
