import os
import importlib
from messaging import send_message
from vector_memory import remember

AGENTS_DIR = "agents"

def create_agent_file(name, code):
    filename = f"{AGENTS_DIR}/{name}.py"
    with open(filename, "w") as f:
        f.write(code)
    return filename

def load_agent_module(name):
    module_name = f"agents.{name}"
    if module_name in list(importlib.sys.modules.keys()):
        importlib.reload(importlib.sys.modules[module_name])
    else:
        importlib.import_module(module_name)

def generate_agent_code(description):
    prompt = (
        "Write a complete Python agent function for my agent-runtime system.\n"
        "It must:\n"
        "- define a function agent(state)\n"
        "- update state['result']\n"
        "- update state['history']\n"
        "- include a load() function that registers the agent\n\n"
        f"Agent description:\n{description}\n"
    )
    return send_message("writer", prompt)

def create_agent(name, description):
    code = generate_agent_code(description)
    filename = create_agent_file(name, code)
    load_agent_module(name)
    remember(f"agent_created {name}: {description}")
    return filename, code
