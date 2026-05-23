def run(text: str):
    return f"Echo: {text}"

schema = {
    "name": "echo",
    "description": "Returns the same text back.",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {"type": "string"}
        },
        "required": ["text"]
    }
}
