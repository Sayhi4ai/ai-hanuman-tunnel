from fastapi import FastAPI

app = FastAPI(title="OpenClawGuardian", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok", "service": "OpenClawGuardian"}

@app.get("/info")
def info():
    return {
        "name": "OpenClawGuardian",
        "port": 9000,
        "mode": "autonomous",
        "telegram_enabled": True,
    }
