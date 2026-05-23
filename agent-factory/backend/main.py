from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx, os

app = FastAPI(title="AgentFactory Backend")

GUARDIAN_URL = os.getenv("GUARDIAN_URL", "http://127.0.0.1:9001")
OPS_URL = os.getenv("OPS_URL", "http://127.0.0.1:9002")

class Task(BaseModel):
  goal: str
  metadata: dict | None = None

def redact(data: str) -> str:
  for key in ["api_key", "token", "secret"]:
    data = data.replace(key, "***")
  return data

@app.get("/health")
async def health():
  return {"status": "ok", "component": "backend"}

@app.post("/tasks")
async def create_task(task: Task):
  async with httpx.AsyncClient() as client:
    await client.post(f"{GUARDIAN_URL}/validate/input", json=task.model_dump())
  # stub: spawn agent, enqueue work, etc.
  return {"status": "accepted", "goal": task.goal}

@app.post("/agents/spawn")
async def spawn_agent(body: dict):
  # stub: spawn a worker/agent process
  return {"status": "spawned", "agent": body.get("name", "unnamed")}

@app.post("/log")
async def log_event(req: Request):
  body = await req.body()
  redacted = redact(body.decode("utf-8", errors="ignore"))
  print("[BACKEND LOG]", redacted, flush=True)
  return {"status": "logged"}
