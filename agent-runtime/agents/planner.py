from graph import AGENT_REGISTRY

def planner_agent(state):
    task = state.get("task", "").lower()

    # Decide which agent to call
    if "search" in task or "find" in task or "look up" in task:
        chosen = "websearcher"
    elif "write" in task or "greeting" in task or "poem" in task:
        chosen = "writer"
    elif "code" in task or "python" in task or "calculate" in task:
        chosen = "coder"
    else:
        state["result"] = (
            "I need more details. What exactly do you want me to do?"
        )
        return state

    # Call the chosen agent directly
    agent_fn = AGENT_REGISTRY.get(chosen)

    if not agent_fn:
        state["result"] = f"Agent '{chosen}' not found."
        return state

    # Create sub-state
    sub_state = {
        "task": task,
        "history": [],
        "result": ""
    }

    # Run the chosen agent
    result_state = agent_fn(sub_state)

    # Merge results
    state["result"] = result_state["result"]
    state["history"].append(f"PLANNER: delegated to {chosen}")
    state["history"].extend(result_state["history"])

    return state

def load():
    AGENT_REGISTRY["planner"] = planner_agent
    return planner_agent
