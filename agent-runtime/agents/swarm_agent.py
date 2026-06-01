from graph import AGENT_REGISTRY
from swarm_manager import create_swarm, dissolve_swarm

def swarm_agent(state):
    task = state.get("task", "").strip()

    # Expected:
    #   create <parent> | <role1,role2,...>
    #   dissolve <parent>
    if task.startswith("create"):
        _, rest = task.split(" ", 1)
        parent, roles = [x.strip() for x in rest.split("|", 1)]
        role_list = [r.strip() for r in roles.split(",")]
        swarm = create_swarm(parent, role_list)

        state["result"] = (
            f"Swarm created for parent '{parent}'.\n"
            f"Agents: {swarm}"
        )
        state["history"].append("SWARM_AGENT: swarm created")
        return state

    if task.startswith("dissolve"):
        _, parent = task.split(" ", 1)
        dissolved = dissolve_swarm(parent.strip())

        state["result"] = (
            f"Swarms dissolved for parent '{parent}'.\n"
            f"Entries: {dissolved}"
        )
        state["history"].append("SWARM_AGENT: swarm dissolved")
        return state

    state["result"] = (
        "Usage:\n"
        "- create <parent> | <role1,role2,...>\n"
        "- dissolve <parent>"
    )
    return state

def load():
    AGENT_REGISTRY["swarm_agent"] = swarm_agent
    return swarm_agent
