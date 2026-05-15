import asyncio
from fastapi import FastAPI
from typing import Dict, Any
from .config import RUNTIME_HOST, RUNTIME_PORT, WORKER_COUNT
from .runtime import runtime_engine

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    runtime_engine.worker_count = WORKER_COUNT
    asyncio.create_task(runtime_engine.start())

@app.on_event("shutdown")
async def shutdown_event():
    await runtime_engine.stop()

@app.post("/run")
async def run_task(payload: Dict[str, Any]):
    # Synchronous processing path for your backend
    result = await runtime_engine.process_task({"payload": payload})
    return result

@app.get("/result/{task_id}")
async def get_result(task_id: str):
    return runtime_engine.results.get(task_id, {"status": "unknown_task"})

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "workers": runtime_engine.worker_count,
        "queued": runtime_engine.queue.qsize(),
        "completed": len(runtime_engine.results),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=RUNTIME_HOST, port=RUNTIME_PORT, reload=False)
