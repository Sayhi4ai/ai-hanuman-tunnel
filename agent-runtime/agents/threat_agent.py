from graph import AGENT_REGISTRY
from threat_detector import detect_threats
from task_queue import enqueue
from vector_memory import remember

def threat_agent(state):
    task = state.get("task", "").strip()

    # Expected:
    #   scan <agent>
    #   quarantine <agent>
    parts = task.split(" ", 1)
    if len(parts) < 2:
        state["result"] = "Usage: scan <agent> | quarantine <agent>"
        return state

    cmd, agent_name = parts[0], parts[1].strip()

    agent_fn = AGENT_REGISTRY.get(agent_name)
    if not agent_fn:
        state["result"] = f"Agent '{agent_name}' not found."
        return state

    threats = detect_threats(agent_name, agent_fn)

    if cmd == "scan":
        state["result"] = (
            f"Threat scan for '{agent_name}':\n\n"
            f"Suspicious code patterns: {threats['code_hits']}\n\n"
            f"Suspicious memory entries: {threats['memory_hits']}\n\n"
            f"Suspicious queue tasks: {threats['queue_hits']}\n\n"
            f"LLM Threat Assessment:\n{threats['llm_assessment']}"
        )
        state["history"].append("THREAT_AGENT: scan complete")
        return state

    if cmd == "quarantine":
        remember(f"quarantined_agent: {agent_name}")
        enqueue(f"secure {agent_name}", "security_agent", priority=10)
        state["result"] = (
            f"Agent '{agent_name}' quarantined.\n"
            f"A security patch task has been scheduled."
        )
        state["history"].append("THREAT_AGENT: agent quarantined")
        return state

    state["result"] = "Usage: scan <agent> | quarantine <agent>"
    return state

def load():
    AGENT_REGISTRY["threat_agent"] = threat_agent
    return threat_agent
