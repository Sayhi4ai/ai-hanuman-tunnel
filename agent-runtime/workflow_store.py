import json
import os

WORKFLOW_FILE = "workflows.json"

def load_workflows():
    if not os.path.exists(WORKFLOW_FILE):
        return {}
    with open(WORKFLOW_FILE, "r") as f:
        return json.load(f)

def save_workflows(data):
    with open(WORKFLOW_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_workflow(name):
    workflows = load_workflows()
    return workflows.get(name, None)

def save_workflow(name, steps):
    workflows = load_workflows()
    workflows[name] = steps
    save_workflows(workflows)
