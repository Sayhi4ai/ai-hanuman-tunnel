from graph import AGENT_REGISTRY
from messaging import send_message

def communicator_agent(state):
    task = state.get("task", "")

    # Expected format: "send <agent> <message>"
    parts = task.split(" ", 2)
    if len(parts) < 3:
        state["result"] = "Usage: send <agent> <message>"
        return state

    agent_name = parts[0]
    message = parts[2]

    reply = send_message(agent_name, message)

    state["result"] = (
        f"Message sent to '{agent_name}'.\n"
        f"Reply:\n{reply}"
    )
    state["history"].append(f"COMMUNICATOR: sent to {agent_name}")
    return state

def load():
    AGENT_REGISTRY["communicator"] = communicator_agent
    return communicator_agent
