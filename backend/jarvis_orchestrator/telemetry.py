import psutil, time
from fastapi import APIRouter

router = APIRouter()

@router.get("/telemetry/system")
async def system_telemetry():
    net = psutil.net_io_counters()
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "ram_percent": psutil.virtual_memory().percent,
        "net_bytes_sent": net.bytes_sent,
        "net_bytes_recv": net.bytes_recv,
        "uptime_seconds": int(time.time() - psutil.boot_time()),
        "orchestrator_status": "healthy"
    }

@router.get("/ias/status")
async def ias_status():
    return {
        "ias": [
            {"id": "deepseek", "nombre": "DeepSeek V4", "estado": "online"},
            {"id": "gpt4o", "nombre": "GPT-4o", "estado": "online"},
            {"id": "mercury", "nombre": "MERCURY", "estado": "online"},
            {"id": "athena", "nombre": "ATHENA", "estado": "online"},
            {"id": "vulcan", "nombre": "VULCAN", "estado": "online"},
            {"id": "hermes", "nombre": "HERMES", "estado": "online"},
            {"id": "diana", "nombre": "DIANA", "estado": "online"},
            {"id": "sre", "nombre": "SRE-Autopilot", "estado": "online"}
        ],
        "total": 8,
        "online": 8
    }