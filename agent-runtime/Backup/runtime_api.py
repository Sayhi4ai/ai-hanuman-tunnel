from fastapi import FastAPI
from pydantic import BaseModel
from graph import app_graph, TASK_QUEUE, State
from logger import log
from graph import AGENT_REGISTRY

app = FastAPI(title="Agent Runtime")

import time
from collections import deque
import json
import time
import psutil
import time
import threading
import subprocess
SELFHEAL_ENABLED = True
SELFHEAL_LAST_ACTION = None

REQUEST_HISTORY = deque(maxlen=600)  # ~10 minutes at 1s resolution
EVENT_TIMELINE = deque(maxlen=500)   # system events (restarts, errors, spikes)

def get_runtime_state():
    with open("runtime_state.json", "r") as f:
        return json.load(f)

def set_runtime_state(state):
    with open("runtime_state.json", "w") as f:
        json.dump(state, f)

def get_runtime_state():
    with open("runtime_state.json", "r") as f:
        return json.load(f)

def set_runtime_state(state):
    with open("runtime_state.json", "w") as f:
        json.dump(state, f)

def openclaw_watchdog():
    global SELFHEAL_LAST_ACTION
    while True:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", "openclaw-gateway"],
                capture_output=True
            )
            status = result.stdout.decode().strip()

            if status != "active":
                EVENT_TIMELINE.append({
                    "timestamp": time.time(),
                    "type": "selfheal",
                    "detail": f"Gateway was '{status}', restarting"
                })
                subprocess.run(["sudo", "systemctl", "restart", "openclaw-gateway"])
                SELFHEAL_LAST_ACTION = f"Restarted at {time.strftime('%H:%M:%S')}"
        except Exception as e:
            SELFHEAL_LAST_ACTION = f"Error: {e}"
        time.sleep(30)

class TaskRequest(BaseModel):
    task: str

class AgentTask(BaseModel):
    task: str
    agent: str

