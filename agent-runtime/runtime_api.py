from fastapi import FastAPI
from pydantic import BaseModel
from graph import app_graph, TASK_QUEUE, State
from logger import log
from graph import AGENT_REGISTRY

app = FastAPI(title="Agent Runtime")

class TaskRequest(BaseModel):
    task: str

class AgentTask(BaseModel):
    task: str
    agent: str

@app.get("/")
async def root():
    return {"status": "agent-runtime-online"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/run")
async def run_task(req: TaskRequest):
    log("task_received", task=req.task)
    state: State = {"task": req.task, "history": [], "result": ""}
    result_state = app_graph.invoke(state)
    log("task_completed", result=result_state["result"])
    return {
        "task": req.task,
        "history": result_state["history"],
        "result": result_state["result"],
    }

@app.post("/run-agent")
async def run_agent(req: AgentTask):
    log("agent_task_received", task=req.task, agent=req.agent)
    state = {"task": req.task, "agent": req.agent, "history": [], "result": ""}
    result_state = app_graph.invoke(state)
    log("agent_task_completed", result=result_state["result"])
    return result_state

@app.post("/enqueue")
async def enqueue(req: TaskRequest):
    TASK_QUEUE.put(req.task)
    return {"status": "queued", "task": req.task}

@app.get("/gateway-info")
async def gateway_info():
    return {
        "name": "agent-runtime",
        "version": "1.0",
        "capabilities": ["planner", "worker", "validator", "governor"],
        "port": 7200,
        "status": "online"
    }

@app.get("/agents")
async def list_agents():
    return {"agents": list(AGENT_REGISTRY.keys())}
