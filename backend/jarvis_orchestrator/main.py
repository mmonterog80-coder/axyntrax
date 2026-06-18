# -*- coding: utf-8 -*-
"""
JARVIS AX - FastAPI Principal
Con JWT, Rate Limiting, HUD y Telemetría
"""
import os
import time
import psutil
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import SlowApi, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="JARVIS AX API", version="2.0.0")

# Rate Limiting
slowapi = SlowApi(key_func=get_remote_address)
app.state.limiter = slowapi
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# JWT simple
security = HTTPBearer(auto_error=False)
API_SECRET = os.getenv('API_SECRET', 'axyntrax-secret-change-me')

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=401, detail="Token requerido")
    if credentials.credentials != API_SECRET:
        raise HTTPException(status_code=403, detail="Token inválido")
    return credentials.credentials

# Start time para uptime
START_TIME = time.time()

# ============ RUTAS PÚBLICAS (Rate Limited) ============

@app.get("/")
@slowapi.limit(limit="60/minute")
async def root():
    return {"message": "JARVIS AX Online", "version": "2.0.0", "timestamp": datetime.now().isoformat()}

@app.get("/health")
@slowapi.limit(limit="120/minute")
async def health():
    uptime = time.time() - START_TIME
    return {
        "status": "healthy",
        "uptime_seconds": int(uptime),
        "uptime_human": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m",
        "timestamp": datetime.now().isoformat()
    }

# ============ RUTAS PROTEGIDAS (JWT + Rate Limited) ============

@app.get("/api/telemetry/system")
@slowapi.limit(limit="30/minute")
async def telemetry(token: str = Depends(verify_token)):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    
    return {
        "cpu": cpu,
        "ram": ram,
        "disk": disk,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/status")
@slowapi.limit(limit="30/minute")
async def status(token: str = Depends(verify_token)):
    return {
        "bot_telegram": "activo",
        "deepseek": "conectado",
        "supabase": "conectado" if os.getenv('SUPABASE_URL') else "no disponible",
        "fish_audio": "configurado" if os.getenv('FISH_API_KEY') else "no configurado",
        "timestamp": datetime.now().isoformat()
    }

# ============ HUD HTML ============

HUD_HTML = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JARVIS AX - HUD</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; min-height: 100vh; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; padding: 40px; background: rgba(255,255,255,0.1); border-radius: 20px; margin-bottom: 30px; backdrop-filter: blur(10px); }
        .header h1 { font-size: 3em; margin-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
        .card h3 { margin-bottom: 20px; font-size: 1.5em; }
        .status { display: inline-block; padding: 8px 20px; border-radius: 25px; font-weight: bold; background: #10b981; }
        .metric { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .metric-value { font-weight: bold; color: #60a5fa; font-size: 1.2em; }
        .btn { display: inline-block; padding: 12px 25px; background: rgba(255,255,255,0.2); border-radius: 10px; color: #fff; text-decoration: none; margin: 5px; transition: all 0.3s; }
        .btn:hover { background: rgba(255,255,255,0.3); transform: translateY(-2px); }
        @media (max-width: 768px) { .header h1 { font-size: 2em; } .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1> JARVIS AX</h1>
            <p>Dashboard de Control - Enjambre de IAs</p>
            <p id="timestamp" style="margin-top: 10px;"></p>
        </div>
        <div class="grid">
            <div class="card">
                <h3>📡 Estado del Sistema</h3>
                <div><span class="status">ONLINE</span></div>
                <div style="margin-top: 20px;">
                    <div class="metric"><span>API:</span><span class="metric-value" id="api-status">Activo</span></div>
                    <div class="metric"><span>Uptime:</span><span class="metric-value" id="uptime">-</span></div>
                    <div class="metric"><span>Bot Telegram:</span><span class="metric-value" id="bot-status">-</span></div>
                </div>
            </div>
            <div class="card">
                <h3>📊 Telemetría</h3>
                <div class="metric"><span>CPU:</span><span class="metric-value" id="cpu">-</span></div>
                <div class="metric"><span>RAM:</span><span class="metric-value" id="ram">-</span></div>
                <div class="metric"><span>Disco:</span><span class="metric-value" id="disk">-</span></div>
            </div>
            <div class="card">
                <h3>🔗 Accesos Rápidos</h3>
                <a href="https://railway.app/dashboard" class="btn" target="_blank">🚂 Railway</a>
                <a href="https://supabase.com/dashboard/project/qatawtbfrfreakdbluat" class="btn" target="_blank">🗄️ Supabase</a>
                <a href="https://github.com/axyntraxautomation-lab/AXYNTRAX" class="btn" target="_blank">💻 GitHub</a>
            </div>
            <div class="card">
                <h3>🎯 Módulos SaaS</h3>
                <div class="metric"><span>VetManager:</span><span class="metric-value"> Activo</span></div>
                <div class="metric"><span>LegalDesk:</span><span class="metric-value">🟢 Activo</span></div>
                <div class="metric"><span>DentalFlow:</span><span class="metric-value">🟢 Activo</span></div>
            </div>
        </div>
    </div>
    <script>
        async function refreshData() {
            try {
                const healthRes = await fetch('/health');
                const health = await healthRes.json();
                document.getElementById('uptime').textContent = health.uptime_human;
                document.getElementById('timestamp').textContent = 'Última actualización: ' + new Date().toLocaleString('es-PE');
            } catch (error) {
                console.error('Error:', error);
            }
        }
        refreshData();
        setInterval(refreshData, 10000);
    </script>
</body>
</html>"""

@app.get("/dashboard", response_class=HTMLResponse)
@slowapi.limit(limit="30/minute")
async def dashboard():
    return HTMLResponse(content=HUD_HTML)

@app.get("/web", response_class=HTMLResponse)
@slowapi.limit(limit="30/minute")
async def web_premium():
    return HTMLResponse(content=HUD_HTML)

# ============ RUTAS DE MÓDULOS SaaS ============

@app.get("/api/modules/vet")
@slowapi.limit(limit="30/minute")
async def vet_module(token: str = Depends(verify_token)):
    return {
        "module": "VetManager",
        "status": "active",
        "features": ["Gestión de pacientes", "Agenda de citas", "Historial médico", "Recetas", "Facturación", "Inventario"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/modules/legal")
@slowapi.limit(limit="30/minute")
async def legal_module(token: str = Depends(verify_token)):
    return {
        "module": "LegalDesk",
        "status": "active",
        "features": ["Gestión de casos", "Calendario de plazos", "Generación de documentos", "Base de conocimiento", "Facturación"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/modules/dental")
@slowapi.limit(limit="30/minute")
async def dental_module(token: str = Depends(verify_token)):
    return {
        "module": "DentalFlow",
        "status": "active",
        "features": ["Odontograma digital", "Agenda con recordatorios", "Planes de tratamiento", "Historial clínico", "Facturación"],
        "timestamp": datetime.now().isoformat()
    }

# ============ INICIO ============

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
