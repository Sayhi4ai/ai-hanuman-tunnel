import json
from typing import Dict, Any
from app.db.db import get_session
from app.db.models import Plan

class Planner:
    def __init__(self) -> None:
        self.active_plans: Dict[str, Dict[str, Any]] = {}

    def load_from_db(self) -> None:
        with get_session() as session:
            for row in session.query(Plan).all():
                self.active_plans[row.id] = json.loads(row.payload)

    def create_plan(self, plan_id: str, payload: Dict[str, Any]) -> None:
        self.active_plans[plan_id] = payload
        self._save_plan(plan_id)

    def _save_plan(self, plan_id: str) -> None:
        payload = self.active_plans[plan_id]
        with get_session() as session:
            db_plan = session.get(Plan, plan_id) or Plan(id=plan_id)
            db_plan.payload = json.dumps(payload)
            db_plan.status = payload.get("status", "pending")
            session.add(db_plan)
            session.commit()

planner = Planner()
