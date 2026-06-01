import time
from vector_memory import recall, remember
from messaging import send_message
from task_queue import list_tasks
from graph import AGENT_REGISTRY

def analyze_agent_usage():
    usage = recall("agent_usage")
    summary = send_message(
        "writer",
        f"Summarize patterns in agent usage and identify inefficiencies:\n{usage}"
    )
    return summary

def analyze_queue_health():
    tasks = list_tasks()
    summary = send_message(
        "writer",
        f"Analyze this task queue for bottlenecks, delays, and failures:\n{tasks}"
    )
    return summary

def analyze_memory_health():
    memories = recall("memory")
    summary = send_message(
        "writer",
        f"Analyze memory growth and identify redundant or low-value entries:\n{memories}"
    )
    return summary

def propose_system_optimizations():
    prompt = (
        "Given the following system diagnostics, propose improvements to the architecture, "
        "agent design, memory usage, and scheduling:\n\n"
        f"Agent Usage:\n{analyze_agent_usage()}\n\n"
        f"Queue Health:\n{analyze_queue_health()}\n\n"
        f"Memory Health:\n{analyze_memory_health()}\n"
    )
    return send_message("writer", prompt)

def optimize_system():
    optimizations = propose_system_optimizations()
    remember(f"system_optimization: {optimizations}")
    return optimizations
