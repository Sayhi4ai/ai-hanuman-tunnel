import json
import os
from typing import Dict, Any, List
from app.integrations.opscaptain import opscaptain

MEMORY_FILE = "/home/inteligent-human/ai-bots/openclaw-backend/data/memory.json"

class MemoryStore:
    def __init__(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump({"tasks": [], "facts": {}}, f)

    def load(self) -> Dict[str, Any]:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)

    def save(self, data: Dict[str, Any]):
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def add_task(self, task: Dict[str, Any]):
        data = self.load()
        data["tasks"].append(task)
        self.save(data)
        opscaptain.log_event("memory_task_added", task)

    def add_fact(self, key: str, value: Any):
        data = self.load()
        data["facts"][key] = value
        self.save(data)
        opscaptain.log_event("memory_fact_added", {"key": key, "value": value})

    def get_facts(self) -> Dict[str, Any]:
        return self.load().get("facts", {})

    def get_tasks(self) -> List[Dict[str, Any]]:
        return self.load().get("tasks", [])

memory_store = MemoryStore()
