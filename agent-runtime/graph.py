from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
import json
import importlib
import os
from queue import Queue
import threading

# ---------- LLM BASE ----------
llm = ChatOllama(
    model="gemma4:latest",
    base_url="http://127.0.0.1:11434",
)

# ---------- STATE ----------
class State(TypedDict):
    task: str
    history: List[str]
    result: str

# ---------- DYNAMIC AGENT SPAWNING ----------
def spawn_agent(role: str, instructions: str):
    return ChatOllama(
        model="gemma4:latest",
        base_url="http://127.0.0.1:11434",
        system=f"You are a {role}. {instructions}",
    )

# ---------- TOOLS ----------
TOOLS = {}

def tool(name):
    def decorator(func):
        TOOLS[name] = func
        return func
    return decorator

@tool("list_files")
def list_files(path: str = "."):
    return os.listdir(path)

# ---------- MEMORY ----------
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(mem):
    with open(MEMORY_FILE, "w") as f:
        json.dump(mem, f, indent=2)

MEMORY = load_memory()

# ---------- ISOLATION CONTEXT ----------
class AgentContext:
    def __init__(self):
        self.history: List[str] = []
        self.memory: dict = {}

# ---------- TASK QUEUE ----------
TASK_QUEUE: Queue = Queue()

def queue_worker():
    from graph import app_graph  # late import to avoid circular
    while True:
        task = TASK_QUEUE.get()
        state: State = {"task": task, "history": [], "result": ""}
        app_graph.invoke(state)

threading.Thread(target=queue_worker, daemon=True).start()

# ---------- NODES ----------
def planner(state: State) -> State:
    MEMORY["last_task"] = state["task"]
    save_memory(MEMORY)
    plan = llm.invoke(f"Break this task into clear steps:\n{state['task']}")
    state["history"].append(f"PLAN: {plan.content}")
    return state

def worker(state: State) -> State:
    # optional tool usage if planner encoded it in state
    if "use_tool" in state:
        tool_name = state["use_tool"]["name"]
        args = state["use_tool"].get("args", {})
        if tool_name in TOOLS:
            result = TOOLS[tool_name](**args)
            state["history"].append(f"TOOL({tool_name}): {result}")
    if "agent" in state:
        agent_name = state["agent"]
        if agent_name in AGENT_REGISTRY:
            agent = AGENT_REGISTRY[agent_name]
            work = agent.invoke(state["task"])
            state["history"].append(f"AGENT({agent_name}): {work.content}")
            state["result"] = work.content
            return state

    work = llm.invoke(f"Execute the next step based on history:\n{state['history']}")
    state["history"].append(f"WORK: {work.content}")
    state["result"] = work.content
    return state

def validator(state: State) -> State:
    review = llm.invoke(
        f"Validate the result for correctness and completeness:\n{state['result']}"
    )
    state["history"].append(f"VALIDATOR: {review.content}")
    return state

def governor(state: State) -> State:
    review = llm.invoke(
        f"Review the entire history and enforce safety and coherence:\n{state['history']}"
    )
    state["history"].append(f"GOVERNOR: {review.content}")
    return state

AGENT_REGISTRY = {}

def load_agents():
    agents_dir = os.path.join(os.path.dirname(__file__), "agents")
    for file in os.listdir(agents_dir):
        if file.endswith(".py"):
            name = file[:-3]
            module = importlib.import_module(f"agents.{name}")
            AGENT_REGISTRY[name] = module.load()

load_agents()
# ---------- GRAPH ----------
graph = StateGraph(State)
graph.add_node("planner", planner)
graph.add_node("worker", worker)
graph.add_node("validator", validator)
graph.add_node("governor", governor)

graph.set_entry_point("planner")
graph.add_edge("planner", "worker")
graph.add_edge("worker", "validator")
graph.add_edge("validator", "governor")
graph.add_edge("governor", END)

app_graph = graph.compile()
