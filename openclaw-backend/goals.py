import asyncio
from typing import Dict, Any
from app.integrations.opscaptain import opscaptain
from app.core.planner import planner  # assuming you have a planner instance
from app.core.memory import memory_store

class GoalManager:
    def __init__(self):
        self.goals: Dict[str, Dict[str, Any]] = {}
        self.counter = 0

    async def start_goal(self, goal: Dict[str, Any]) -> str:
        self.counter += 1
        goal_id = f"goal-{self.counter}"
        self.goals[goal_id] = {"goal": goal, "status": "running"}
        opscaptain.log_event("goal_started", {"goal_id": goal_id, "goal": goal})
        asyncio.create_task(self.goal_loop(goal_id))
        return goal_id

    async def goal_loop(self, goal_id: str):
        goal_entry = self.goals[goal_id]
        goal = goal_entry["goal"]

        while True:
            # Run planner for this goal
            result = await planner.run_plan({"task": goal.get("description", "")})
            memory_store.add_task({
                "type": "goal_iteration",
                "goal_id": goal_id,
                "result": result,
            })

            # Simple stopping condition hook
            if result.get("status") == "done" or goal.get("one_shot"):
                self.goals[goal_id]["status"] = "completed"
                opscaptain.log_event("goal_completed", {"goal_id": goal_id})
                break

            await asyncio.sleep(goal.get("interval", 10))

goal_manager = GoalManager()
