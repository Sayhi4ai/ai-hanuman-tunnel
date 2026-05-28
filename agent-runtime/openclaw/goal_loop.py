from openclaw.planner import planner
from openclaw.executor import executor

class GoalLoop:
    def run(self, goal):
        results = []
        steps = planner.plan(goal, [])

        prev = ""

        for step in steps:
            out = executor.run_step("agent", step, previous_output=prev)
            results.append(out)
            prev = out

        return results

goal_loop = GoalLoop()
