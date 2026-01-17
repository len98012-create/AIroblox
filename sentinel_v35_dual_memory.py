import json
import os
import datetime

class DualMemorySystem:
    def __init__(self):
        self.long_term_file = "long_term.json"
        self.memory_cache = {}
        self.learning_form_template = {
            "update_date": "",
            "action_completed": "",
            "new_learned_data": "",
            "ai_status": "Active"
        }

    def sync_long_term(self):
        if not os.path.exists(self.long_term_file):
            with open(self.long_term_file, "w") as f:
                json.dump({"history": [], "knowledge_base": {}}, f)
        print("[MEMORY] Long-term memory synchronized.")

    def save_special_key_9(self, input_data):
        """
        Special Key 9: Teach AI and automatically save.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "id": len(self.memory_cache) + 1,
            "timestamp": timestamp,
            "data": input_data,
            "type": "USER_DIRECT_TEACHING"
        }
        
        # Cập nhật Learning Form
        form = self.learning_form_template.copy()
        form["update_date"] = timestamp
        form["action_completed"] = "KEY_9_LEARNING"
        form["new_learned_data"] = input_data
        
        # Ghi file (Action: Create/Update File)
        with open(f"memory/learn_{timestamp.replace(':', '-')}.json", "w") as f:
            json.dump(form, f, indent=4)
        
        return "Knowledge saved to Memory folder."

memory_engine = DualMemorySystem()
