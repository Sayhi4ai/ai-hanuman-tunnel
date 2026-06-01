import time
from graph import AGENT_REGISTRY
from load_balancer import choose_best_agent, record_agent_usage, spawn_specialist

def load_balancer_agent(state):
    task = state.get("task", "").strip()

    best_agent, loads = choose_best_agent(task)

    # If load is too high, spawn a specialist
    if loads[best_agent] > 2.0:
        specialist, filename, code = spawn_specialist(task)
        best_agent = specialist
        state["history"].append(f"LOAD_BALANCER: spawned specialist {specialist}")

    agent_fn = AGENT_REGISTRY.get(best_agent)
    if not agent_fn:
        state["result"] = f"Agent '{best_agent}' not found."
        return state

    start = time.time()
    sub_state = {"task": task, "history": [], "result": ""}
    result_state = agent_fn(sub_state)
    duration = time.time() - start

    record_agent_usage(best_agent, duration)

    state["result"] = (
        f"Task routed to: {best_agent}\n"
        f"Execution time: {duration:.2f}s\n\n"
        f"Output:\n{result_state['result']}"
    )

    state["history"].append("LOAD_BALANCER: task routed")
    return state

def load():
    AGENT_REGISTRY["load_balancer_agent"] = load_balancer_agent
    return load_balancer_agent
