import time
from task_queue import fetch_next, mark_done, mark_failed
from graph import AGENT_REGISTRY

def run_queue_daemon(interval=2):
    print("[QUEUE DAEMON] Started persistent task queue processor")

    while True:
        item, _ = fetch_next()

        if not item:
            time.sleep(interval)
            continue

        agent_name = item["agent"]
        task = item["task"]
        task_id = item["id"]

        agent_fn = AGENT_REGISTRY.get(agent_name)
        if not agent_fn:
            mark_failed(task_id, f"Agent '{agent_name}' not found")
            continue

        try:
            state = {"task": task, "history": [], "result": ""}
            result_state = agent_fn(state)
            mark_done(task_id, result_state["result"])
        except Exception as e:
            mark_failed(task_id, str(e))

        time.sleep(interval)
