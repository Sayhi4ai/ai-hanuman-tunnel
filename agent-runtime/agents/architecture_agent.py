from graph import AGENT_REGISTRY
from architecture_evolver import evolve_architecture

def architecture_agent(state):
    task = state.get("task", "").strip()

    if not task:
        state["result"] = "Usage: evolve <agent_name>"
        return state

    agent_name = task.replace("evolve", "").strip()

    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        state["result"] = f"Agent '{agent_name}' not found."
        return state

    result = evolve_architecture(agent_name, agent_fn)

    state["result"] = (
        f"Architecture evolution complete.\n\n"
        f"Old agent: {result['old_agent']}\n"
        f"New agent: {result['new_agent']}\n\n"
        f"Critique:\n{result['critique']}\n\n"
        f"Improvements:\n{result['improvements']}\n\n"
        f"New agent code saved to: {result['file']}\n\n"
        f"Generated Code:\n{result['code']}"
    )

    state["history"].append("ARCHITECTURE_AGENT: evolved agent")
    return state

def load():
    AGENT_REGISTRY["architecture_agent"] = architecture_agent
    return architecture_agent
