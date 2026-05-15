import asyncio
from typing import Dict, Any
from tenacity import retry, stop_after_attempt, wait_fixed
from .tools import handle_tool

class RuntimeEngine:
    def __init__(self, worker_count: int = 4):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.worker_count = worker_count
        self.workers = []
        self.results: Dict[str, Any] = {}
        self.task_counter = 0

    async def start(self):
        for i in range(self.worker_count):
            worker = asyncio.create_task(self.worker_loop(i))
            self.workers.append(worker)
        print(f"[Runtime] Started {self.worker_count} workers")

    async def stop(self):
        for _ in self.workers:
            await self.queue.put(None)
        await asyncio.gather(*self.workers)
        print("[Runtime] Stopped workers")

    async def submit(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.task_counter += 1
        task_id = f"task-{self.task_counter}"
        await self.queue.put({"id": task_id, "payload": payload})
        return {"task_id": task_id, "status": "queued"}

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        return await handle_tool(task["payload"])

    async def worker_loop(self, worker_id: int):
        print(f"[Runtime] Worker {worker_id} started")
        while True:
            item = await self.queue.get()
            if item is None:
                break

            task_id = item["id"]
            payload = item["payload"]
            print(f"[Runtime] Worker {worker_id} processing {task_id}: {payload}")

            try:
                result = await self.process_task(item)
                self.results[task_id] = {"status": "done", "result": result}
            except Exception as e:
                self.results[task_id] = {"status": "error", "error": str(e)}

            self.queue.task_done()

runtime_engine = RuntimeEngine()
