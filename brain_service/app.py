import os, sys, json, time, ast
from flask import Flask, request, jsonify

# --- PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_PATH = os.path.join(BASE_DIR, "../libs")
if LIBS_PATH not in sys.path: sys.path.insert(0, LIBS_PATH)

# --- NEW 2026 GENAI SDK ---
from google import genai

app = Flask(__name__)
# Sử dụng Key 9 từ secrets
client = genai.Client(api_key=os.environ.get("GEMINI_KEY_9"))

@app.route('/evolve', methods=['POST'])
def evolve():
    try:
        # Sử dụng model gemini-2.0-flash chuẩn
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Viết skill Python cho Roblox sử dụng PyAutoGUI để di chuyển chống AFK."
        )
        code = response.text.replace("```python", "").replace("```", "").strip()
        
        filename = f"skill_auto_{int(time.time())}.py"
        path = os.path.join(BASE_DIR, "../extensions", filename)
        with open(path, "w") as f: f.write(code)
            
        return jsonify({"status": "evolved", "file": filename})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
