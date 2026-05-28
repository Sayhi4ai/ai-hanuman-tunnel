from openclaw import memory

class Planner:
    def plan(self, goal: str, stage: str):
        if stage == "none":
            return ["Analyze the goal"]

        if stage == "analysis_complete":
            return ["Draft a response"]

        if stage == "draft_complete":
            return ["Reflect on the draft"]

        if stage == "reflection_complete":
            return ["Improve the draft"]

        if stage == "improvement_complete":
            return ["Finalize the result"]

        # final or unknown → stop
        return []

planner = Planner()