@app.get("/")
async def root():
    return {"status": "agent-runtime-online"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/run")
async def run_task(req: TaskRequest):
    log("task_received", task=req.task)
    state: State = {"task": req.task, "history": [], "result": ""}
    result_state = app_graph.invoke(state)
    log("task_completed", result=result_state["result"])
    return {
        "task": req.task,
        "history": result_state["history"],
        "result": result_state["result"],
    }

@app.post("/run-agent")
async def run_agent(req: AgentTask):
    log("agent_task_received", task=req.task, agent=req.agent)
    state = {"task": req.task, "agent": req.agent, "history": [], "result": ""}
    result_state = app_graph.invoke(state)
    log("agent_task_completed", result=result_state["result"])
    return result_state

@app.post("/enqueue")
async def enqueue(req: TaskRequest):
    TASK_QUEUE.put(req.task)
    return {"status": "queued", "task": req.task}

@app.get("/gateway-info")
async def gateway_info():
    return {
        "name": "agent-runtime",
        "version": "1.0",
        "capabilities": ["planner", "worker", "validator", "governor"],
        "port": 7200,
        "status": "online"
    }

@app.get("/agents")
async def list_agents():
    return {"agents": list(AGENT_REGISTRY.keys())}

@app.get("/system/mode")
def get_mode():
    return get_runtime_state()

@app.post("/system/mode")
def set_mode(data: dict):
    state = get_runtime_state()
    state["turbo_mode"] = data.get("turbo_mode", False)
    set_runtime_state(state)
    return state

@app.get("/system/turbo-status")
def turbo_status():
    state = get_runtime_state()
    return {
        "turbo_mode": state["turbo_mode"],
        "activated_at": state.get("turbo_activated_at", None),
        "auto_triggered": state.get("auto_triggered", False)
    }

@app.get("/system/turbo-logs")
def turbo_logs():
    try:
        with open("turbo.log", "r") as f:
            return {"logs": f.read().splitlines()}
    except:
        return {"logs": []}

@app.post("/system/auto-turbo")
def auto_turbo(data: dict):
    state = get_runtime_state()
    state["turbo_mode"] = True
    state["auto_triggered"] = True
    state["turbo_activated_at"] = time.time()
    set_runtime_state(state)

    with open("turbo.log", "a") as f:
        f.write(f"AUTO TURBO ACTIVATED at {time.time()}\n")

    return state

@app.get("/system/openclaw-logs")
def openclaw_logs():
    try:
        with open("/var/log/syslog", "r") as f:
            lines = [l for l in f.readlines() if "openclaw" in l.lower()]
        return {"logs": lines[-200:]}
    except:
        return {"logs": []}

@app.get("/system/openclaw-health")
def openclaw_health():
    import subprocess
    result = subprocess.run(["systemctl", "is-active", "openclaw-gateway"], capture_output=True)
    status = result.stdout.decode().strip()
    return {"status": status}

@app.post("/system/openclaw-restart")
def restart_openclaw():
    import subprocess
    subprocess.run(["sudo", "systemctl", "restart", "openclaw-gateway"])
    return {"status": "restarted"}

@app.get("/system/openclaw-version")
def openclaw_version():
    import subprocess
    result = subprocess.run(["openclaw", "--version"], capture_output=True)
    return {"version": result.stdout.decode().strip()}

@app.post("/system/openclaw-upgrade")
def openclaw_upgrade():
    import subprocess
    result = subprocess.run(["openclaw", "update"], capture_output=True)
    return {"output": result.stdout.decode().splitlines()}

# Track crashes in memory
CRASH_LOG = []

@app.get("/system/openclaw-stats")
def openclaw_stats():
    # CPU and RAM
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent

    # Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    # Crash heatmap (last 24 hours)
    now = time.time()
    last_24h = [t for t in CRASH_LOG if now - t < 86400]

    return {
        "cpu": cpu,
        "ram": ram,
        "uptime_seconds": uptime_seconds,
        "crashes_last_24h": len(last_24h),
        "crash_timestamps": last_24h
    }

# Hook into restart endpoint to track crashes
@app.post("/system/openclaw-restart")
def restart_openclaw():
    import subprocess
    EVENT_TIMELINE.append({
        "timestamp": time.time(),
        "type": "restart",
        "detail": "OpenClaw gateway restart requested"
    })
    subprocess.run(["sudo", "systemctl", "restart", "openclaw-gateway"])
    return {"status": "restarted"}

REQUEST_HISTORY = deque(maxlen=300)  # 5 minutes at 1-second resolution

@app.middleware("http")
async def track_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    REQUEST_HISTORY.append({
        "timestamp": time.time(),
        "status": response.status_code,
        "duration": duration
    })

    return response

@app.get("/system/openclaw-rps")
def openclaw_rps():
    now = time.time()
    last_60 = [r for r in REQUEST_HISTORY if now - r["timestamp"] <= 60]

    total = len(last_60)
    errors = len([r for r in last_60 if r["status"] >= 400])
    rps = total / 60

    return {
        "rps": rps,
        "total_requests": total,
        "errors": errors,
        "error_rate": (errors / total * 100) if total > 0 else 0,
        "history": list(last_60)
    }

@app.get("/system/metrics")
def system_metrics():
    import psutil, time
    return {
        "cpu": psutil.cpu_percent(interval=0.2),
        "ram": psutil.virtual_memory().percent,
        "timestamp": time.time()
    }

@app.middleware("http")
async def track_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    entry = {
        "timestamp": time.time(),
        "status": response.status_code,
        "duration": duration,
        "path": request.url.path
    }
    REQUEST_HISTORY.append(entry)

    if response.status_code >= 500:
        EVENT_TIMELINE.append({
            "timestamp": time.time(),
            "type": "error",
            "detail": f"{response.status_code} {request.url.path}"
        })

    return response

@app.get("/system/openclaw-rps")
def openclaw_rps():
    now = time.time()
    last_60 = [r for r in REQUEST_HISTORY if now - r["timestamp"] <= 60]

    total = len(last_60)
    errors = len([r for r in last_60 if r["status"] >= 400])
    rps = total / 60 if total > 0 else 0

    durations = sorted([r["duration"] for r in last_60]) or [0]
    def percentile(p):
        if not durations:
            return 0
        idx = int(len(durations) * p)
        idx = min(max(idx, 0), len(durations) - 1)
        return durations[idx]

    return {
        "rps": rps,
        "total_requests": total,
        "errors": errors,
        "error_rate": (errors / total * 100) if total > 0 else 0,
        "p50": percentile(0.5),
        "p90": percentile(0.9),
        "p99": percentile(0.99),
        "history": last_60,
    }

@app.get("/system/openclaw-timeline")
def openclaw_timeline():
    return {"events": list(EVENT_TIMELINE)}

@app.get("/system/agent-metrics")
def agent_metrics():
    now = time.time()
    last_300 = [r for r in REQUEST_HISTORY if now - r["timestamp"] <= 300]

    agents = {}
    for r in last_300:
        name = r["path"]
        if name not in agents:
            agents[name] = {"calls": 0, "errors": 0, "total_duration": 0.0}
        agents[name]["calls"] += 1
        agents[name]["total_duration"] += r["duration"]
        if r["status"] >= 400:
            agents[name]["errors"] += 1

    result = []
    for name, stats in agents.items():
        calls = stats["calls"]
        avg = stats["total_duration"] / calls if calls else 0
        err_rate = (stats["errors"] / calls * 100) if calls else 0
        result.append({
            "agent": name,
            "calls": calls,
            "avg_duration": avg,
            "error_rate": err_rate,
        })

    return {"agents": result}

@app.get("/system/agent-call-graph")
def agent_call_graph():
    # Static example; you can later wire real edges
    nodes = [
        {"id": "planner"},
        {"id": "web_search"},
        {"id": "browser"},
        {"id": "writer"},
        {"id": "runtime"},
    ]
    links = [
        {"source": "planner", "target": "web_search"},
        {"source": "planner", "target": "browser"},
        {"source": "planner", "target": "writer"},
        {"source": "writer", "target": "runtime"},
    ]
    return {"nodes": nodes, "links": links}

@app.get("/system/openclaw-selfheal")
def openclaw_selfheal_status():
    return {
        "enabled": SELFHEAL_ENABLED,
        "last_action": SELFHEAL_LAST_ACTION,
    }
