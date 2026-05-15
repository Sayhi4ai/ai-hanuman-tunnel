from typing import Dict, Any
import httpx

# Your backend exposes browser + filesystem tools
BACKEND_URL = "http://localhost:8081"

async def call_backend(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(f"{BACKEND_URL}{path}", json=payload)
        return response.json()

async def handle_tool(task: Dict[str, Any]) -> Dict[str, Any]:
    action = task.get("action")

    # Echo (debug)
    if action == "echo":
        return {"status": "ok", "echo": task}

    # Browser actions
    if action == "browser_start":
        return await call_backend("/agents/browser/start", {})

    if action == "browser_navigate":
        return await call_backend("/agents/browser/navigate", {"url": task["url"]})

    if action == "browser_extract":
        return await call_backend("/agents/browser/extract", {"selector": task["selector"]})

    if action == "browser_click":
        return await call_backend("/agents/browser/click", {"selector": task["selector"]})

    # Filesystem actions
    if action == "fs_read":
        return await call_backend("/agents/fs/read", {"path": task["path"]})

    if action == "fs_write":
        return await call_backend("/agents/fs/write", {"path": task["path"], "content": task["content"]})

    if action == "fs_list":
        return await call_backend("/agents/fs/list", {"path": task["path"]})

    if action == "fs_delete":
        return await call_backend("/agents/fs/delete", {"path": task["path"]})

    return {"status": "unknown_action", "task": task}
