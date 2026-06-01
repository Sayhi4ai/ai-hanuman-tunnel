import inspect
from messaging import send_message
from agent_factory import create_agent
from vector_memory import remember

DANGEROUS_PATTERNS = [
    "os.system",
    "subprocess",
    "eval(",
    "exec(",
    "open(",
    "requests.get",
    "requests.post",
    "import socket",
    "import telnetlib",
]

def scan_code_for_patterns(code):
    found = []
    for pattern in DANGEROUS_PATTERNS:
        if pattern in code:
            found.append(pattern)
    return found

def llm_security_review(agent_name, code):
    return send_message(
        "writer",
        f"Perform a security audit of this agent's code. "
        f"Identify vulnerabilities, unsafe patterns, injection risks, and missing validation:\n\n{code}"
    )

def propose_security_fixes(agent_name, vulnerabilities):
    return send_message(
        "writer",
        f"Propose secure code improvements for agent '{agent_name}'. "
        f"Fix vulnerabilities and rewrite unsafe sections:\n\n{vulnerabilities}"
    )

def auto_patch_agent(agent_name, fixes):
    new_name = f"{agent_name}_secure"
    filename, code = create_agent(new_name, f"Secure version of {agent_name}:\n{fixes}")
    remember(f"security_patch {agent_name} -> {new_name}")
    return new_name, filename, code

def run_security_scan(agent_name, agent_fn):
    code = inspect.getsource(agent_fn)

    pattern_hits = scan_code_for_patterns(code)
    llm_review = llm_security_review(agent_name, code)

    fixes = propose_security_fixes(agent_name, llm_review)

    return {
        "agent": agent_name,
        "patterns": pattern_hits,
        "llm_review": llm_review,
        "fixes": fixes,
    }
