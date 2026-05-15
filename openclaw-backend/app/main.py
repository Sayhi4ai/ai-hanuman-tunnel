import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.db import init_db
from app.core.goals import goal_manager
from app.core.planner import planner
from app.routes import system as system_routes

app = FastAPI(title="OpenClaw Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.on_event("startup")
async def startup_event():
    init_db()
    goal_manager.load_from_db()
    planner.load_from_db()
    # here you can reattach loops, schedulers, etc.
    # e.g. asyncio.create_task(goal_scheduler_loop())

app.include_router(system_routes.router)
