from graph import AGENT_REGISTRY
from registry_healer import heal_registry

def registry_healer_agent(state):
    healed = heal_registry()

    if not healed:
        state["result"] = "All agents are healthy. No healing required."
        state["history"].append("REGISTRY_HEALER: no issues")
        return state

    result = "Registry healing complete.\n\nHealed agents:\n"
    for name, filename, code in healed:
        result += f"- {name} (file: {filename})\n"

    state["result"] = result
    state["history"].append("REGISTRY_HEALER: healed agents")
    return state

def load():
    AGENT_REGISTRY["registry_healer_agent"] = registry_healer_agent
    return registry_healer_agent
