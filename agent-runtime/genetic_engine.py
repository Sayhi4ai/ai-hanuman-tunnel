import inspect
import random
from messaging import send_message
from agent_factory import create_agent
from vector_memory import remember

def mutate_code(code):
    prompt = (
        "Mutate this agent code. Apply small, meaningful changes that preserve functionality "
        "but alter behavior slightly. Do NOT break syntax.\n\n"
        f"{code}"
    )
    return send_message("writer", prompt)

def crossover_code(code_a, code_b):
    prompt = (
        "Perform genetic crossover between these two agent implementations. "
        "Combine their strengths into a new hybrid agent. Ensure valid Python.\n\n"
        f"Parent A:\n{code_a}\n\n"
        f"Parent B:\n{code_b}"
    )
    return send_message("writer", prompt)

def score_fitness(agent_name, agent_fn):
    code = inspect.getsource(agent_fn)
    prompt = (
        "Evaluate the fitness of this agent. Consider clarity, robustness, safety, "
        "efficiency, and usefulness. Return a numeric score from 0 to 100.\n\n"
        f"{code}"
    )
    score = send_message("writer", prompt)
    try:
        return float(score.strip())
    except:
        return random.uniform(40, 60)

def evolve_agents(parent_a, parent_b, agent_fn_a, agent_fn_b):
    code_a = inspect.getsource(agent_fn_a)
    code_b = inspect.getsource(agent_fn_b)

    mutated_a = mutate_code(code_a)
    mutated_b = mutate_code(code_b)
    hybrid = crossover_code(code_a, code_b)

    candidates = {
        "mutated_a": mutated_a,
        "mutated_b": mutated_b,
        "hybrid": hybrid,
    }

    fitness_scores = {}
    for name, code in candidates.items():
        new_agent_name = f"{parent_a}_{parent_b}_{name}"
        filename, _ = create_agent(new_agent_name, f"Evolved variant: {name}")
        fitness_scores[name] = score_fitness(new_agent_name, agent_fn_a)

    best_variant = max(fitness_scores, key=fitness_scores.get)
    remember(f"genetic_evolution: {parent_a},{parent_b} -> {best_variant}")

    return best_variant, fitness_scores
