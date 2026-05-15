import asyncio
from typing import Dict, Any, List
from tenacity import retry, stop_after_attempt, wait_fixed
from app.integrations.guardian import guardian
from app.integrations.opscaptain import opscaptain
from app.integrations.agent_runtime import agent_runtime
from app.core.messaging import messaging_bus
from app.core.memory import memory_store
from app.core.knowledge_graph import knowledge_graph

class Planner:
    def __init__(self):
        self.active_plans: Dict[str, Dict[str, Any]] = {}

    async def create_plan(self, task: dict) -> dict:
        """
        Break a task into subtasks.
        This is a placeholder for real LLM-based planning.
        """
        plan_id = f"plan-{len(self.active_plans)+1}"
        subtasks = [
            {"step": 1, "action": "analyze", "input": task},
            {"step": 2, "action": "execute", "input": task},
            {"step": 3, "action": "summarize", "input": task},
        ]

        self.active_plans[plan_id] = {
            "original_task": task,
            "subtasks": subtasks,
            "status": "created"
        }

        opscaptain.log_event("plan_created", {"plan_id": plan_id, "task": task})

        return {"plan_id": plan_id, "subtasks": subtasks}
        @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
        async def execute_subtask(self, subtask: dict) -> dict:
            """
            Execute a subtask using agent-runtime.
            """
            result = await agent_runtime.send_task(subtask)
            reflection = {
                "id": f"reflection-{subtask.get('id', 'unknown')}",
                "subtask": subtask,
                "result": result,
                "summary": f"Subtask {subtask.get('id')} completed with status {result.get('status', 'unknown')}",
            }

  	    # Store in memory
	    memory_store.add_task({
	        "type": "reflection",
	        "reflection": reflection,
	    })

	    # Store in knowledge graph
	    knowledge_graph.add_node(reflection["id"], reflection)

	    # Broadcast to interested agents
	    await messaging_bus.publish("reflections", {
	        "reflection": reflection
	    })
            return {"subtask": subtask, "result": result}
            await messaging_bus.publish("plan_updates", {
                "plan_id": plan_id,
                "subtask": subtask,
                "status": "completed"
            })

            opscaptain.log_event("subtask_completed", {"plan_id": plan_id, "subtask": subtask})

    async def run_plan(self, plan_id: str) -> dict:
        """
        Execute all subtasks in sequence.
        """
        plan = self.active_plans.get(plan_id)
        if not plan:
            return {"error": "plan not found"}

        results: List[dict] = []
        kg_context = knowledge_graph.search(task.get("task", ""))

        for subtask in plan["subtasks"]:
            result = await self.execute_subtask(subtask)
            results.append(result)

        plan["status"] = "completed"
        plan["results"] = results

        output = {"plan_id": plan_id, "results": results}
        validation = guardian.validate_output(output)
        if not validation["valid"]:
            return {"error": validation["reason"]}
        facts = memory_store.get_facts()

        return output

        opscaptain.log_event("plan_completed", {"plan_id": plan_id})

planner = Planner()
