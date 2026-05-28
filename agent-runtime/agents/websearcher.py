import requests
from graph import AGENT_REGISTRY

def websearcher_agent(state):
    query = state.get("task", "")
    url = f"https://api.duckduckgo.com/?q={query}&format=json"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        abstract = data.get("Abstract", "No summary found.")
        result = f"Search result for '{query}':\n\n{abstract}"
    except Exception as e:
        result = f"Search failed: {e}"

    state["result"] = result
    state["history"].append(f"WEBSEARCHER: {result}")
    return state

def load():
    AGENT_REGISTRY["websearcher"] = websearcher_agent
    return websearcher_agent
