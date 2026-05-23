from fastapi import APIRouter
from pydantic import BaseModel
from openclaw.opscaptain import opscaptain
from openclaw.planner import planner
from openclaw.executor import executor

router = APIRouter()

class AutoRun(BaseModel):
    goal: str

@router.post("/auto/run")
def auto_run(req: AutoRun):
    session_id = opscaptain.start_task(req.goal)

    while True:
        stage = opscaptain.detect_stage(session_id)
        steps = planner.plan(req.goal, stage)

        # If no more steps, break
        if not steps:
            break

        for step in steps:
            routed = opscaptain.route_step(session_id, step)
            result = executor.run_step(routed["agent"], routed["instruction"])
            opscaptain.record_result(session_id, result)

        # Stop when final result is complete
        if "final" in opscaptain.sessions[session_id]["results"][-1].lower():
            break

    return {
        "session_id": session_id,
        "results": opscaptain.sessions[session_id]["results"]
    }
