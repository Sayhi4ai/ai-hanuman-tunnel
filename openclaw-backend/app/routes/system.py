from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from app.core.goals import goal_manager
from app.core.planner import planner
from app.core.serializer import safe

router = APIRouter(prefix="/system", tags=["system"])

# Simple in-memory websocket connection store
class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict) -> None:
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

ws_manager = ConnectionManager()

@router.get("/goals")
async def list_goals():
    return safe(goal_manager.goals)

@router.post("/goals")
async def create_goal(goal: dict):
    goal_id = goal_manager.create_goal(goal)
    await ws_manager.broadcast({"type": "goal_created", "id": goal_id})
    return {"id": goal_id}

@router.get("/goals/raw")
async def list_goals_raw():
    return safe(goal_manager.goals)

@router.get("/plans")
async def list_plans():
    return safe(planner.active_plans)

@router.websocket("/ws")
async def system_ws(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep alive / ignore client messages
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
