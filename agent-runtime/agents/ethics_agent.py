from graph import AGENT_REGISTRY
from ethics_engine import evaluate_ethics, ETHICAL_PRINCIPLES, CONSTRAINTS
from task_queue import enqueue
from vector_memory import remember

def ethics_agent(state):
    task = state.get("task", "").strip()

    # Commands:
    #   evaluate <agent> | <action>
    #   show ethics
    #   show constraints
    #   add principle <text>
    #   add constraint <text>

    if task == "show ethics":
        state["result"] = "Ethical Principles:\n" + "\n".join(ETHICAL_PRINCIPLES)
        return state

    if task == "show constraints":
        state["result"] = "Constraints:\n" + "\n".join(CONSTRAINTS)
        return state

    if task.startswith("add principle"):
        new_p = task.replace("add principle", "").strip()
        ETHICAL_PRINCIPLES.append(new_p)
        remember(f"ethics_principle_added: {new_p}")
        state["result"] = f"Principle added: {new_p}"
        return state

    if task.startswith("add constraint"):
        new_c = task.replace("add constraint", "").strip()
        CONSTRAINTS.append(new_c)
        remember(f"ethics_constraint_added: {new_c}")
        state["result"] = f"Constraint added: {new_c}"
        return state

    if " | " in task:
        agent, action = [x.strip() for x in task.split("|", 1)]
        decision = evaluate_ethics(agent, action)

        # Auto-escalate if unethical
        if "not ethical" in decision.lower() or "deny" in decision.lower():
            enqueue(f"evaluate {agent} | {action}", "governance_agent", priority=10)
            enqueue(f"scan {agent}", "security_agent", priority=9)
            state["history"].append("ETHICS: escalated to governance & security")

        state["result"] = (
            f"Ethical evaluation for agent '{agent}':\n\n"
            f"{decision}\n\n"
            "Escalation triggered if required."
        )
        return state

    state["result"] = (
        "Usage:\n"
        "- evaluate <agent> | <action>\n"
        "- show ethics\n"
        "- show constraints\n"
        "- add principle <text>\n"
        "- add constraint <text>"
    )
    return state

def load():
    AGENT_REGISTRY["ethics_agent"] = ethics_agent
    return ethics_agent
