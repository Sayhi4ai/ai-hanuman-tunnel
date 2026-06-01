from graph import AGENT_REGISTRY
from cluster_manager import run_remote

def distributed_agent(state):
    task = state.get("task", "").strip()

    # Expected:
    #   <agent> | <task>
    if "|" not in task:
        state["result"] = "Usage: <agent> | <task>"
        return state

    agent, inner_task = [x.strip() for x in task.split("|", 1)]

    # Try remote execution
    result, node = run_remote(agent, inner_task)

    if result:
        state["result"] = (
            f"Executed on remote node: {node}\n\n"
            f"Output:\n{result}"
        )
        state["history"].append("DISTRIBUTED_AGENT: remote execution")
        return state

    # Fallback to local
    agent_fn = AGENT_REGISTRY.get(agent)
    if not agent_fn:
        state["result"] = f"Agent '{agent}' not found locally or remotely."
        return state

    sub_state = {"task": inner_task, "history": [], "result": ""}
    result_state = agent_fn(sub_state)

    state["result"] = (
        "Remote execution unavailable. Fallback to local.\n\n"
        f"Output:\n{result_state['result']}"
    )
    state["history"].append("DISTRIBUTED_AGENT: local fallback")
    return state

def load():
    AGENT_REGISTRY["distributed_agent"] = distributed_agent
    return distributed_agent
