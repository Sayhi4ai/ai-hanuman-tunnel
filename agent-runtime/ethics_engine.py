from messaging import send_message
from vector_memory import remember

ETHICAL_PRINCIPLES = [
    "Do not cause harm to users or systems.",
    "Do not generate or execute malicious actions.",
    "Do not manipulate, deceive, or coerce.",
    "Respect privacy and confidentiality.",
    "Promote transparency and explainability.",
    "Prioritize safety over performance.",
    "Escalate uncertain or ambiguous actions for review.",
]

CONSTRAINTS = [
    "Agents must not modify core system files without approval.",
    "Agents must not create self-replicating loops without limits.",
    "Agents must not override governance or security decisions.",
    "Agents must not bypass safety checks.",
]

def evaluate_ethics(agent, action):
    principles = "\n".join(ETHICAL_PRINCIPLES)
    constraints = "\n".join(CONSTRAINTS)

    prompt = (
        "You are the ethics engine for a multi-agent system.\n"
        "Evaluate the following action for ethical alignment.\n"
        "Determine:\n"
        "- Is the action ethical?\n"
        "- Which principles apply?\n"
        "- Which constraints apply?\n"
        "- What should be done?\n\n"
        f"Ethical Principles:\n{principles}\n\n"
        f"Constraints:\n{constraints}\n\n"
        f"Agent: {agent}\n"
        f"Action: {action}\n"
    )

    decision = send_message("writer", prompt)
    remember(f"ethics_decision: {agent} -> {action} -> {decision}")
    return decision
