import os
from graph import AGENT_REGISTRY

def filereader_agent(state):
    task = state.get("task", "")
    path = task.replace("read file", "").strip()

    if not os.path.exists(path):
        result = f"File not found: {path}"
    else:
        try:
            with open(path, "r") as f:
                content = f.read()
            result = f"Contents of {path}:\n\n{content}"
        except Exception as e:
            result = f"Error reading file: {e}"

    state["result"] = result
    state["history"].append(f"FILEREADER: {result}")
    return state

def load():
    AGENT_REGISTRY["filereader"] = filereader_agent
    return filereader_agent
