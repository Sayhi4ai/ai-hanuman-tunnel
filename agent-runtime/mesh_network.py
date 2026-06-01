import requests
import random
import time
from vector_memory import remember, recall

MESH_NODES = {}

def register_mesh_node(name, url):
    MESH_NODES[name] = {"url": url, "last_seen": time.time()}
    remember(f"mesh_node: {name} {url}")

def discover_mesh_nodes():
    entries = recall("mesh_node")
    for e in entries:
        _, name, url = e.split(" ")
        if name not in MESH_NODES:
            MESH_NODES[name] = {"url": url, "last_seen": 0}

def ping_node(url):
    try:
        r = requests.get(f"{url}/mesh/ping")
        return r.status_code == 200
    except:
        return False

def get_alive_nodes():
    discover_mesh_nodes()
    alive = []
    for name, node in MESH_NODES.items():
        if ping_node(node["url"]):
            node["last_seen"] = time.time()
            alive.append((name, node))
    return alive

def gossip_state(local_state):
    alive = get_alive_nodes()
    if not alive:
        return None

    name, node = random.choice(alive)
    try:
        r = requests.post(f"{node['url']}/mesh/gossip", json=local_state)
        return r.json()
    except:
        return None

def route_task(agent, task):
    alive = get_alive_nodes()
    if not alive:
        return None, "No mesh nodes available"

    # Choose lowest-latency node (approx by last_seen)
    name, node = sorted(alive, key=lambda x: x[1]["last_seen"])[0]

    try:
        payload = {"agent": agent, "task": task}
        r = requests.post(f"{node['url']}/run-agent", json=payload)
        return r.json(), name
    except:
        return None, "Routing failed"
