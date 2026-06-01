import requests
import time

class ClusterNode:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.last_seen = time.time()

    def is_alive(self):
        try:
            r = requests.get(f"{self.url}/health")
            return r.status_code == 200
        except:
            return False

    def run_agent(self, agent, task):
        payload = {"agent": agent, "task": task}
        r = requests.post(f"{self.url}/run-agent", json=payload)
        return r.json()
