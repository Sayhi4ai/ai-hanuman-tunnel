import asyncio
from typing import Dict, Any
import uuid
from app.integrations.opscaptain import opscaptain
from app.core.messaging import messaging_bus
from app.core.knowledge_graph import knowledge_graph

class AgentSpawner:
    def __init__(self):
        self.running_agents: Dict[str, Dict[str, Any]] = {}

    async def spawn_agent(self, metadata: dict) -> dict:
        agent_id = f"agent-{uuid.uuid4().hex[:8]}"

        # Create an async task to simulate agent execution
        task = asyncio.create_task(self.agent_loop(agent_id, metadata))

        self.running_agents[agent_id] = {
            "metadata": metadata,
            "task": task,
            "status": "running"
        }

        return {"agent_id": agent_id, "status": "spawned"}

        opscaptain.log_event("agent_spawned", {"agent_id": agent_id, "metadata": metadata})

    async def agent_loop(self, agent_id: str, metadata: dict):
        """
        A long-running agent loop.
        In a real system, this would connect to agent-runtime.
        """
        while True:
            print(f"[Spawner] Agent {agent_id} alive with metadata: {metadata}")
            await asyncio.sleep(2)
            opscaptain.log_event("agent_heartbeat", {"agent_id": agent_id})
        if metadata.get("role") == "browser-agent":
            await browser_agent.start()
	async def on_message(message):
	    try:
	        print(f"[Agent {agent_id}] received message: {message}")

	        # Optional: store raw message in memory
	        memory_store.add_task({
	            "agent_id": agent_id,
	            "type": "message",
	            "content": message,
	        })

	        # Async learning hook
	        learn = message.get("learn")
	        if isinstance(learn, dict):
	            node_id = learn.get("id")
	            if node_id:
	                knowledge_graph.add_node(node_id, learn.get("properties", {}))

	        # Self-reflection hook (see next section)
	        reflection = message.get("reflection")
	        if isinstance(reflection, dict):
	            node_id = reflection.get("id", f"reflection-{agent_id}")
	            knowledge_graph.add_node(node_id, reflection)

	    except Exception as e:
	        print(f"[Agent {agent_id}] error handling message: {e}")
        if "learn" in message:
            knowledge_graph.add_node(message["learn"]["id"], message["learn"].get("properties", {}))

        messaging_bus.subscribe(agent_id, on_message)

    async def list_running_agents(self):
        return {
            agent_id: {
                "metadata": info["metadata"],
                "status": info["status"]
            }
            for agent_id, info in self.running_agents.items()
        }

spawner = AgentSpawner()
