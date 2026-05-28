from graph import AGENT_REGISTRY
from loop_engine import run_loop
import threading

def loop_agent(state):
    task = state.get("task", "")
    parts = task.split(" ", 2)

    if len(parts) < 3:
        state["result"] = "Usage: loop <agent> <interval_seconds> <task>"
        return state

    agent_name = parts[0]
    interval = int(parts[1])
    loop_task = parts[2]

    t = threading.Thread(target=run_loop, args=(agent_name, loop_task, interval))
    t.daemon = True
    t.start()

    state["result"] = (
        f"Started autonomous loop:\n"
        f"- Agent: {agent_name}\n"
        f"- Interval: {interval}s\n"
        f"- Task: {loop_task}"
    )

    state["history"].append("LOOP: started")
    return state

def load():
    AGENT_REGISTRY["loop"] = loop_agent
    return loop_agent
