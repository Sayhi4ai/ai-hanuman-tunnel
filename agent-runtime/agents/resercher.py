from langchain_ollama import ChatOllama

def load():
    return ChatOllama(
        model="gemma4:latest",
        base_url="http://127.0.0.1:11434",
        system="You are a research agent. Provide deep analysis."
    )
