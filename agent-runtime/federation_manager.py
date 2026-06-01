from federation_protocol import federation_handshake, exchange_capabilities, propose_treaty
from vector_memory import remember, recall

FEDERATED_ECOSYSTEMS = {}

def register_ecosystem(name, url):
    FEDERATED_ECOSYSTEMS[name] = url
    remember(f"federation_registered: {name} {url}")

def discover_ecosystems():
    entries = recall("federation_registered")
    for e in entries:
        _, name, url = e.split(" ")
        FEDERATED_ECOSYSTEMS[name] = url

def negotiate_federation(name, url, local_capabilities):
    hello = federation_handshake(url)
    if not hello:
        return None, "Handshake failed"

    remote_capabilities = exchange_capabilities(url)
    if not remote_capabilities:
        return None, "Capability exchange failed"

    treaty = propose_treaty(local_capabilities, remote_capabilities)
    remember(f"federation_treaty: {name} -> {treaty}")

    return treaty, remote_capabilities
