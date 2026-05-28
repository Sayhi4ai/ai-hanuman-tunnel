import re

def reflect(output: str):
    # Remove ALL previous reflection tags
    clean = re.sub(r"

\[Reflection\]

", "", output)

    # Remove repeated reflection sentences
    clean = re.sub(
        r"I checked my answer\. Here is what I think:",
        "",
        clean,
        flags=re.IGNORECASE
    )

    # Trim whitespace
    clean = clean.strip()

    # Prevent runaway growth
    clean = clean[:200]

    return f"[Reflection] I checked my answer. Here is what I think: {clean}"
