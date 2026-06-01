from graph import AGENT_REGISTRY
from memory_compressor import compress_topic
from vector_memory import recall

def memory_compression_agent(state):
    topic = state.get("task", "")

    if not topic:
        state["result"] = "Usage: <topic> (compress memories for this topic)"
        return state

    before = recall(topic)
    compressed = compress_topic(topic)
    after = recall(f"compressed {topic}")

    result = (
        f"Memory compression complete for topic: {topic}\n\n"
        f"Original entries: {len(before)}\n"
        f"Compressed entries: {len(after)}\n\n"
        f"Compressed summaries:\n"
    )

    for c in after:
        result += f"- {c}\n"

    state["result"] = result
    state["history"].append("MEMORY_COMPRESSION: completed")
    return state

def load():
    AGENT_REGISTRY["memory_compression_agent"] = memory_compression_agent
    return memory_compression_agent
