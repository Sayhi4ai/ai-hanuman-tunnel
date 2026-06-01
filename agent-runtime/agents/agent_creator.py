from graph import AGENT_REGISTRY
from agent_factory import create_agent
from vector_memory import remember

def agent_creator(state):
    task = state.get("task", "")

    # Expected format:
    #   create <agent_name> : <description>
    if ":" not in task:
        state["result"] = "Usage: create <agent_name> : <description>"
        return state

    left, description = task.split(":", 1)
    parts = left.strip().split(" ", 1)

    if len(parts) < 2:
        state["result"] = "Usage: create <agent_name> : <description>"
        return state

    _, agent_name = parts
    agent_name = agent_name.strip()

    filename, code = create_agent(agent_name, description.strip())

    state["result"] = (
        f"New agent '{agent_name}' created.\n"
        f"File: {filename}\n\n"
        f"Code:\n{code}"
    )

    state["history"].append("AGENT_CREATOR: created new agent")
    remember(f"agent_creator: {agent_name}")

    return state

def load():
    AGENT_REGISTRY["agent_creator"] = agent_creator
    return agent_creator
