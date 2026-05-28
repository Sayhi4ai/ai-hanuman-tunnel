import time
from graph import AGENT_REGISTRY

def run_loop(agent_name, task, interval=10):
    print(f"[LOOP] Starting autonomous loop for agent '{agent_name}' every {interval}s")
    agent_fn = AGENT_REGISTRY.get(agent_name)

    if not agent_fn:
        print(f"[LOOP] Agent '{agent_name}' not found")
        return

    while True:
        try:
            state = {"task": task, "history": [], "result": ""}
            result_state = agent_fn(state)

            print("\n[LOOP RESULT]")
            print(result_state["result"])
            print("[END RESULT]\n")

        except Exception as e:
            print(f"[LOOP ERROR] {e}")

        time.sleep(interval)
