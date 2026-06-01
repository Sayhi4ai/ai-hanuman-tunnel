from graph import AGENT_REGISTRY
from task_queue import fetch_next, mark_done, mark_failed

def queue_worker_agent(state):
    # One iteration: pick next task, run it, update status
    item, _ = fetch_next()
    if not item:
        state["result"] = "No queued tasks."
        state["history"].append("QUEUE_WORKER: idle")
        return state

    agent_name = item["agent"]
    task = item["task"]
    task_id = item["id"]

    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        mark_failed(task_id, f"Agent '{agent_name}' not found")
        state["result"] = f"Agent '{agent_name}' not found for task {task_id}"
        state["history"].append("QUEUE_WORKER: agent not found")
        return state

    try:
        sub_state = {"task": task, "history": [], "result": ""}
        result_state = agent_fn(sub_state)
        mark_done(task_id, result_state["result"])
        state["result"] = f"Task {task_id} completed by {agent_name}."
        state["history"].append("QUEUE_WORKER: task completed")
        state["history"].extend(result_state["history"])
    except Exception as e:
        mark_failed(task_id, e)
        state["result"] = f"Task {task_id} failed: {e}"
        state["history"].append("QUEUE_WORKER: task failed")

    return state

def load():
    from graph import AGENT_REGISTRY
    AGENT_REGISTRY["queue_worker"] = queue_worker_agent
    return queue_worker_agent
