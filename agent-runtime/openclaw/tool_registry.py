import importlib
import os

TOOLS_DIR = "openclaw/tools"

def load_tools():
    tools = {}
    for file in os.listdir(TOOLS_DIR):
        if file.endswith(".py") and not file.startswith("__"):
            name = file[:-3]
            module = importlib.import_module(f"openclaw.tools.{name}")
            tools[name] = module
    return tools

TOOLS = load_tools()

def call_tool(name, **kwargs):
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    return TOOLS[name].run(**kwargs)

