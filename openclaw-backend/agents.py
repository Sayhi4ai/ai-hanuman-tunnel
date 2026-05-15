from fastapi import APIRouter
from app.core.agent_manager import agent_manager
from app.core.spawner import spawner
from app.integrations.guardian import guardian
from app.integrations.browser_agent import browser_agent
from app.integrations.filesystem_agent import filesystem_agent
from app.integrations.guardian import guardian
from app.core.messaging import messaging_bus
from app.core.team_manager import team_manager

router = APIRouter(prefix="/agents", tags=["agents"])

@router.get("/")
async def list_agents():
    return await agent_manager.list_agents()

@router.post("/register")
async def register_agent(agent: dict):
    agent_id = agent.get("id")
    metadata = agent.get("metadata", {})
    await agent_manager.register_agent(agent_id, metadata)
    return {"status": "registered", "agent_id": agent_id}

@router.post("/spawn")
async def spawn_agent(metadata: dict):
    validation = guardian.validate_agent_metadata(metadata)
    if not validation["valid"]:
        return {"error": validation["reason"]}

    return await spawner.spawn_agent(metadata)

@router.get("/running")
async def running_agents():
    return await spawner.list_running_agents()

@router.post("/browser/start")
async def browser_start():
    await browser_agent.start()
    return {"status": "browser_started"}

@router.post("/browser/navigate")
async def browser_navigate(data: dict):
    return await browser_agent.navigate(data["url"])

@router.post("/browser/extract")
async def browser_extract(data: dict):
    return await browser_agent.extract_text(data["selector"])

@router.post("/browser/click")
async def browser_click(data: dict):
    return await browser_agent.click(data["selector"])

@router.post("/fs/read")
async def fs_read(data: dict):
    validation = guardian.validate_path(data["path"])
    if not validation["valid"]:
        return {"error": validation["reason"]}

    return filesystem_agent.read_file(data["path"])

@router.post("/fs/write")
async def fs_write(data: dict):
    validation = guardian.validate_path(data["path"])
    if not validation["valid"]:
        return {"error": validation["reason"]}

    return filesystem_agent.write_file(data["path"], data["content"])

@router.post("/fs/list")
async def fs_list(data: dict):
    validation = guardian.validate_path(data["path"])
    if not validation["valid"]:
        return {"error": validation["reason"]}

    return filesystem_agent.list_dir(data["path"])

@router.post("/fs/delete")
async def fs_delete(data: dict):
    validation = guardian.validate_path(data["path"])
    if not validation["valid"]:
        return {"error": validation["reason"]}

    return filesystem_agent.delete_file(data["path"])

@router.post("/message")
async def send_message(data: dict):
    topic = data["topic"]
    message = data["message"]
    await messaging_bus.publish(topic, message)
    return {"status": "sent", "topic": topic}

@router.post("/team/create")
async def create_team(data: dict):
    team_manager.create_team(data["team_id"])
    return {"status": "created", "team_id": data["team_id"]}

@router.post("/team/add")
async def add_agent_to_team(data: dict):
    team_manager.add_agent(data["team_id"], data["agent_id"])
    return {"status": "added"}

@router.post("/team/message")
async def message_team(data: dict):
    team_id = data["team_id"]
    message = data["message"]
    members = team_manager.get_team(team_id)
    for agent_id in members:
        await messaging_bus.publish(agent_id, message)
    return {"status": "sent", "team_id": team_id, "members": members}
