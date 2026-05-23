import json, sys, time

def log(event: str, **kwargs):
    entry = {
        "timestamp": time.time(),
        "event": event,
        "data": kwargs,
    }
    sys.stdout.write(json.dumps(entry) + "\n")
    sys.stdout.flush()
