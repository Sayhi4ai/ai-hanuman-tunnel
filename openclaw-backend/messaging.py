import asyncio
from typing import Dict, Any, Callable, List
from app.integrations.opscaptain import opscaptain

class MessagingBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, handler: Callable):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(handler)
        opscaptain.log_event("agent_subscribed", {"topic": topic})

    async def publish(self, topic: str, message: Dict[str, Any]):
        opscaptain.log_event("agent_message", {"topic": topic, "message": message})

        if topic not in self.subscribers:
            return

        for handler in self.subscribers[topic]:
            async def safe_call(h=handler):
                try:
                    await h(message)
                except Exception as e:
                    opscaptain.log_event("agent_message_error", {
                        "topic": topic,
                        "error": str(e),
                        "message": message,
                    })
                return
            asyncio.create_task(safe_call())

messaging_bus = MessagingBus()
