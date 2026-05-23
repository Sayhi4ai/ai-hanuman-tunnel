from fastapi import FastAPI

app = FastAPI(title="AgentFactory OpsCaptain")

@app.get("/health")
async def health():
  return {"status": "ok", "component": "ops"}

@app.post("/heal")
async def heal():
  # stub: restart workers, clear queues, etc.
  return {"status": "healing_triggered"}
