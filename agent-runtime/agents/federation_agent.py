from graph import AGENT_REGISTRY
from federation_manager import register_ecosystem, negotiate_federation, FEDERATED_ECOSYSTEMS
from vector_memory import recall

def federation_agent(state):
    task = state.get("task", "").strip()

    # Commands:
    #   register <name> <url>
    #   negotiate <name>
    #   list ecosystems

    if task.startswith("register"):
        _, name, url = task.split(" ", 2)
        register_ecosystem(name, url)
        state["result"] = f"Ecosystem '{name}' registered at {url}"
        return state

    if task.startswith("negotiate"):
        _, name = task.split(" ", 1)
        url = FEDERATED_ECOSYSTEMS.get(name)
        if not url:
            state["result"] = f"Ecosystem '{name}' not found."
            return state

        local_capabilities = list(AGENT_REGISTRY.keys())
        treaty, remote_caps = negotiate_federation(name, url, local_capabilities)

        state["result"] = (
            f"Federation negotiation with '{name}' complete.\n\n"
            f"Treaty:\n{treaty}\n\n"
            f"Remote capabilities:\n{remote_caps}"
        )
        return state

    if task == "list ecosystems":
        entries = recall("federation_registered")
        state["result"] = "Federated ecosystems:\n" + "\n".join(entries)
        return state

    state["result"] = (
        "Usage:\n"
        "- register <name> <url>\n"
        "- negotiate <name>\n"
        "- list ecosystems"
    )
    return state

def load():
    AGENT_REGISTRY["federation_agent"] = federation_agent
    return federation_agent
