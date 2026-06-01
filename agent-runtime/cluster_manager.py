import time
from cluster_node import ClusterNode
from vector_memory import remember, recall

CLUSTER_NODES = {}

def register_node(name, url):
    CLUSTER_NODES[name] = ClusterNode(name, url)
    remember(f"cluster_node: {name} {url}")

def discover_nodes():
    nodes = recall("cluster_node")
    for entry in nodes:
        name, url = entry.split(" ")[1:]
        if name not in CLUSTER_NODES:
            CLUSTER_NODES[name] = ClusterNode(name, url)

def get_alive_nodes():
    discover_nodes()
    return [n for n in CLUSTER_NODES.values() if n.is_alive()]

def choose_best_node():
    alive = get_alive_nodes()
    if not alive:
        return None
    return sorted(alive, key=lambda n: n.last_seen)[0]

def run_remote(agent, task):
    node = choose_best_node()
    if not node:
        return None, "No alive nodes"
    result = node.run_agent(agent, task)
    node.last_seen = time.time()
    return result, node.name
