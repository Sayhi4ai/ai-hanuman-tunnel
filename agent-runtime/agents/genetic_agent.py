from graph import AGENT_REGISTRY
from genetic_engine import evolve_agents

def genetic_agent(state):
    task = state.get("task", "").strip()

    # Expected:
    #   evolve <agentA> <agentB>
    parts = task.split(" ")
    if len(parts) != 3 or parts[0] != "evolve":
        state["result"] = "Usage: evolve <agentA> <agentB>"
        return state

    _, a, b = parts

    agent_fn_a = AGENT_REGISTRY.get(a)
    agent_fn_b = AGENT_REGISTRY.get(b)

    if not agent_fn_a or not agent_fn_b:
        state["result"] = "One or both parent agents not found."
        return state

    best, scores = evolve_agents(a, b, agent_fn_a, agent_fn_b)

    state["result"] = (
        f"Genetic evolution complete.\n\n"
        f"Parents: {a}, {b}\n"
        f"Best offspring: {best}\n\n"
        f"Fitness scores:\n{scores}"
    )

    state["history"].append("GENETIC_AGENT: evolution cycle complete")
    return state

def load():
    AGENT_REGISTRY["genetic_agent"] = genetic_agent
    return genetic_agent
