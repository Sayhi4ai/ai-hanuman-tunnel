from graph import AGENT_REGISTRY
from messaging import send_message
from vector_memory import remember, recall

def reasoning_agent(state):
    task = state.get("task", "")

    # 1) Retrieve related memories
    related = recall(task)

    # 2) Ask writer to create a step-by-step plan
    plan_prompt = (
        "You are a careful reasoning engine.\n"
        "Given this problem, first outline a step-by-step plan to solve it:\n\n"
        f"Problem:\n{task}\n\n"
        f"Relevant past context:\n{related}\n\n"
        "Return ONLY the plan, as numbered steps."
    )
    plan = send_message("writer", plan_prompt)

    # 3) Ask writer to reason through the plan
    reasoning_prompt = (
        "Follow this plan and reason step by step.\n"
        "Show your reasoning clearly, but do NOT yet give the final answer.\n\n"
        f"Problem:\n{task}\n\n"
        f"Plan:\n{plan}\n"
    )
    reasoning = send_message("writer", reasoning_prompt)

    # 4) Ask writer to produce a final answer
    answer_prompt = (
        "Based on the reasoning below, produce the best final answer.\n"
        "Be concise, clear, and directly address the problem.\n\n"
        f"Problem:\n{task}\n\n"
        f"Reasoning:\n{reasoning}\n"
    )
    final_answer = send_message("writer", answer_prompt)

    # 5) Ask writer to self-critique and refine
    critique_prompt = (
        "Critique the following answer. Identify weaknesses, missing details, or errors.\n"
        "Then provide an improved final answer.\n\n"
        f"Problem:\n{task}\n\n"
        f"Initial answer:\n{final_answer}\n"
    )
    improved_answer = send_message("writer", critique_prompt)

    # 6) Store reasoning trace in memory
    remember(f"reasoning {task}: PLAN={plan} REASONING={reasoning} ANSWER={improved_answer}")

    # 7) Build result
    result = (
        f"Problem:\n{task}\n\n"
        f"Plan:\n{plan}\n\n"
        f"Reasoning:\n{reasoning}\n\n"
        f"Final Answer:\n{improved_answer}"
    )

    state["result"] = result
    state["history"].append("REASONING_AGENT: completed reasoning cycle")
    return state

def load():
    AGENT_REGISTRY["reasoning_agent"] = reasoning_agent
    return reasoning_agent
