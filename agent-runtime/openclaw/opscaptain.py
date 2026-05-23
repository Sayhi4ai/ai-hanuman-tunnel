import uuid
from openclaw.tool_registry import TOOLS

class OpsCaptain:
    def __init__(self):
        self.sessions = {}

    def start_task(self, goal: str):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "goal": goal,
            "steps": [],
            "results": []
        }
        return session_id

    def add_step(self, session_id: str, agent: str, instruction: str):
        step = {
            "agent": agent,
            "instruction": instruction
        }
        self.sessions[session_id]["steps"].append(step)
        return step

    def record_result(self, session_id: str, result: str):
        self.sessions[session_id]["results"].append(result)

    def summarize(self, session_id: str):
        results = self.sessions[session_id]["results"]
        return "\n".join(results)

    def route_step(self, session_id: str, instruction: str):
        if "analyze" in instruction.lower():
            agent = "analyst"
        elif "critique" in instruction.lower():
            agent = "critic"
        else:
            agent = "assistant"

        return self.add_step(session_id, agent, instruction)

    def detect_failure(self, session_id: str):
        results = self.sessions[session_id]["results"]
        if not results:
            return False

        last = results[-1].lower()

        if "error" in last or "failed" in last or "unable" in last:
            return True

        return False

    def recover(self, session_id: str):
        # If analysis failed → retry with analyst
        return self.add_step(session_id, "analyst", "Retry the previous step with more detail")

    def detect_stage(self, session_id: str):
        results = self.sessions[session_id]["results"]
        if not results:
            return "none"

        last = results[-1].lower()

        if "analysis" in last:
            return "analysis_complete"

        if "draft" in last:
            return "draft_complete"

        if "critique" in last:
            return "critique_complete"

            return "unknown"

opscaptain = OpsCaptain()
