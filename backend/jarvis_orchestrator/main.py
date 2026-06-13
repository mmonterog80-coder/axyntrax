import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="JARVIS AX Orchestrator", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

from tasks import router as tasks_router
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])