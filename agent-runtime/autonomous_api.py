from fastapi import APIRouter
from pydantic import BaseModel
from openclaw.opscaptain import opscaptain
from openclaw.planner import planner

router = APIRouter()

class AutoStart(BaseModel):
    goal: str

@router.post("/auto/start")
def auto_start(req: AutoStart):
    session_id = opscaptain.start_task(req.goal)
    stage = "none"
    steps = planner.plan(req.goal, stage)
    return {"session_id": session_id, "steps": steps, "stage": stage}

class AutoNext(BaseModel):
    session_id: str

@router.post("/auto/next")
def auto_next(req: AutoNext):
    session = opscaptain.sessions[req.session_id]

    stage = opscaptain.detect_stage(req.session_id)
    steps = planner.plan(session["goal"], stage)

    routed = []
    for step in steps:
        routed_step = opscaptain.route_step(req.session_id, step)
        routed.append(routed_step)

    return {"steps": routed, "stage": stage}
