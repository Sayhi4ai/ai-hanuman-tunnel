class Planner:
    def plan(self, goal: str, stage: str):
        if stage == "none":
            return ["Analyze the goal"]

        if stage == "analysis_complete":
            return ["Write a draft response"]

        if stage == "draft_complete":
            return ["Critique the draft"]

        if stage == "critique_complete":
            return ["Finalize the result"]
        if stage == "analysis_complete":
            return [
                "tool:web_fetch(url='https://example.com')",
                "Write a draft response"
            ]

        return ["Continue working toward the goal"]

planner = Planner()
