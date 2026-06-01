import inspect
from messaging import send_message
from agent_factory import create_agent
from vector_memory import remember

def analyze_agent(agent_name, agent_fn):
    code = inspect.getsource(agent_fn)

    critique = send_message(
        "writer",
        f"Critique this agent's design. Identify weaknesses, inefficiencies, missing features, and architectural flaws:\n\n{code}"
    )

    improvements = send_message(
        "writer",
        f"Based on this critique, propose architectural improvements and new agent modules that should be created:\n\n{critique}"
    )

    return code, critique, improvements

def evolve_architecture(agent_name, agent_fn):
    code, critique, improvements = analyze_agent(agent_name, agent_fn)

    new_agent_name = f"{agent_name}_v2"

    filename, new_code = create_agent(
        new_agent_name,
        f"Create an improved version of {agent_name}. Improvements:\n{improvements}"
    )

    remember(f"architecture_evolution {agent_name}: {new_agent_name}")

    return {
        "old_agent": agent_name,
        "new_agent": new_agent_name,
        "critique": critique,
        "improvements": improvements,
        "file": filename,
        "code": new_code
    }
