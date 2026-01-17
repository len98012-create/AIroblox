
import os, sys, json, datetime, time, traceback, random, ast
from flask import Flask, request, jsonify

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_PATH = os.path.join(BASE_DIR, "../libs")
if LIBS_PATH not in sys.path:
    sys.path.insert(0, LIBS_PATH)

# --- STABLE GEMINI IMPORT ---
import google.generativeai as genai

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_KEY_9")
EXTENSION_SAVE_DIR = os.path.join(BASE_DIR, "../extensions")
os.makedirs(EXTENSION_SAVE_DIR, exist_ok=True)

# --- BRAIN INITIALIZATION ---
model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # Fallback to flash-latest if experimental unavailable
        model = genai.GenerativeModel('gemini-2.0-flash-exp') 
        print("✅ [BRAIN] Neural Link Established (Gemini 2.0)")
    except Exception as e:
        print(f"❌ [BRAIN] API Error: {e}")
else:
    print("⚠️ [BRAIN] Running in Offline Mode (No API Key)")

def clean_python_code(text):
    """Strip Markdown formatting from LLM response"""
    text = text.replace("```python", "").replace("```", "")
    return text.strip()

@app.route('/evolve', methods=['POST'])
def evolve():
    """Generate new behavioral extensions based on heuristics."""
    if not model: return jsonify({"status": "offline"})
    
    strategies = [
        "Detect 'AFK' text on screen and press Space.",
        "If mouse hasn't moved for 1 min, draw a circle.",
        "Check chat for 'admin' and log out immediately.",
        "Move to a random booth in Pls Donate.",
        "Reply 'ty' if screen text contains 'donated'."
    ]
    strategy = random.choice(strategies)
    
    print(f"🧬 [EVOLVE] Synthesizing: {strategy}")
    
    prompt = f"""
    Write a Python extension for a Roblox Bot using PyAutoGUI/Selenium.
    Task: {strategy}
    
    Requirements:
    1. Function name: `def execute(agent):`
    2. Use `agent.human.move_mouse_human(x, y)` for movement.
    3. Use `agent.take_screenshot(path)` for vision.
    4. NO infinite loops. Use `time.sleep(random.uniform(1,3))`.
    
    Return ONLY Python code.
    """
    
    try:
        response = model.generate_content(prompt)
        code = clean_python_code(response.text)
        
        # Validation
        ast.parse(code)
        
        filename = f"skill_auto_{int(time.time())}.py"
        path = os.path.join(EXTENSION_SAVE_DIR, filename)
        with open(path, "w") as f:
            f.write(code)
            
        return jsonify({"status": "evolved", "file": filename})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

@app.route('/self_heal', methods=['POST'])
def self_heal():
    """Analyze traceback and suggest fixes."""
    if not model: return jsonify({"status": "offline"})
    
    data = request.json
    trace = data.get("traceback", "")
    print(f"🚑 [HEAL] Diagnosing Crash...")
    
    try:
        prompt = f"Fix this Python error for a Selenium/PyAutoGUI bot:\n{trace}\nReturn full fixed code."
        response = model.generate_content(prompt)
        return jsonify({"status": "healed", "fix": clean_python_code(response.text)})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
