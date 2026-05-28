from graph import AGENT_REGISTRY

def send_message(agent_name, message):
    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        return f"Agent '{agent_name}' not found."

    state = {"task": message, "history": [], "result": ""}
    result_state = agent_fn(state)
    return result_state["result"]
