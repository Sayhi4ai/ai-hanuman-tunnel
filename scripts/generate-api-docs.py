import json
import requests

OPENAPI_URL = "http://localhost:7200/openapi.json"

print("Fetching OpenAPI schema...")
schema = requests.get(OPENAPI_URL).json()

with open("API_DOCS.md", "w") as f:
    f.write("# API Documentation\n\n")
    f.write("Generated automatically from FastAPI.\n\n")

    for path, methods in schema["paths"].items():
        f.write(f"## `{path}`\n\n")
        for method, details in methods.items():
            f.write(f"### {method.upper()}\n")
            f.write(f"**Summary:** {details.get('summary', 'N/A')}\n\n")
            if "description" in details:
                f.write(f"{details['description']}\n\n")
            if "requestBody" in details:
                f.write("**Request Body:**\n")
                f.write("```json\n")
                f.write(json.dumps(details["requestBody"], indent=2))
                f.write("\n```\n\n")
            if "responses" in details:
                f.write("**Responses:**\n")
                f.write("```json\n")
                f.write(json.dumps(details["responses"], indent=2))
                f.write("\n```\n\n")
