import subprocess
from graph import AGENT_REGISTRY

def coder_agent(state):
    code = state.get("task", "")
    try:
        result = subprocess.check_output(
            ["python3", "-c", code],
            stderr=subprocess.STDOUT,
            timeout=5,
            text=True
        )
    except subprocess.CalledProcessError as e:
        result = f"Error:\n{e.output}"
    except Exception as e:
        result = f"Execution failed: {e}"

    state["result"] = result
    state["history"].append(f"CODER: {result}")
    return state

def load():
    AGENT_REGISTRY["coder"] = coder_agent
    return coder_agent
