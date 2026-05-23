from fastapi import FastAPI
from openclaw.tool_registry import TOOLS, call_tool
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
        "tools": list(TOOLS.keys()),
        "agents": [],
        "uptime": "local-dev"
    }

@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": name,
                "schema": TOOLS[name].schema
            }
            for name in TOOLS
        ]
    }

@app.post("/tools/run")
def run_tool(payload: dict):
    tool_name = payload.get("tool")
    args = payload.get("arguments", {})

    if tool_name not in TOOLS:
        return {"error": f"Unknown tool: {tool_name}"}

    result = call_tool(tool_name, **args)

    return {
        "status": "ok",
        "tool": tool_name,
        "result": result
    }
