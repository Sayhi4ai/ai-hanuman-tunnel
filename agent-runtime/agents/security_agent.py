from graph import AGENT_REGISTRY
from security_scanner import run_security_scan, auto_patch_agent

def security_agent(state):
    task = state.get("task", "").strip()

    # Expected:
    #   scan <agent>
    #   secure <agent>
    parts = task.split(" ", 1)
    if len(parts) < 2:
        state["result"] = "Usage: scan <agent> | secure <agent>"
        return state

    cmd, agent_name = parts[0], parts[1].strip()

    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        state["result"] = f"Agent '{agent_name}' not found."
        return state

    scan = run_security_scan(agent_name, agent_fn)

    if cmd == "scan":
        state["result"] = (
            f"Security scan for '{agent_name}':\n\n"
            f"Pattern hits: {scan['patterns']}\n\n"
            f"LLM Review:\n{scan['llm_review']}\n\n"
            f"Proposed Fixes:\n{scan['fixes']}"
        )
        state["history"].append("SECURITY_AGENT: scan complete")
        return state

    if cmd == "secure":
        new_name, filename, code = auto_patch_agent(agent_name, scan["fixes"])
        state["result"] = (
            f"Secure version created.\n\n"
            f"Old agent: {agent_name}\n"
            f"New agent: {new_name}\n"
            f"File: {filename}\n\n"
            f"Code:\n{code}"
        )
        state["history"].append("SECURITY_AGENT: secure version created")
        return state

    state["result"] = "Usage: scan <agent> | secure <agent>"
    return state

def load():
    AGENT_REGISTRY["security_agent"] = security_agent
    return security_agent
