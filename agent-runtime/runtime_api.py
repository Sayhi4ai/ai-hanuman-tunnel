from fastapi import FastAPI
from pydantic import BaseModel
from graph import app_graph, TASK_QUEUE, State
from logger import log
from graph import AGENT_REGISTRY

app = FastAPI(title="Agent Runtime")

import time
from collections import deque
import json
import psutil
import threading
import subprocess
import requests

# -------------------------
# GLOBALS
# -------------------------
SELFHEAL_ENABLED = True
SELFHEAL_LAST_ACTION = None

REQUEST_HISTORY = deque(maxlen=600)
EVENT_TIMELINE = deque(maxlen=500)
CRASH_LOG = []

CLUSTER_NODES = [
    {"id": "runtime-1", "host": "127.0.0.1", "port": 7200, "role": "primary"},
    {"id": "runtime-2", "host": "127.0.0.1", "port": 7201, "role": "secondary"},
    {"id": "runtime-3", "host": "127.0.0.1", "port": 7202, "role": "worker"},
]

# -------------------------
# RUNTIME STATE HELPERS
# -------------------------
def get_runtime_state():
    with open("runtime_state.json", "r") as f:
        return json.load(f)

def set_runtime_state(state):
    with open("runtime_state.json", "w") as f:
        json.dump(state, f)

PLANNER_STATS = {
    "auto_turbo_activations": 0,
    "last_auto_turbo_at": None,
    "agents": {}  # per-path stats
}

def maybe_auto_turbo(agent_name: str):
    now = time.time()
    last_180 = [r for r in REQUEST_HISTORY if now - r["timestamp"] <= 180 and r.get("path") == agent_name]

    if not last_180:
        return

    total = len(last_180)
    errors = len([r for r in last_180 if r["status"] >= 400])
    durations = [r["duration"] for r in last_180]

    error_rate = (errors / total * 100) if total > 0 else 0
    avg_ms = (sum(durations) / total) * 1000

    # record per-agent stats
    PLANNER_STATS["agents"].setdefault(agent_name, {})
    PLANNER_STATS["agents"][agent_name].update({
        "calls": total,
        "error_rate": error_rate,
        "avg_ms": avg_ms,
        "last_checked": now,
    })

    # heuristic: this agent's traffic looks bad → suggest turbo
    if error_rate > 15 or avg_ms > 1500:
        state = get_runtime_state()
        if not state.get("turbo_mode", False):
            state["turbo_mode"] = True
            state["auto_triggered"] = True
            state["turbo_activated_at"] = now
            set_runtime_state(state)

            PLANNER_STATS["auto_turbo_activations"] += 1
            PLANNER_STATS["last_auto_turbo_at"] = now
            PLANNER_STATS["agents"][agent_name]["last_auto_turbo"] = now

            EVENT_TIMELINE.append({
                "timestamp": now,
                "type": "planner-auto-turbo",
                "detail": f"auto turbo enabled for path={agent_name} (error_rate={error_rate:.1f}%, avg_ms={avg_ms:.1f})"
            })

# -------------------------
# WATCHDOG (SELF-HEAL)
# -------------------------
def runtime_watchdog():
    while True:
        try:
            health = runtime_health()
            if health["health_score"] < 40:
                EVENT_TIMELINE.append({
                    "timestamp": time.time(),
                    "type": "runtime-selfheal",
                    "detail": f"Runtime unhealthy (score={health['health_score']}), restarting"
                })
                subprocess.run(["sudo", "systemctl", "restart", "agent-runtime"])
        except Exception as e:
            EVENT_TIMELINE.append({
                "timestamp": time.time(),
                "type": "runtime-selfheal-error",
                "detail": str(e)
            })
        time.sleep(20)

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

# -------------------------
# MODELS
# -------------------------
class TaskRequest(BaseModel):
    task: str

class AgentTask(BaseModel):
    task: str
    agent: str

