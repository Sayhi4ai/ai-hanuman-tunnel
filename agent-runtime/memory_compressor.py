from vector_memory import recall, remember
from messaging import send_message

def cluster_memories(memories, cluster_size=5):
    clusters = []
    current = []

    for m in memories:
        current.append(m)
        if len(current) >= cluster_size:
            clusters.append(current)
            current = []

    if current:
        clusters.append(current)

    return clusters

def summarize_cluster(cluster):
    text = "\n".join(cluster)
    summary = send_message(
        "writer",
        f"Summarize and compress this memory cluster into one concise memory:\n{text}"
    )
    return summary

def compress_topic(topic):
    memories = recall(topic)
    if not memories:
        return None

    clusters = cluster_memories(memories)
    compressed = []

    for c in clusters:
        summary = summarize_cluster(c)
        compressed.append(summary)
        remember(f"compressed {topic}: {summary}")

    return compressed
