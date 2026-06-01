import threading
from queue_daemon import run_queue_daemon
from graph import AGENT_REGISTRY

def queue_daemon_agent(state):
    interval = 2

    t = threading.Thread(target=run_queue_daemon, args=(interval,))
    t.daemon = True
    t.start()

    state["result"] = "Queue daemon started (persistent background worker)."
    state["history"].append("QUEUE_DAEMON: started")
    return state

def load():
    AGENT_REGISTRY["queue_daemon"] = queue_daemon_agent
    return queue_daemon_agent
