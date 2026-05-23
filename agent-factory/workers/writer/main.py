from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Worker: writer")

class Job(BaseModel):
    goal: str
    metadata: dict | None = None

@app.get("/health")
async def health():
    return {"status": "ok", "worker": "writer"}

@app.post("/run")
async def run(job: Job):
    # TODO: implement real logic
    return {
        "worker": "writer",
        "result": f"Processed goal: {job.goal}"
    }
