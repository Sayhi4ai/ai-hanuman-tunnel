import json
import os

MEMORY_FILE = "agent_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def remember(agent, key, value):
    memory = load_memory()
    if agent not in memory:
        memory[agent] = {}
    memory[agent][key] = value
    save_memory(memory)

def recall(agent, key):
    memory = load_memory()
    return memory.get(agent, {}).get(key, None)
