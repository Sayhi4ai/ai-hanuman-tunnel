from graph import AGENT_REGISTRY
from workflows import run_workflow

def workflow_agent(state):
    task = state.get("task", "")

    # Example workflow: research → summarize → write
    steps = [
        {"agent": "websearcher", "task": "{input}"},
        {"agent": "writer", "task": "Summarize this: {input}"},
        {"agent": "writer", "task": "Rewrite this clearly: {input}"}
    ]

    result_state = run_workflow(steps, initial_input=task)

    state["result"] = result_state["result"]
    state["history"].append("WORKFLOW: completed")
    state["history"].extend(result_state["history"])
    return state

def load():
    AGENT_REGISTRY["workflow"] = workflow_agent
    return workflow_agent
