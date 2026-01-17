import os, sys, time, random, ast
from flask import Flask, request, jsonify

# --- PATH SETUP (CRITICAL) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIBS_PATH = os.path.normpath(os.path.join(BASE_DIR, "../libs"))
if LIBS_PATH not in sys.path:
    sys.path.insert(0, LIBS_PATH)

# --- SAFE IMPORT ---
try:
    from google import genai
    print("✅ [SYSTEM] GenAI SDK 2026 Loaded Successfully")
except ImportError:
    print("⚠️ [SYSTEM] GenAI SDK not found in libs, attempting fallback...")
    # Nếu vẫn lỗi, bot sẽ chạy chế độ Offline để không làm crash Workflow
    genai = None

app = Flask(__name__)
API_KEY = os.environ.get("GEMINI_KEY_9")

client = genai.Client(api_key=API_KEY) if genai and API_KEY else None

@app.route('/evolve', methods=['POST'])
def evolve():
    if not client: return jsonify({"status": "offline", "reason": "SDK_MISSING"})
    
    # Logic Evolve sử dụng Gemini 2.0 Flash
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Viết code Python sử dụng pyautogui để nhấn phím Space chống AFK."
        )
        # Lưu vào extensions...
        return jsonify({"status": "evolved", "code": response.text})
    except Exception as e:
        return jsonify({"status": "failed", "error": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
