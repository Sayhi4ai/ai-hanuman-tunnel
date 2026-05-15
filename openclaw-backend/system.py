from fastapi import APIRouter
from app.integrations.opscaptain import opscaptain
import platform
from app.core.memory import memory_store
from app.core.knowledge_graph import knowledge_graph
from app.core.goals import goal_manager

router = APIRouter(prefix="/system", tags=["system"])

@router.get("/info")
async def system_info():
    return {
        "python_version": platform.python_version(),
        "system": platform.system(),
        "machine": platform.machine()
    }

from app.core.planner import planner

@router.get("/plans")
async def list_plans():
    return planner.active_plans

from app.core.recovery import recovery_engine

@router.get("/repairs")
async def repair_log():
    return recovery_engine.repair_log

@router.get("/events")
async def events():
    return opscaptain.get_events()

@router.get("/memory/tasks")
async def memory_tasks():
    return memory_store.get_tasks()

@router.get("/memory/facts")
async def memory_facts():
    return memory_store.get_facts()

@router.post("/memory/facts")
async def memory_add_fact(data: dict):
    memory_store.add_fact(data["key"], data["value"])
    return {"status": "added"}

@router.post("/kg/node")
async def kg_add_node(data: dict):
    knowledge_graph.add_node(data["id"], data.get("properties", {}))
    return {"status": "node_added"}

@router.post("/kg/edge")
async def kg_add_edge(data: dict):
    knowledge_graph.add_edge(data["source"], data["relation"], data["target"])
    return {"status": "edge_added"}

@router.get("/kg/node/{node_id}")
async def kg_get_node(node_id: str):
    return knowledge_graph.get_node(node_id)

@router.get("/kg/edges/{node_id}")
async def kg_get_edges(node_id: str):
    return knowledge_graph.get_edges(node_id)

@router.get("/kg/search/{text}")
async def kg_search(text: str):
    return knowledge_graph.search(text)

@router.post("/goals")
async def start_goal(data: dict):
    goal_id = await goal_manager.start_goal(data)
    return {"status": "started", "goal_id": goal_id}

@router.get("/goals")
async def list_goals():
    return goal_manager.goals
