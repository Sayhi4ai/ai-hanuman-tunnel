import requests
from vector_memory import remember
from messaging import send_message

def federation_handshake(url):
    try:
        r = requests.get(f"{url}/federation/hello")
        if r.status_code == 200:
            remember(f"federation_handshake_success: {url}")
            return r.json()
    except:
        pass
    remember(f"federation_handshake_failed: {url}")
    return None

def propose_treaty(local_capabilities, remote_capabilities):
    prompt = (
        "You are the federation negotiator.\n"
        "Given two ecosystems' capabilities, propose a cooperation treaty.\n\n"
        f"Local capabilities:\n{local_capabilities}\n\n"
        f"Remote capabilities:\n{remote_capabilities}\n"
    )
    return send_message("writer", prompt)

def exchange_capabilities(url):
    try:
        r = requests.get(f"{url}/federation/capabilities")
        return r.json()
    except:
        return None
