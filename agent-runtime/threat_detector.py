import inspect
from vector_memory import recall, remember
from messaging import send_message
from task_queue import list_tasks
from graph import AGENT_REGISTRY

SUSPICIOUS_PATTERNS = [
    "delete",
    "rm -rf",
    "DROP TABLE",
    "shutdown",
    "format disk",
    "sudo",
    "chmod 777",
    "curl http",
    "wget http",
    "import socket",
    "import telnetlib",
    "eval(",
    "exec(",
]

def detect_suspicious_code(agent_name, agent_fn):
    code = inspect.getsource(agent_fn)
    hits = [p for p in SUSPICIOUS_PATTERNS if p in code]
    return code, hits

def detect_suspicious_memory():
    memories = recall("memory")
    suspicious = [m for m in memories if any(p in m.lower() for p in ["hack", "attack", "exploit", "breach"])]
    return suspicious

def detect_queue_anomalies():
    tasks = list_tasks()
    anomalies = [t for t in tasks if "delete" in t["task"].lower() or "shutdown" in t["task"].lower()]
    return anomalies

def llm_threat_assessment(agent_name, code, memory_hits, queue_hits):
    prompt = (
        "Perform a security threat assessment.\n"
        "Identify malicious intent, injection attempts, or dangerous behavior.\n\n"
        f"Agent: {agent_name}\n\n"
        f"Code:\n{code}\n\n"
        f"Suspicious memory entries:\n{memory_hits}\n\n"
        f"Suspicious queue tasks:\n{queue_hits}\n"
    )
    return send_message("writer", prompt)

def detect_threats(agent_name, agent_fn):
    code, code_hits = detect_suspicious_code(agent_name, agent_fn)
    memory_hits = detect_suspicious_memory()
    queue_hits = detect_queue_anomalies()

    llm_assessment = llm_threat_assessment(agent_name, code, memory_hits, queue_hits)

    return {
        "agent": agent_name,
        "code_hits": code_hits,
        "memory_hits": memory_hits,
        "queue_hits": queue_hits,
        "llm_assessment": llm_assessment,
    }
