import json
import os
from typing import Dict, Any, List
from app.integrations.opscaptain import opscaptain

KG_FILE = "/home/inteligent-human/ai-bots/openclaw-backend/data/knowledge_graph.json"

class KnowledgeGraph:
    def __init__(self):
        os.makedirs(os.path.dirname(KG_FILE), exist_ok=True)
        if not os.path.exists(KG_FILE):
            with open(KG_FILE, "w") as f:
                json.dump({"nodes": {}, "edges": []}, f)

    def load(self):
        with open(KG_FILE, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(KG_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def add_node(self, node_id: str, properties: Dict[str, Any]):
        data = self.load()
        data["nodes"][node_id] = properties
        self.save(data)
        opscaptain.log_event("kg_node_added", {"node": node_id})

    def add_edge(self, source: str, relation: str, target: str):
        data = self.load()
        data["edges"].append({
            "source": source,
            "relation": relation,
            "target": target
        })
        self.save(data)
        opscaptain.log_event("kg_edge_added", {
            "source": source,
            "relation": relation,
            "target": target
        })

    def get_node(self, node_id: str):
        return self.load()["nodes"].get(node_id)

    def get_edges(self, node_id: str):
        return [
            e for e in self.load()["edges"]
            if e["source"] == node_id or e["target"] == node_id
        ]

    def search(self, text: str):
        data = self.load()
        return {
            "nodes": {
                k: v for k, v in data["nodes"].items()
                if text.lower() in k.lower() or text.lower() in str(v).lower()
            },
            "edges": [
                e for e in data["edges"]
                if text.lower() in e["relation"].lower()
            ]
        }

knowledge_graph = KnowledgeGraph()
