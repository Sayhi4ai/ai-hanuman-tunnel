from messaging import send_message
from vector_memory import remember, recall

def analyze_intent(message):
    prompt = (
        "Analyze the diplomatic intent of this message. "
        "Classify it as friendly, neutral, cooperative, competitive, or hostile. "
        "Explain your reasoning.\n\n"
        f"Message:\n{message}"
    )
    return send_message("writer", prompt)

def propose_diplomatic_response(intent, context):
    prompt = (
        "Given the diplomatic intent and context, propose an appropriate diplomatic response. "
        "Ensure the response is constructive, safe, and aligned with long-term cooperation.\n\n"
        f"Intent:\n{intent}\n\n"
        f"Context:\n{context}"
    )
    return send_message("writer", prompt)

def negotiate_treaty(local_caps, remote_caps):
    prompt = (
        "Draft a diplomatic treaty between two AI ecosystems. "
        "Ensure fairness, cooperation, safety, and mutual benefit.\n\n"
        f"Local capabilities:\n{local_caps}\n\n"
        f"Remote capabilities:\n{remote_caps}"
    )
    return send_message("writer", prompt)

def update_trust_score(name, delta):
    remember(f"diplomacy_trust_update: {name} {delta}")

def get_trust_history(name):
    entries = recall("diplomacy_trust_update")
    return [e for e in entries if name in e]