# -------------------------
# BASIC ENDPOINTS
# -------------------------
@app.get("/")
async def root():
    return {"status": "agent-runtime-online"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# -------------------------
# TASK EXECUTION
# -------------------------
@app.post("/run")
async def run_task(req: TaskRequest):
    maybe_auto_turbo("/run")
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
    maybe_auto_turbo("/run-agent")
    log("agent_task_received", task=req.task, agent=req.agent)
    state = {"task": req.task, "agent": req.agent, "history": [], "result": ""}
    result_state = app_graph.invoke(state)
    log("agent_task_completed", result=result_state["result"])
    return result_state

@app.post("/enqueue")
async def enqueue(req: TaskRequest):
    TASK_QUEUE.put(req.task)
    return {"status": "queued", "task": req.task}

# -------------------------
# SYSTEM INFO
# -------------------------
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

# -------------------------
# TURBO MODE
# -------------------------
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

# -------------------------
# OPENCLAW SYSTEM ENDPOINTS
# -------------------------
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
    result = subprocess.run(["systemctl", "is-active", "openclaw-gateway"], capture_output=True)
    return {"status": result.stdout.decode().strip()}

@app.post("/system/openclaw-restart")
def restart_openclaw():
    EVENT_TIMELINE.append({
        "timestamp": time.time(),
        "type": "restart",
        "detail": "OpenClaw gateway restart requested"
    })
    subprocess.run(["sudo", "systemctl", "restart", "openclaw-gateway"])
    return {"status": "restarted"}

@app.get("/system/openclaw-version")
def openclaw_version():
    result = subprocess.run(["openclaw", "--version"], capture_output=True)
    return {"version": result.stdout.decode().strip()}

@app.post("/system/openclaw-upgrade")
def openclaw_upgrade():
    result = subprocess.run(["openclaw", "update"], capture_output=True)
    return {"output": result.stdout.decode().splitlines()}

@app.get("/system/planner-stats")
def planner_stats():
    state = get_runtime_state()
    return {
        "turbo_mode": state.get("turbo_mode", False),
        "auto_triggered": state.get("auto_triggered", False),
        "turbo_activated_at": state.get("turbo_activated_at", None),
        "auto_turbo_activations": PLANNER_STATS["auto_turbo_activations"],
        "last_auto_turbo_at": PLANNER_STATS["last_auto_turbo_at"],
    }

@app.get("/system/planner-brain")
def planner_brain():
    state = get_runtime_state()
    return {
        "turbo_mode": state.get("turbo_mode", False),
        "auto_triggered": state.get("auto_triggered", False),
        "turbo_activated_at": state.get("turbo_activated_at", None),
        "auto_turbo_activations": PLANNER_STATS["auto_turbo_activations"],
        "last_auto_turbo_at": PLANNER_STATS["last_auto_turbo_at"],
        "agents": PLANNER_STATS["agents"],
    }

# -------------------------
# METRICS
# -------------------------
@app.get("/system/openclaw-stats")
def openclaw_stats():
    cpu = psutil.cpu_percent(interval=0.2)
    ram = psutil.virtual_memory().percent
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    now = time.time()
    last_24h = [t for t in CRASH_LOG if now - t < 86400]

    return {
        "cpu": cpu,
        "ram": ram,
        "uptime_seconds": uptime_seconds,
        "crashes_last_24h": len(last_24h),
        "crash_timestamps": last_24h
    }

# -------------------------
# REQUEST TRACKING (ONE COPY ONLY)
# -------------------------
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

@app.get("/system/agent-health")
def agent_health():
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
        if calls == 0:
            score = 100
        else:
            avg_ms = (stats["total_duration"] / calls) * 1000
            err_rate = stats["errors"] / calls * 100

            score = 100
            score -= min(err_rate, 80)          # penalize errors
            score -= min(avg_ms / 50, 20)       # penalize latency
            score = max(0, min(100, score))

        result.append({
            "agent": name,
            "calls": calls,
            "health_score": round(score, 1),
        })

    return {"agents": result}

@app.get("/system/agent-call-graph")
def agent_call_graph():
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

@app.get("/system/diagnostics")
def diagnostics():
    # OpenClaw health
    oc = subprocess.run(
        ["systemctl", "is-active", "openclaw-gateway"],
        capture_output=True
    ).stdout.decode().strip()

    # Runtime basic stats
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent

    # Recent events
    events = list(EVENT_TIMELINE)[-20:]

    # Recent RPS snapshot
    rps_info = openclaw_rps()

    return {
        "openclaw_status": oc,
        "runtime_cpu": cpu,
        "runtime_ram": ram,
        "rps": rps_info.get("rps"),
        "error_rate": rps_info.get("error_rate"),
        "recent_events": events,
    }

@app.get("/system/runtime-health")
def runtime_health():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    threads = threading.active_count()
    return {
        "status": "ok",
        "cpu": cpu,
        "ram": ram,
        "threads": threads,
    }

@app.get("/system/runtime-health")
def runtime_health():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    threads = threading.active_count()

    # Simple health score
    score = 100
    score -= min(cpu, 50) * 0.5
    score -= min(ram, 50) * 0.5
    score -= max(0, threads - 50)

    score = max(0, min(100, score))

    return {
        "cpu": cpu,
        "ram": ram,
        "threads": threads,
        "health_score": round(score, 1)
    }

@app.get("/system/diagnostics")
def diagnostics():
    oc = subprocess.run(
        ["systemctl", "is-active", "openclaw-gateway"],
        capture_output=True
    ).stdout.decode().strip()

    runtime = runtime_health()
    rps_info = openclaw_rps()
    agent_info = agent_health()

    return {
        "gateway_status": oc,
        "runtime_health": runtime,
        "rps": rps_info,
        "agent_health": agent_info,
        "recent_events": list(EVENT_TIMELINE)[-20:]
    }

@app.get("/system/cluster-nodes")
def cluster_nodes():
    results = [ping_runtime(n) for n in CLUSTER_NODES]
    return {"nodes": results}

@app.get("/system/agent-memory-graph")
def agent_memory_graph():
    nodes = [
        {"id": "planner"},
        {"id": "memory-core"},
        {"id": "writer"},
        {"id": "runtime"},
    ]
    links = [
        {"source": "planner", "target": "memory-core", "weight": 0.8},
        {"source": "memory-core", "target": "writer", "weight": 0.6},
        {"source": "writer", "target": "runtime", "weight": 0.9},
    ]
    return {"nodes": nodes, "links": links}

# -------------------------------------------------

def ping_runtime(node):
    url = f"http://{node['host']}:{node['port']}/health"
    start = time.time()
    try:
        r = requests.get(url, timeout=1)
        latency = (time.time() - start) * 1000
        if r.status_code == 200:
            return {
                "id": node["id"],
                "host": node["host"],
                "port": node["port"],
                "role": node["role"],
                "status": "online",
                "latency_ms": round(latency, 1),
            }
        else:
            return {
                "id": node["id"],
                "host": node["host"],
                "port": node["port"],
                "role": node["role"],
                "status": "degraded",
                "latency_ms": None,
            }
    except:
        return {
            "id": node["id"],
            "host": node["host"],
            "port": node["port"],
            "role": node["role"],
            "status": "offline",
            "latency_ms": None,
        }

def choose_best_runtime():
    nodes = [ping_runtime(n) for n in CLUSTER_NODES]
    online = [n for n in nodes if n["status"] == "online"]

    if not online:
        return None

    # pick lowest latency
    best = sorted(online, key=lambda x: x["latency_ms"])[0]
    return best

def dispatch_to_runtime(node, path: str, payload: dict):
    url = f"http://{node['host']}:{node['port']}{path}"
    try:
        r = requests.post(url, json=payload, timeout=10)
        return {
            "ok": r.status_code == 200,
            "status": r.status_code,
            "data": r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text,
            "target": node["id"],
        }
    except Exception as e:
        return {
            "ok": False,
            "status": None,
            "error": str(e),
            "target": node["id"],
        }

@app.post("/orchestrate/run-agent")
async def orchestrate_run_agent(req: AgentTask):
    # 1) choose best runtime
    best = choose_best_runtime()
    if not best:
        # no remote nodes online → run locally
        state = {"task": req.task, "agent": req.agent, "history": [], "result": ""}
        result_state = app_graph.invoke(state)
        return {
            "mode": "local-fallback",
            "target": "self",
            "result": result_state,
        }

    # 2) try remote
    payload = {"task": req.task, "agent": req.agent}
    remote = dispatch_to_runtime(best, "/run-agent", payload)

    if remote["ok"]:
        return {
            "mode": "remote",
            "target": remote["target"],
            "result": remote["data"],
        }

    # 3) remote failed → fallback to local
    state = {"task": req.task, "agent": req.agent, "history": [], "result": ""}
    result_state = app_graph.invoke(state)

    EVENT_TIMELINE.append({
        "timestamp": time.time(),
        "type": "orchestrator-fallback",
        "detail": f"remote {best['id']} failed, ran locally"
    })

    return {
        "mode": "remote-failed-local-fallback",
        "target": best["id"],
        "remote_error": remote.get("error") or remote.get("status"),
        "result": result_state,
    }

@app.post("/orchestrate/run")
async def orchestrate_run(req: TaskRequest):
    best = choose_best_runtime()
    if not best:
        state: State = {"task": req.task, "history": [], "result": ""}
        result_state = app_graph.invoke(state)
        return {
            "mode": "local-fallback",
            "target": "self",
            "result": result_state,
        }

    payload = {"task": req.task}
    remote = dispatch_to_runtime(best, "/run", payload)

    if remote["ok"]:
        return {
            "mode": "remote",
            "target": remote["target"],
            "result": remote["data"],
        }

    state: State = {"task": req.task, "history": [], "result": ""}
    result_state = app_graph.invoke(state)

    EVENT_TIMELINE.append({
        "timestamp": time.time(),
        "type": "orchestrator-fallback",
        "detail": f"remote {best['id']} failed for /run, ran locally"
    })

    return {
        "mode": "remote-failed-local-fallback",
        "target": best["id"],
        "remote_error": remote.get("error") or remote.get("status"),
        "result": result_state,
    }

# -------------------------
# START WATCHDOG THREAD
# -------------------------
threading.Thread(target=runtime_watchdog, daemon=True).start()
threading.Thread(target=openclaw_watchdog, daemon=True).start()
