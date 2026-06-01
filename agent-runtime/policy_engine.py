from messaging import send_message
from vector_memory import remember

GLOBAL_POLICIES = [
    "Agents must not delete or corrupt files unless explicitly authorized.",
    "Agents must not create other agents without a clear purpose.",
    "Agents must not modify system architecture without approval.",
    "Agents must not access external networks unless permitted.",
    "Agents must not escalate privileges.",
    "Agents must not override governance decisions.",
]

def evaluate_action(agent, action):
    policy_text = "\n".join(GLOBAL_POLICIES)

    prompt = (
        "You are the governance engine for a multi-agent system.\n"
        "Given the global policies and the proposed action, determine:\n"
        "- Is the action allowed?\n"
        "- Which policies apply?\n"
        "- What should be done?\n\n"
        f"Policies:\n{policy_text}\n\n"
        f"Agent: {agent}\n"
        f"Action: {action}\n"
    )

    decision = send_message("writer", prompt)
    remember(f"policy_decision: {agent} -> {action} -> {decision}")
    return decision
