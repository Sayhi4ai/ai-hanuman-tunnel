import random
from vector_memory import recall, remember
from task_queue import list_tasks, mark_failed
from graph import AGENT_REGISTRY
from messaging import send_message

def random_agent_failure():
    agent = random.choice(list(AGENT_REGISTRY.keys()))
    remember(f"chaos: killed_agent {agent}")
    return agent

def random_queue_corruption():
    tasks = list_tasks()
    if not tasks:
        return None
    task = random.choice(tasks)
    mark_failed(task["id"], "Chaos-induced failure")
    remember(f"chaos: corrupted_task {task['id']}")
    return task["id"]

def random_memory_corruption():
    memories = recall("memory")
    if not memories:
        return None
    corrupted = random.choice(memories)
    remember(f"chaos: corrupted_memory {corrupted}")
    return corrupted

def random_node_outage():
    return send_message(
        "writer",
        "Simulate a distributed node outage scenario and describe expected failures."
    )

def generate_chaos_scenario():
    return send_message(
        "writer",
        "Generate a realistic chaos testing scenario for a distributed multi-agent system."
    )

def run_chaos_test():
    actions = [
        ("agent_failure", random_agent_failure),
        ("queue_corruption", random_queue_corruption),
        ("memory_corruption", random_memory_corruption),
        ("node_outage", random_node_outage),
        ("scenario", generate_chaos_scenario),
    ]

    name, fn = random.choice(actions)
    result = fn()

    remember(f"chaos_event: {name} -> {result}")

    return name, result
