import time
from vector_memory import remember, recall
from messaging import send_message
from agent_factory import create_agent
from graph import AGENT_REGISTRY
from runtime_api import get_runtime_state   # <-- already correct import

def record_agent_usage(agent_name, duration):
    remember(f"agent_usage: {agent_name} took {duration} seconds")

def get_agent_load(agent_name):
    usage = recall("agent_usage")
    relevant = [u for u in usage if agent_name in u]
    if not relevant:
        return 0
    return sum(float(x.split("took ")[1].split(" ")[0]) for x in relevant[-10:]) / len(relevant[-10:])

def propose_alternative_agents(task):
    return send_message(
        "writer",
        f"Given this task, propose 3 alternative agents that could handle it:\n{task}"
    )

def spawn_specialist(task):
    description = send_message(
        "writer",
        f"Create a description for a new specialist agent optimized for this task:\n{task}"
    )
    name = f"specialist_{int(time.time())}"
    filename, code = create_agent(name, description)
    return name, filename, code

def choose_best_agent(task):
    # -------------------------------
    # 🔥 TURBO MODE FILTERING
    # -------------------------------
    state = get_runtime_state()

    if state.get("turbo_mode"):
        core_agents = [
            "planner",
            "backup_writer",
            "reasoning_agent",
            "browser",
            "filereader",
            "queue_manager",
            "queue_worker",
            "manager_agent",
            "supervisor"
        ]

        # Filter AGENT_REGISTRY to only core agents
        filtered_registry = {
            name: agent
            for name, agent in AGENT_REGISTRY.items()
            if name in core_agents
        }
    else:
        # Normal mode → use all agents
        filtered_registry = AGENT_REGISTRY
    # -------------------------------
    # 🔥 END TURBO MODE FILTERING
    # -------------------------------

    # Now compute loads ONLY on allowed agents
    loads = {name: get_agent_load(name) for name in filtered_registry.keys()}
    sorted_agents = sorted(loads.items(), key=lambda x: x[1])
    return sorted_agents[0][0], loads
