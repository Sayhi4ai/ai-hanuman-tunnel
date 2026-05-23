import sys
sys.path.insert(0, "/home/inteligent-human/ai-bots/agent-runtime")

import logger
from logger import log

print("LOGGER LOADED FROM:", logger.__file__)
import time
import subprocess
import requests
from pathlib import Path

PORT = 7200
WORKERS = 4
HEALTH_URL = f"http://127.0.0.1:{PORT}/health"
CHECK_INTERVAL = 50
UNHEALTHY_THRESHOLD = 15
STARTUP_GRACE_PERIOD = 20
REQUEST_TIMEOUT = 20

BASE_DIR = Path("/home/inteligent-human/ai-bots/agent-runtime")
VENV_PYTHON = BASE_DIR / "venv" / "bin" / "python"
RUNTIME_CMD = [
    str(VENV_PYTHON),
    "-m",
    "uvicorn",
    "runtime_api:app",
    "--host", "0.0.0.0",
    "--port", str(PORT),
    "--workers", str(WORKERS),
]

def is_healthy() -> bool:
    try:
        r = requests.get(HEALTH_URL, timeout=REQUEST_TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False

def start_process():
    log("starting_runtime", cmd=RUNTIME_CMD)
    return subprocess.Popen(RUNTIME_CMD, cwd=str(BASE_DIR), stdout=sys.stdout, stderr=sys.stderr)

def stop_process(proc: subprocess.Popen | None):
    if proc is None:
        return
    try:
        log("stopping_runtime")
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            log("process did not terminate gracefully, killing...")
            proc.kill()
    except Exception as e:
        log("error while stopping process: {e}")

def main():
    proc = start_process()
    unhealthy_count = 0

    log(f"startup grace period: {STARTUP_GRACE_PERIOD}s")
    time.sleep(STARTUP_GRACE_PERIOD)

    while True:
        if proc is None or proc.poll() is not None:
            log("process not running, restarting...")
            stop_process(proc)
            proc = start_process()
            unhealthy_count = 0
            log(f"post-restart grace period: {STARTUP_GRACE_PERIOD}s")
            time.sleep(STARTUP_GRACE_PERIOD)
            continue

        if is_healthy():
            if unhealthy_count > 0:
                log(f"health_restored (unhealthy_count was {unhealthy_count})")
            unhealthy_count = 0
        else:
            unhealthy_count += 1
            log(f"health_failed (unhealthy_count={unhealthy_count})")

        if unhealthy_count >= UNHEALTHY_THRESHOLD:
            log(f"unhealthy threshold reached ({UNHEALTHY_THRESHOLD}), restarting runtime...")
            stop_process(proc)
            proc = start_process()
            unhealthy_count = 0
            log(f"post-restart grace period: {STARTUP_GRACE_PERIOD}s")
            time.sleep(STARTUP_GRACE_PERIOD)
            continue

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
