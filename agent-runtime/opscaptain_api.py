from fastapi import APIRouter
from pydantic import BaseModel
from openclaw.opscaptain import opscaptain

router = APIRouter()

class StartTask(BaseModel):
    goal: str

class AddStep(BaseModel):
    session_id: str
    agent: str
    instruction: str

class RecordResult(BaseModel):
    session_id: str
    result: str

@router.post("/opscaptain/start")
def start_task(req: StartTask):
    session_id = opscaptain.start_task(req.goal)
    return {"session_id": session_id}

@router.post("/opscaptain/step")
def add_step(req: AddStep):
    step = opscaptain.add_step(req.session_id, req.agent, req.instruction)
    return {"step": step}

@router.post("/opscaptain/result")
def record_result(req: RecordResult):
    opscaptain.record_result(req.session_id, req.result)
    return {"status": "ok"}

@router.get("/opscaptain/summary/{session_id}")
def summary(session_id: str):
    return {"summary": opscaptain.summarize(session_id)}
