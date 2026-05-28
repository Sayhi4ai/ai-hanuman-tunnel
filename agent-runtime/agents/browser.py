from graph import AGENT_REGISTRY
from playwright.sync_api import sync_playwright

def browser_agent(state):
    task = state.get("task", "")
    url = task.replace("browse", "").strip()

    if not url.startswith("http"):
        url = "https://" + url

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=15000)
            content = page.content()
            browser.close()

        result = f"Page content from {url}:\n\n{content[:5000]}..."
    except Exception as e:
        result = f"Browser error: {e}"

    state["result"] = result
    state["history"].append(f"BROWSER: visited {url}")
    return state

def load():
    AGENT_REGISTRY["browser"] = browser_agent
    return browser_agent
