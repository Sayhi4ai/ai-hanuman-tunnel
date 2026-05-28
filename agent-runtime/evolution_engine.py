import random
import traceback
from messaging import send_message
from vector_memory import remember

def mutate_code(code):
    lines = code.split("\n")
    if len(lines) < 2:
        return code

    # Random mutation: reorder, remove, or duplicate a line
    mutation_type = random.choice(["swap", "remove", "duplicate"])

    if mutation_type == "swap" and len(lines) > 3:
        i, j = random.sample(range(len(lines)), 2)
        lines[i], lines[j] = lines[j], lines[i]

    elif mutation_type == "remove" and len(lines) > 3:
        idx = random.randint(0, len(lines)-1)
        lines.pop(idx)

    elif mutation_type == "duplicate":
        idx = random.randint(0, len(lines)-1)
        lines.insert(idx, lines[idx])

    return "\n".join(lines)

def evaluate_variant(agent_name, code, test_input):
    try:
        # Ask coder to execute the code
        result = send_message("coder", f"Execute this code:\n{code}\n\nTest with: {test_input}")
        return 1.0  # If no error, good score
    except Exception:
        return 0.0  # Failed variant

def evolve_agent(agent_name, original_code, test_input, generations=5, population=4):
    best_code = original_code
    best_score = 0

    for gen in range(generations):
        variants = [best_code] + [mutate_code(best_code) for _ in range(population)]

        scored = []
        for v in variants:
            score = evaluate_variant(agent_name, v, test_input)
            scored.append((score, v))

        scored.sort(reverse=True, key=lambda x: x[0])
        best_score, best_code = scored[0]

        remember(f"evolution {agent_name}: gen {gen} score {best_score}")

    return best_code, best_score
