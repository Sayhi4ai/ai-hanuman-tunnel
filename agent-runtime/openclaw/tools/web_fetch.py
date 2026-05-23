import requests

schema = {
    "name": "web_fetch",
    "description": "Fetches the contents of a URL",
    "arguments": {
        "url": {
            "type": "string",
            "description": "The URL to fetch"
        }
    }
}

def run(url: str):
    r = requests.get(url, timeout=10)
    return r.text[:2000]
