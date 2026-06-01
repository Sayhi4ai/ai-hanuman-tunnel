from graph import AGENT_REGISTRY
from chaos_engine import run_chaos_test
from task_queue import enqueue

def chaos_agent(state):
    task = state.get("task", "").strip()

    name, result = run_chaos_test()

    # Schedule healing or security tasks
    enqueue("Run full registry healing", "registry_healer_agent", priority=10)
    enqueue("Run full security scan", "security_agent", priority=9)

    state["result"] = (
        f"Chaos test executed.\n\n"
        f"Event type: {name}\n"
        f"Result: {result}\n\n"
        f"Healing and security tasks have been scheduled."
    )

    state["history"].append("CHAOS_AGENT: chaos test executed")
    return state

def load():
    AGENT_REGISTRY["chaos_agent"] = chaos_agent
    return chaos_agent
