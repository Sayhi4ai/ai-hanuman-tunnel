from graph import AGENT_REGISTRY
from messaging import send_message
from vector_memory import remember, recall

def goal_agent(state):
    goal = state.get("task", "")

    # Retrieve related memories
    related = recall(goal)

    # Step 1: Break goal into subtasks
    subtasks = []

    if "research" in goal:
        subtasks.append(("websearcher", goal))
        subtasks.append(("writer", f"Summarize findings about: {goal}"))
        subtasks.append(("writer", f"Write a clean report about: {goal}"))

    elif "monitor" in goal:
        subtasks.append(("browser", goal.replace("monitor", "").strip()))
        subtasks.append(("writer", f"Summarize page changes for: {goal}"))

    else:
        subtasks.append(("writer", f"Describe the goal: {goal}"))

    # Step 2: Execute subtasks
    results = []
    for agent_name, task in subtasks:
        reply = send_message(agent_name, task)
        results.append(f"[{agent_name}] {reply}")

    # Step 3: Store progress in vector memory
    remember(f"Goal progress for '{goal}': {results}")

    # Step 4: Build final output
    result = f"Goal: {goal}\n\n"
    if related:
        result += "Relevant past progress:\n"
        for r in related:
            result += f"- {r}\n"
        result += "\n"

    result += "New progress:\n"
    for r in results:
        result += f"{r}\n"

    state["result"] = result
    state["history"].append("GOAL_AGENT: executed goal plan")
    return state

def load():
    AGENT_REGISTRY["goal_agent"] = goal_agent
    return goal_agent
