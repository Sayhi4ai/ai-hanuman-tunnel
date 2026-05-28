from graph import AGENT_REGISTRY
from messaging import send_message
from vector_memory import remember, recall

def debate_agent(state):
    topic = state.get("task", "")

    # Retrieve similar past debates
    related = recall(f"debate {topic}")

    # Step 1: Create two roles
    pro_role = f"Argue in favor of: {topic}"
    con_role = f"Argue against: {topic}"

    # Step 2: Ask writer to generate arguments
    pro_argument = send_message("writer", pro_role)
    con_argument = send_message("writer", con_role)

    # Step 3: Ask writer to summarize the debate
    summary = send_message(
        "writer",
        f"Summarize this debate:\n\nPRO:\n{pro_argument}\n\nCON:\n{con_argument}"
    )

    # Step 4: Store debate in vector memory
    remember(f"debate {topic}: PRO={pro_argument} CON={con_argument}")

    # Step 5: Build final output
    result = f"Debate on: {topic}\n\n"

    if related:
        result += "Relevant past debates:\n"
        for r in related:
            result += f"- {r}\n"
        result += "\n"

    result += (
        f"PRO Argument:\n{pro_argument}\n\n"
        f"CON Argument:\n{con_argument}\n\n"
        f"Summary:\n{summary}"
    )

    state["result"] = result
    state["history"].append("DEBATE_AGENT: debate completed")
    return state

def load():
    AGENT_REGISTRY["debate_agent"] = debate_agent
    return debate_agent
