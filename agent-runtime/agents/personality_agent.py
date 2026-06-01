from graph import AGENT_REGISTRY
from messaging import send_message
from personalities import PERSONALITIES
from vector_memory import remember

def personality_agent(state):
    task = state.get("task", "")

    # Expected format:
    #   <personality> | <agent> | <task>
    parts = task.split("|", 2)
    if len(parts) < 3:
        state["result"] = "Usage: <personality> | <agent> | <task>"
        return state

    personality_name = parts[0].strip()
    agent_name = parts[1].strip()
    inner_task = parts[2].strip()

    personality = PERSONALITIES.get(personality_name)
    if not personality:
        state["result"] = f"Unknown personality '{personality_name}'."
        return state

    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        state["result"] = f"Agent '{agent_name}' not found."
        return state

    # Apply personality prompt
    modified_task = (
        f"{personality['prompt']}\n\n"
        f"Task:\n{inner_task}"
    )

    # Run the inner agent
    sub_state = {"task": modified_task, "history": [], "result": ""}
    result_state = agent_fn(sub_state)

    # Store personality usage
    remember(f"personality {personality_name}: {inner_task}")

    state["result"] = (
        f"Personality: {personality_name} ({personality['style']})\n"
        f"Agent: {agent_name}\n\n"
        f"Output:\n{result_state['result']}"
    )
    state["history"].append("PERSONALITY_AGENT: applied personality")
    return state

def load():
    AGENT_REGISTRY["personality_agent"] = personality_agent
    return personality_agent
