from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AgentFactory Guardian")

class Payload(BaseModel):
  goal: str | None = None
  metadata: dict | None = None
  output: str | None = None

@app.get("/health")
async def health():
  return {"status": "ok", "component": "guardian"}

@app.post("/validate/input")
async def validate_input(payload: Payload):
  if not payload.goal:
    return {"ok": False, "reason": "missing_goal"}
  return {"ok": True}

@app.post("/validate/output")
async def validate_output(payload: Payload):
  # stub: add safety / policy checks here
  return {"ok": True}
