import time
from agent_factory import create_agent
from vector_memory import remember, recall
from messaging import send_message

def generate_swarm_agent_description(parent, role):
    return send_message(
        "writer",
        f"Create a description for a swarm agent derived from '{parent}' "
        f"with the specialized role: {role}."
    )

def create_swarm_agent(parent, role):
    description = generate_swarm_agent_description(parent, role)
    name = f"{parent}_swarm_{role}_{int(time.time())}"
    filename, code = create_agent(name, description)
    remember(f"swarm_agent_created: {name}")
    return name, filename, code

def create_swarm(parent, roles):
    swarm = []
    for role in roles:
        agent_name, filename, code = create_swarm_agent(parent, role)
        swarm.append(agent_name)
    remember(f"swarm_created: {parent} -> {swarm}")
    return swarm

def dissolve_swarm(parent):
    memories = recall("swarm_created")
    dissolved = []
    for m in memories:
        if parent in m:
            dissolved.append(m)
            remember(f"swarm_dissolved: {m}")
    return dissolved
