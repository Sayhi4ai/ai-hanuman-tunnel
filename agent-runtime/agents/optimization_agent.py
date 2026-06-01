from graph import AGENT_REGISTRY
from system_optimizer import optimize_system
from task_queue import enqueue

def optimization_agent(state):
    task = state.get("task", "").strip()

    optimizations = optimize_system()

    # Optionally schedule improvements
    enqueue(
        f"Implement these system optimizations:\n{optimizations}",
        "manager_agent",
        priority=10
    )

    state["result"] = (
        "System optimization complete.\n\n"
        "Recommended improvements:\n"
        f"{optimizations}\n\n"
        "A high-priority task has been scheduled for the manager_agent to implement improvements."
    )

    state["history"].append("OPTIMIZATION_AGENT: system optimized")
    return state

def load():
    AGENT_REGISTRY["optimization_agent"] = optimization_agent
    return optimization_agent
