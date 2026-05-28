from graph import AGENT_REGISTRY
from evolution_engine import evolve_agent
from vector_memory import remember

def evolution_agent(state):
    task = state.get("task", "")

    # Expected format: "evolve <agent> <test_input>"
    parts = task.split(" ", 2)
    if len(parts) < 3:
        state["result"] = "Usage: evolve <agent> <test_input>"
        return state

    agent_name = parts[0]
    test_input = parts[2]

    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        state["result"] = f"Agent '{agent_name}' not found."
        return state

    # Load original code
    try:
        import inspect
        original_code = inspect.getsource(agent_fn)
    except Exception as e:
        state["result"] = f"Could not load agent code: {e}"
        return state

    # Run evolution
    new_code, score = evolve_agent(agent_name, original_code, test_input)

    # Save evolved version to memory
    remember(f"evolved {agent_name}: score={score}")

    state["result"] = (
        f"Evolution complete for agent '{agent_name}'.\n"
        f"Best score: {score}\n\n"
        f"New evolved code:\n{new_code}"
    )

    state["history"].append("EVOLUTION_AGENT: evolution complete")
    return state

def load():
    AGENT_REGISTRY["evolution_agent"] = evolution_agent
    return evolution_agent
