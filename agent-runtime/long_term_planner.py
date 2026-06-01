import time
from task_queue import enqueue
from vector_memory import remember, recall
from messaging import send_message

def generate_milestones(goal):
    # Ask writer to break the goal into steps
    steps = send_message(
        "writer",
        f"Break this long-term goal into 5–8 clear milestones:\n{goal}"
    )
    return steps.split("\n")

def schedule_milestones(goal, milestones):
    scheduled = []
    now = time.time()

    for i, m in enumerate(milestones):
        run_at = now + (i * 86400)  # 1 day apart
        task_id = enqueue(m, "manager_agent", run_at=run_at, priority=5)
        scheduled.append((task_id, m))

    return scheduled

def summarize_progress(goal):
    related = recall(goal)
    summary = send_message(
        "writer",
        f"Summarize this long-term progress:\n{related}"
    )
    return summary

def plan_long_term(goal):
    milestones = generate_milestones(goal)
    scheduled = schedule_milestones(goal, milestones)
    remember(f"longterm {goal}: {milestones}")
    return milestones, scheduled
