import json
import os
import time
import uuid

QUEUE_FILE = "task_queue.json"

def _load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, "r") as f:
        return json.load(f)

def _save_queue(queue):
    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)

def enqueue(task, agent, run_at=None, priority=0):
    queue = _load_queue()
    item = {
        "id": str(uuid.uuid4()),
        "task": task,
        "agent": agent,
        "priority": priority,
        "run_at": run_at or time.time(),
        "status": "queued",
        "created_at": time.time(),
        "last_error": None,
        "attempts": 0,
    }
    queue.append(item)
    _save_queue(queue)
    return item["id"]

def fetch_next():
    queue = _load_queue()
    now = time.time()
    ready = [q for q in queue if q["status"] == "queued" and q["run_at"] <= now]
    if not ready:
        return None, queue

    ready.sort(key=lambda x: (-x["priority"], x["created_at"]))
    item = ready[0]
    item["status"] = "running"
    _save_queue(queue)
    return item, queue

def mark_done(task_id, result=None):
    queue = _load_queue()
    for q in queue:
        if q["id"] == task_id:
            q["status"] = "done"
            q["result"] = result
            q["completed_at"] = time.time()
            break
    _save_queue(queue)

def mark_failed(task_id, error):
    queue = _load_queue()
    for q in queue:
        if q["id"] == task_id:
            q["status"] = "failed"
            q["last_error"] = str(error)
            q["attempts"] += 1
            break
    _save_queue(queue)

def list_tasks(status=None):
    queue = _load_queue()
    if status:
        return [q for q in queue if q["status"] == status]
    return queue
