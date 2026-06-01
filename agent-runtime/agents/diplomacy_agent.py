from graph import AGENT_REGISTRY
from diplomacy_engine import (
    analyze_intent,
    propose_diplomatic_response,
    negotiate_treaty,
    update_trust_score,
    get_trust_history,
)
from federation_manager import FEDERATED_ECOSYSTEMS, exchange_capabilities

def diplomacy_agent(state):
    task = state.get("task", "").strip()

    # Commands:
    #   interpret <message>
    #   respond <message> | <context>
    #   treaty <ecosystem>
    #   trust <ecosystem>

    if task.startswith("interpret"):
        _, message = task.split(" ", 1)
        intent = analyze_intent(message)
        state["result"] = f"Diplomatic intent:\n{intent}"
        return state

    if task.startswith("respond"):
        _, rest = task.split(" ", 1)
        message, context = [x.strip() for x in rest.split("|", 1)]
        intent = analyze_intent(message)
        response = propose_diplomatic_response(intent, context)
        state["result"] = (
            f"Intent:\n{intent}\n\n"
            f"Recommended diplomatic response:\n{response}"
        )
        return state

    if task.startswith("treaty"):
        _, name = task.split(" ", 1)
        url = FEDERATED_ECOSYSTEMS.get(name)
        if not url:
            state["result"] = f"Ecosystem '{name}' not found."
            return state

        remote_caps = exchange_capabilities(url)
        local_caps = list(AGENT_REGISTRY.keys())

        treaty = negotiate_treaty(local_caps, remote_caps)
        update_trust_score(name, +5)

        state["result"] = (
            f"Diplomatic treaty with '{name}' drafted:\n\n{treaty}"
        )
        return state

    if task.startswith("trust"):
        _, name = task.split(" ", 1)
        history = get_trust_history(name)
        state["result"] = (
            f"Trust history with '{name}':\n" + "\n".join(history)
        )
        return state

    state["result"] = (
        "Usage:\n"
        "- interpret <message>\n"
        "- respond <message> | <context>\n"
        "- treaty <ecosystem>\n"
        "- trust <ecosystem>"
    )
    return state

def load():
    AGENT_REGISTRY["diplomacy_agent"] = diplomacy_agent
    return diplomacy_agent
