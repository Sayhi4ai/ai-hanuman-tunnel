from fastapi import FastAPI
from openclaw.tool_registry import TOOLS
from chat import router as chat_router
from opscaptain_api import router as opscaptain_router
from autonomous_api import router as auto_router
from autonomous_run_api import router as auto_run_router
import json
import os

app = FastAPI()

app.include_router(opscaptain_router)
app.include_router(chat_router)
app.include_router(auto_router)
app.include_router(auto_run_router)

@app.get("/system/info")
def system_info():
    return {
        "name": "Human Runtime",
        "version": "1.0.0",
        "status": "ok",
        "tools": [],
        "agents": [],
        "uptime": "local-dev"
    }

@app.get("/tools")
def list_tools():
    return {
        "tools": []
    }

@app.post("/execute")
def execute_tool(payload: dict):
    tool_name = payload.get("tool")
    args = payload.get("arguments", {})

    if tool_name not in TOOLS:
        return {"error": f"Unknown tool: {tool_name}"}

    result = TOOLS[tool_name]["run"](**args)

    return {
        "status": "ok",
        "tool": tool_name,
        "result": result
    }


@app.get("/tools")
def list_tools():
    return {
        "tools": [TOOLS[name]["schema"] for name in TOOLS]
    }

@app.get("/agents")
def list_agents():
    agents_dir = "openclaw/agents"
    agents = []

    for file in os.listdir(agents_dir):
        if file.endswith(".json"):
            with open(os.path.join(agents_dir, file)) as f:
                agents.append(json.load(f))

    return {"agents": agents}
