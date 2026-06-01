import os
import importlib
import inspect
from graph import AGENT_REGISTRY
from agent_factory import create_agent
from messaging import send_message
from vector_memory import remember

AGENTS_DIR = "agents"

def check_agent_file(agent_name):
    path = f"{AGENTS_DIR}/{agent_name}.py"
    return os.path.exists(path)

def check_agent_load(agent_name):
    try:
        module_name = f"agents.{agent_name}"
        importlib.import_module(module_name)
        return True
    except Exception:
        return False

def regenerate_agent(agent_name):
    description = send_message(
        "writer",
        f"Describe the purpose of an agent named '{agent_name}' based on its name. "
        "Then write a short description of what it should do."
    )

    filename, code = create_agent(agent_name, description)
    remember(f"registry_healer regenerated {agent_name}")
    return filename, code

def heal_registry():
    healed = []

    for agent_name in list(AGENT_REGISTRY.keys()):
        file_ok = check_agent_file(agent_name)
        load_ok = check_agent_load(agent_name)

        if file_ok and load_ok:
            continue

        filename, code = regenerate_agent(agent_name)
        healed.append((agent_name, filename, code))

    return healed
