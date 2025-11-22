import json
import os
from datetime import datetime

DATA_FILE = os.path.join("data", "memory.json")

class MemoryManager:
    def __init__(self):
        self._ensure_data_file()

    def _ensure_data_file(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({"history": [], "schedules": []}, f)

    def _load(self):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {"history": [], "schedules": []}

    def _save(self, data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def add_history(self, entry):
        data = self._load()
        entry["timestamp"] = datetime.now().isoformat()
        data["history"].insert(0, entry)
        # Keep last 50
        data["history"] = data["history"][:50]
        self._save(data)

    def get_history(self):
        return self._load()["history"]

    def add_schedule(self, job):
        data = self._load()
        job["created_at"] = datetime.now().isoformat()
        data["schedules"].append(job)
        self._save(data)

    def get_schedules(self):
        return self._load()["schedules"]
    
    def delete_schedule(self, index):
        data = self._load()
        if 0 <= index < len(data["schedules"]):
            del data["schedules"][index]
            self._save(data)
