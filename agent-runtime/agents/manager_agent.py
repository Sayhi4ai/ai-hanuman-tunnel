from graph import AGENT_REGISTRY
from messaging import send_message
from vector_memory import remember, recall

def manager_agent(state):
    goal = state.get("task", "")

    # Retrieve similar past team structures
    related = recall(f"team {goal}")

    # Step 1: Break goal into sub-goals
    subtasks = []

    if "research" in goal:
        subtasks = [
            ("websearcher", f"Search: {goal}"),
            ("writer", f"Summarize findings about: {goal}"),
            ("writer", f"Rewrite clearly: {goal}")
        ]

    elif "analyze" in goal:
        subtasks = [
            ("filereader", f"Read file {goal.replace('analyze', '').strip()}"),
            ("writer", f"Summarize analysis for: {goal}"),
            ("coder", f"Generate Python analysis code for: {goal}")
        ]

    elif "monitor" in goal:
        subtasks = [
            ("browser", f"Visit {goal.replace('monitor', '').strip()}"),
            ("writer", f"Summarize page changes for: {goal}")
        ]

    else:
        subtasks = [
            ("writer", f"Describe the goal: {goal}")
        ]

    # Step 2: Execute subtasks and collect results
    results = []
    for agent_name, task in subtasks:
        reply = send_message(agent_name, task)
        results.append(f"[{agent_name}] {reply}")

    # Step 3: Store team structure in vector memory
    remember(f"team {goal}: {subtasks}")

    # Step 4: Build final output
    result = f"Manager Team Execution for Goal: {goal}\n\n"

    if related:
        result += "Relevant past team structures:\n"
        for r in related:
            result += f"- {r}\n"
        result += "\n"

    result += "Team Results:\n"
    for r in results:
        result += f"{r}\n"

    state["result"] = result
    state["history"].append("MANAGER_AGENT: executed team plan")
    return state

def load():
    AGENT_REGISTRY["manager_agent"] = manager_agent
    return manager_agent
