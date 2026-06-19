import psutil, time, os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer(auto_error=False)
API_SECRET = os.getenv('API_SECRET', 'axyntrax-secret-change-me')

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials or credentials.credentials != API_SECRET:
        raise HTTPException(status_code=401, detail="Token requerido o inválido")
    return credentials.credentials

@router.get("/telemetry/system")
async def system_telemetry(token: str = Depends(verify_token)):
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
async def ias_status(token: str = Depends(verify_token)):
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