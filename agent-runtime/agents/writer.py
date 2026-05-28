from graph import AGENT_REGISTRY
from vector_memory import remember, recall

def writer_agent(state):
    task = state.get("task", "")

    # Retrieve similar memories
    related = recall(task)

    result = f"I wrote this for you:\n\n{task}"

    if related:
        result += "\n\nRelevant memories:\n"
        for r in related:
            result += f"- {r}\n"

    # Save new memory
    remember(task)

    state["result"] = result
    state["history"].append(f"WRITER: {result}")
    return state

def load():
    AGENT_REGISTRY["writer"] = writer_agent
    return writer_agent
