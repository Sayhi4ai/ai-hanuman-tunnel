from graph import AGENT_REGISTRY
from task_queue import enqueue, list_tasks

def queue_manager_agent(state):
    task = state.get("task", "")

    # Commands:
    #   enqueue <agent> <task text>
    #   list
    parts = task.split(" ", 2)
    if not parts:
        state["result"] = "Usage: enqueue <agent> <task> | list"
        return state

    cmd = parts[0]

    if cmd == "list":
        tasks = list_tasks()
        out = []
        for t in tasks:
            out.append(f"{t['id']} [{t['status']}] {t['agent']}: {t['task']}")
        state["result"] = "\n".join(out) if out else "No tasks."
        return state

    if cmd == "enqueue" and len(parts) == 3:
        agent_name = parts[1]
        task_text = parts[2]
        task_id = enqueue(task_text, agent_name)
        state["result"] = f"Enqueued task {task_id} for agent '{agent_name}'."
        return state

    state["result"] = "Usage: enqueue <agent> <task> | list"
    return state

def load():
    AGENT_REGISTRY["queue_manager"] = queue_manager_agent
    return queue_manager_agent
