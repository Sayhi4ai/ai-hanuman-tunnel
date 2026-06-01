from graph import AGENT_REGISTRY
from long_term_planner import plan_long_term, summarize_progress
from vector_memory import recall

def long_term_agent(state):
    goal = state.get("task", "")

    if goal.startswith("progress"):
        topic = goal.replace("progress", "").strip()
        summary = summarize_progress(topic)
        state["result"] = f"Progress summary for '{topic}':\n\n{summary}"
        return state

    milestones, scheduled = plan_long_term(goal)

    result = f"Long-term plan created for: {goal}\n\nMilestones:\n"
    for m in milestones:
        result += f"- {m}\n"

    result += "\nScheduled tasks:\n"
    for tid, m in scheduled:
        result += f"- {tid}: {m}\n"

    state["result"] = result
    state["history"].append("LONG_TERM_AGENT: plan created")
    return state

def load():
    AGENT_REGISTRY["long_term_agent"] = long_term_agent
    return long_term_agent
