import traceback
from graph import AGENT_REGISTRY
from messaging import send_message
from vector_memory import remember

def debugger_agent(state):
    task = state.get("task", "")

    # Expected format: "debug <agent> <input>"
    parts = task.split(" ", 2)
    if len(parts) < 3:
        state["result"] = "Usage: debug <agent> <task>"
        return state

    agent_name = parts[0]
    test_input = parts[2]

    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        state["result"] = f"Agent '{agent_name}' not found."
        return state

    # Step 1: Try running the agent
    try:
        test_state = {"task": test_input, "history": [], "result": ""}
        result_state = agent_fn(test_state)

        state["result"] = (
            f"No errors detected.\n"
            f"Agent '{agent_name}' executed successfully.\n\n"
            f"Output:\n{result_state['result']}"
        )
        return state

    except Exception as e:
        error_text = traceback.format_exc()
        state["history"].append("DEBUGGER: error detected")

    # Step 2: Ask writer to propose a fix
    fix_suggestion = send_message(
        "writer",
        f"Fix this Python error:\n\n{error_text}\n\n"
        f"Original agent code likely needs repair."
    )

    # Step 3: Store debugging info in vector memory
    remember(f"Debugging {agent_name}: {error_text}")

    # Step 4: Return debugging report
    state["result"] = (
        f"Error detected in agent '{agent_name}':\n\n"
        f"{error_text}\n"
        f"Suggested fix:\n{fix_suggestion}"
    )

    return state

def load():
    AGENT_REGISTRY["debugger"] = debugger_agent
    return debugger_agent
