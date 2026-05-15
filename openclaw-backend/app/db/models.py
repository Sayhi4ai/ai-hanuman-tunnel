from sqlmodel import SQLModel, Field
from typing import Optional

class Goal(SQLModel, table=True):
    id: str = Field(primary_key=True)
    payload: str
    status: str
    priority: int
    iterations: int

class Plan(SQLModel, table=True):
    id: str = Field(primary_key=True)
    payload: str
    status: str

class Agent(SQLModel, table=True):
    id: str = Field(primary_key=True)
    host: str
    capabilities: str
    status: str
    last_heartbeat: Optional[str] = None
