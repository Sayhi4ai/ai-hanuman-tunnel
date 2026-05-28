import json
import os
from sentence_transformers import SentenceTransformer, util

MEMORY_FILE = "vector_memory.json"
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memories):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memories, f, indent=2)

def remember(text):
    memories = load_memory()
    embedding = model.encode(text).tolist()
    memories.append({"text": text, "embedding": embedding})
    save_memory(memories)

def recall(query, top_k=3):
    memories = load_memory()
    if not memories:
        return []

    query_emb = model.encode(query)

    scored = []
    for m in memories:
        score = util.cos_sim(query_emb, m["embedding"])[0][0].item()
        scored.append((score, m["text"]))

    scored.sort(reverse=True)
    return [t for _, t in scored[:top_k]]
