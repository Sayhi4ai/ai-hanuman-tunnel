from graph import AGENT_REGISTRY
from mesh_network import register_mesh_node, route_task, gossip_state, get_alive_nodes

def mesh_agent(state):
    task = state.get("task", "").strip()

    # Commands:
    #   register <name> <url>
    #   route <agent> | <task>
    #   gossip
    #   status

    if task.startswith("register"):
        _, name, url = task.split(" ", 2)
        register_mesh_node(name, url)
        state["result"] = f"Mesh node '{name}' registered at {url}"
        return state

    if task.startswith("route"):
        _, rest = task.split(" ", 1)
        agent, inner_task = [x.strip() for x in rest.split("|", 1)]
        result, node = route_task(agent, inner_task)
        state["result"] = (
            f"Task routed to mesh node: {node}\n\n"
            f"Output:\n{result}"
        )
        return state

    if task == "gossip":
        local_state = {"agents": list(AGENT_REGISTRY.keys())}
        result = gossip_state(local_state)
        state["result"] = f"Gossip exchange complete.\n\nResponse:\n{result}"
        return state

    if task == "status":
        alive = get_alive_nodes()
        state["result"] = (
            "Mesh network status:\n" +
            "\n".join([f"{name} -> {node['url']}" for name, node in alive])
        )
        return state

    state["result"] = (
        "Usage:\n"
        "- register <name> <url>\n"
        "- route <agent> | <task>\n"
        "- gossip\n"
        "- status"
    )
    return state

def load():
    AGENT_REGISTRY["mesh_agent"] = mesh_agent
    return mesh_agent
