from graph import AGENT_REGISTRY

def run_workflow(steps, initial_input=""):
    state = {"task": initial_input, "history": [], "result": ""}

    for step in steps:
        agent_name = step["agent"]
        task_template = step["task"]

        agent_fn = AGENT_REGISTRY.get(agent_name)
        if not agent_fn:
            state["history"].append(f"WORKFLOW: Agent '{agent_name}' not found")
            continue

        # Fill in the task with previous result
        task = task_template.replace("{input}", state["result"])

        sub_state = {"task": task, "history": [], "result": ""}
        result_state = agent_fn(sub_state)

        state["result"] = result_state["result"]
        state["history"].append(f"WORKFLOW: ran {agent_name}")
        state["history"].extend(result_state["history"])

    return state
