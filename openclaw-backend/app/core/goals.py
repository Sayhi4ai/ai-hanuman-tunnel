import json
import uuid
from typing import Dict, Any
from app.db.db import get_session
from app.db.models import Goal

class GoalManager:
    def __init__(self) -> None:
        self.goals: Dict[str, Dict[str, Any]] = {}

    def load_from_db(self) -> None:
        with get_session() as session:
            for row in session.query(Goal).all():
                self.goals[row.id] = {
                    "goal": json.loads(row.payload),
                    "status": row.status,
                    "priority": row.priority,
                    "iterations": row.iterations,
                    "task": None,
                }

    def create_goal(self, payload: Dict[str, Any]) -> str:
        goal_id = str(uuid.uuid4())
        self.goals[goal_id] = {
            "goal": payload,
            "status": "pending",
            "priority": payload.get("priority", 1),
            "iterations": 0,
            "task": None,
        }
        self._save_goal(goal_id)
        return goal_id

    def update_status(self, goal_id: str, status: str) -> None:
        if goal_id in self.goals:
            self.goals[goal_id]["status"] = status
            self._save_goal(goal_id)

    def _save_goal(self, goal_id: str) -> None:
        entry = self.goals[goal_id]
        with get_session() as session:
            db_goal = session.get(Goal, goal_id) or Goal(id=goal_id)
            db_goal.payload = json.dumps(entry["goal"])
            db_goal.status = entry["status"]
            db_goal.priority = entry.get("priority", 1)
            db_goal.iterations = entry.get("iterations", 0)
            session.add(db_goal)
            session.commit()

goal_manager = GoalManager()
