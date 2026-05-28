from graph import AGENT_REGISTRY
from messaging import send_message
from workflow_store import get_workflow, save_workflow
from vector_memory import remember, recall

def workflow_editor_agent(state):
    task = state.get("task", "")

    # Expected format: "improve <workflow_name>"
    parts = task.split(" ", 1)
    if len(parts) < 2:
        state["result"] = "Usage: improve <workflow_name>"
        return state

    name = parts[1]
    workflow = get_workflow(name)

    if not workflow:
        state["result"] = f"No workflow named '{name}' found."
        return state

    # Retrieve past improvements
    related = recall(f"workflow {name}")

    # Ask writer to propose improvements
    suggestion = send_message(
        "writer",
        f"Improve this workflow:\n{workflow}\n\n"
        f"Past related improvements:\n{related}"
    )

    # Ask coder to rewrite the workflow steps
    rewritten = send_message(
        "writer",
        f"Rewrite the workflow steps clearly as a Python list of dicts:\n{suggestion}"
    )

    # Save improved workflow
    try:
        new_steps = eval(rewritten)
        save_workflow(name, new_steps)
        remember(f"workflow {name}: {new_steps}")
        result = f"Workflow '{name}' improved and saved.\n\nNew steps:\n{new_steps}"
    except Exception as e:
        result = f"Failed to parse improved workflow:\n{rewritten}\n\nError: {e}"

    state["result"] = result
    state["history"].append("WORKFLOW_EDITOR: improved workflow")
    return state

def load():
    AGENT_REGISTRY["workflow_editor"] = workflow_editor_agent
    return workflow_editor_agent
