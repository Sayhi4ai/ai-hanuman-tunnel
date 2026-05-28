from graph import AGENT_REGISTRY

def supervisor_agent(state):
    task = state.get("task", "")

    # Step 1: Try planner
    planner = AGENT_REGISTRY.get("planner")
    if planner:
        try:
            sub_state = {"task": task, "history": [], "result": ""}
            result = planner(sub_state)
            state["result"] = result["result"]
            state["history"].append("SUPERVISOR: planner succeeded")
            state["history"].extend(result["history"])
            return state
        except Exception as e:
            state["history"].append(f"SUPERVISOR: planner failed ({e})")

    # Step 2: Retry planner once
    if planner:
        try:
            sub_state = {"task": task, "history": [], "result": ""}
            result = planner(sub_state)
            state["result"] = result["result"]
            state["history"].append("SUPERVISOR: planner retry succeeded")
            state["history"].extend(result["history"])
            return state
        except Exception as e:
            state["history"].append(f"SUPERVISOR: planner retry failed ({e})")

    # Step 3: Fallback to writer
    writer = AGENT_REGISTRY.get("writer")
    if writer:
        sub_state = {"task": f"Fallback: {task}", "history": [], "result": ""}
        result = writer(sub_state)
        state["result"] = result["result"]
        state["history"].append("SUPERVISOR: fallback to writer")
        state["history"].extend(result["history"])
        return state

    # Step 4: Total failure
    state["result"] = "All agents failed. Supervisor cannot recover."
    state["history"].append("SUPERVISOR: total failure")
    return state

def load():
    AGENT_REGISTRY["supervisor"] = supervisor_agent
    return supervisor_agent
