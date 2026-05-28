import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    return json.load(open(MEMORY_FILE))

def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w"))

def remember(key, value):
    mem = load_memory()
    mem[key] = value
    save_memory(mem)

def recall(key):
    return load_memory().get(key)
