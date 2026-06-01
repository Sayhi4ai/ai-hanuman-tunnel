from graph import AGENT_REGISTRY
from policy_engine import evaluate_action, GLOBAL_POLICIES
from task_queue import enqueue
from vector_memory import remember

def governance_agent(state):
    task = state.get("task", "").strip()

    # Expected:
    #   evaluate <agent> | <action>
    #   show policies
    #   add policy <text>
    if task == "show policies":
        state["result"] = "Global Policies:\n" + "\n".join(GLOBAL_POLICIES)
        return state

    if task.startswith("add policy"):
        new_policy = task.replace("add policy", "").strip()
        GLOBAL_POLICIES.append(new_policy)
        remember(f"policy_added: {new_policy}")
        state["result"] = f"Policy added: {new_policy}"
        return state

    if " | " in task:
        agent, action = [x.strip() for x in task.split("|", 1)]
        decision = evaluate_action(agent, action)

        # Auto-enforce if needed
        if "deny" in decision.lower() or "not allowed" in decision.lower():
            enqueue(f"quarantine {agent}", "threat_agent", priority=10)
            state["history"].append("GOVERNANCE: enforcement triggered")

        state["result"] = (
            f"Governance decision for agent '{agent}':\n\n"
            f"{decision}\n\n"
            "Enforcement actions have been scheduled if required."
        )
        return state

    state["result"] = (
        "Usage:\n"
        "- evaluate <agent> | <action>\n"
        "- show policies\n"
        "- add policy <text>"
    )
    return state

def load():
    AGENT_REGISTRY["governance_agent"] = governance_agent
    return governance_agent
