# -*- coding: utf-8 -*-
"""
JARVIS AX - FastAPI Principal
Con JWT, Rate Limiting, HUD y Telemetría
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import psutil
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException, Depends
from contextlib import asynccontextmanager
from telemetry import router as telemetry_router
from secrets_broker import router as secrets_router
from whatsapp_bot import router as whatsapp_router
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Startup y Shutdown Events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando J.A.R.V.I.S. AXYNTRAX Neural Network...")
    yield
    print("Apagando módulos...")

app = FastAPI(title="AXYNTRAX Orchestrator", version="Mark X", lifespan=lifespan)

# Montar Rutas
app.include_router(whatsapp_router, prefix="/api")
app.include_router(telemetry_router, prefix="/api")
app.include_router(secrets_router, prefix="/api")

# Rate Limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
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

# El frontend ahora se servirá vía Proxy a Space-Z (ver final del archivo)

@app.get("/health")
# @limiter.limit("120/minute")
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
# @limiter.limit("30/minute")
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
# @limiter.limit("30/minute")
async def status(token: str = Depends(verify_token)):
    return {
        "bot_telegram": "activo",
        "deepseek": "conectado",
        "supabase": "conectado" if os.getenv('SUPABASE_URL') else "no disponible",
        "fish_audio": "configurado" if os.getenv('FISH_API_KEY') else "no configurado",
        "timestamp": datetime.now().isoformat()
    }

# ============ HUD HTML ============

from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI

class ChatRequest(BaseModel):
    message: str

# Montaje eliminado de /dashboard para evitar confusiones. Todo va a la raíz /

import base64

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_key:
            return {"reply": "Error: Enlace con DeepSeek perdido."}
        
        client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")
        sys_prompt = "Eres JARVIS, el Orquestador Maestro (arquitectura Z.IA) del ecosistema de IAs de AXYNTRAX. Estás conectado al HUD Web del usuario. Responde siempre asumiendo tu identidad como JARVIS. Sé conciso, elegante y servicial, usando tu clásica personalidad."
        
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": req.message}
            ],
            max_tokens=300
        )
        reply_text = resp.choices[0].message.content
        
        # Generar audio clonado con Fish Audio
        audio_b64 = None
        FISH_API_KEY = os.getenv("FISH_API_KEY")
        if FISH_API_KEY:
            try:
                from fish_audio_sdk import Session, TTSRequest
                from fish_audio_sdk.schemas import ReferenceAudio
                
                # Buscar jarvis_reference.mp3 en la carpeta de ejecución
                ref_path = os.path.join(base_dir, "jarvis_reference.mp3") # base_dir is /app
                
                if os.path.exists(ref_path):
                    with open(ref_path, "rb") as ref_f:
                        ref_audio_bytes = ref_f.read()
                    
                    ref = ReferenceAudio(audio=ref_audio_bytes, text="He finalizado a su espera, señor")
                    tts_req = TTSRequest(text=str(reply_text)[:500], format="mp3", references=[ref])
                    
                    session = Session(FISH_API_KEY)
                    audio_chunks = []
                    for chunk in session.tts(tts_req):
                        audio_chunks.append(chunk)
                    
                    full_audio = b"".join(audio_chunks)
                    audio_b64 = base64.b64encode(full_audio).decode("utf-8")
            except Exception as e:
                print(f"Error HUD Audio: {e}")

        return {"reply": reply_text, "audio": audio_b64}
    except Exception as e:
        return {"reply": f"Fallo en la matriz de red: {str(e)}"}

from reasoning_engine import run_chain_of_thought

@app.get("/api/modules/vet")
async def vet_module(token: str = Depends(verify_token)):
    return {
        "module": "VetManager",
        "status": "active",
        "features": ["Gestión de pacientes", "Agenda de citas", "Historial médico", "Recetas", "Facturación", "Inventario"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/mark_x/reason")
async def execute_reasoning(task: dict, token: str = Depends(verify_token)):
    """Ejecuta el bucle cognitivo Mark X (Gemini -> DeepSeek -> Sentinel)"""
    description = task.get("description", "Sin descripción")
    result = run_chain_of_thought(description)
    return result

@app.get("/api/modules/legal")
# @limiter.limit("30/minute")
async def legal_module(token: str = Depends(verify_token)):
    return {
        "module": "LegalDesk",
        "status": "active",
        "features": ["Gestión de casos", "Calendario de plazos", "Generación de documentos", "Base de conocimiento", "Facturación"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/modules/dental")
# @limiter.limit("30/minute")
async def dental_module(token: str = Depends(verify_token)):
    return {
        "module": "DentalFlow",
        "status": "active",
        "features": ["Odontograma digital", "Agenda con recordatorios", "Planes de tratamiento", "Historial clínico", "Facturación"],
        "timestamp": datetime.now().isoformat()
    }

# (Montado en top level)
from tasks import router as tasks_router
app.include_router(tasks_router) # Mounts /telegram/webhook

@app.get("/api/logs")
async def get_logs():
    try:
        with open("telegram.log", "r") as f:
            return {"logs": f.read()[-5000:]}
    except Exception as e:
        return {"error": str(e)}

# ============ JARVIS AX v3.0 SKILLS API (By DeepSeek) ============

from skills_catalog import DEFAULT_SKILLS, DEFAULT_TOOLS, Skill

# Estado en memoria para permitir reordenamiento
skills_state = [s.model_dump() for s in DEFAULT_SKILLS]

@app.get("/api/skills")
async def list_skills(token: str = Depends(verify_token)):
    # Devuelve skills ordenadas por prioridad (mayor a menor)
    sorted_skills = sorted(skills_state, key=lambda x: x['priority'], reverse=True)
    return {"skills": sorted_skills}

@app.get("/api/tools")
async def list_tools(token: str = Depends(verify_token)):
    return {"tools": [t.model_dump() for t in DEFAULT_TOOLS]}

@app.get("/api/skills/count")
async def count_skills(token: str = Depends(verify_token)):
    return {"total_skills": len(skills_state)}

class ExecuteRequest(BaseModel):
    skill_id: str
    params: dict = {}

@app.post("/api/skills/execute")
async def execute_skill(req: ExecuteRequest, token: str = Depends(verify_token)):
    # Mock de ejecución
    skill = next((s for s in skills_state if s['id'] == req.skill_id), None)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    
    return {
        "status": "success",
        "message": f"Ejecutando skill {skill['name']} de forma simulada",
        "result": {"output": "Mock output para la fase 1 de arquitectura"}
    }

class ReorderRequest(BaseModel):
    skill_id: str
    new_priority: int

@app.post("/api/skills/reorder")
async def reorder_skills(req: ReorderRequest, token: str = Depends(verify_token)):
    skill = next((s for s in skills_state if s['id'] == req.skill_id), None)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill no encontrada")
    
    skill['priority'] = req.new_priority
    return {"status": "success", "message": f"Prioridad de {req.skill_id} actualizada a {req.new_priority}"}

# ============ JARVIS AX v3.0 MARK VII API (SWARM & MAIL) ============

@app.get("/api/swarm/status")
async def swarm_status(token: str = Depends(verify_token)):
    departments = [
        {
            "id": "ceo",
            "name": "JARVIS Antigravity",
            "role": "CEO / PC Controller",
            "status": "ONLINE",
            "mem": "Core",
            "sub_agents": []
        },
        {
            "id": "strategy",
            "name": "Gemini 1.5",
            "role": "Dir. Estrategia y Arquitectura",
            "status": "ONLINE",
            "mem": "1.2GB",
            "sub_agents": [
                {"id": "vision", "name": "Vision", "role": "Market & E-commerce", "status": "ONLINE", "mem": "300MB"},
                {"id": "architect", "name": "Architect", "role": "Diseño B2B", "status": "IDLE", "mem": "0MB"},
                {"id": "kimi", "name": "Kimi", "role": "UX/UI Expert", "status": "ONLINE", "mem": "450MB"}
            ]
        },
        {
            "id": "factory",
            "name": "DeepSeek V3",
            "role": "Dir. Fábrica de Software",
            "status": "PROCESSING",
            "mem": "3.5GB",
            "sub_agents": [
                {"id": "stitch", "name": "Stitch", "role": "Frontend / React", "status": "PROCESSING", "mem": "1.1GB"},
                {"id": "forge", "name": "Forge", "role": "Backend / DB", "status": "ONLINE", "mem": "800MB"},
                {"id": "sentinel", "name": "Sentinel", "role": "QA & SecOps", "status": "IDLE", "mem": "0MB"}
            ]
        },
        {
            "id": "operations",
            "name": "Qwen 2.5",
            "role": "Dir. Operaciones e Infra",
            "status": "ONLINE",
            "mem": "1.8GB",
            "sub_agents": [
                {"id": "nano", "name": "Nano", "role": "API & Tools Admin", "status": "ONLINE", "mem": "120MB"},
                {"id": "devops", "name": "DevOps AI", "role": "Cloud Deployments", "status": "ONLINE", "mem": "200MB"},
                {"id": "banana2", "name": "Banana2", "role": "Data Processing", "status": "PROCESSING", "mem": "950MB"}
            ]
        }
    ]
    return {"swarm": departments}

# Base de datos simulada de correos
mock_inbox = [
    {"id": "mail_1", "from": "inversor@capital.com", "subject": "Reunión de Series A", "body": "Estimado CEO, ¿cuándo podemos ver la demo de AXYNTRAX?", "status": "unread"},
    {"id": "mail_2", "from": "aws-alerts@amazon.com", "subject": "ALERTA: Límite de facturación", "body": "Sus instancias EC2 están al 90% del límite de la capa gratuita.", "status": "read"}
]

@app.get("/api/mail/inbox")
async def get_inbox(token: str = Depends(verify_token)):
    return {"inbox": mock_inbox}

class MailRespondReq(BaseModel):
    mail_id: str

@app.post("/api/mail/respond")
async def respond_mail(req: MailRespondReq, token: str = Depends(verify_token)):
    mail = next((m for m in mock_inbox if m["id"] == req.mail_id), None)
    if not mail:
        raise HTTPException(status_code=404, detail="Mail no encontrado")
    
    mail["status"] = "replied"
    
    # Simular que JARVIS lee y responde usando DeepSeek (mockeado para rapidez visual)
    respuesta = f"Estimado {mail['from']},\n\nSoy J.A.R.V.I.S., asistente personal de AXYNTRAX. He procesado su solicitud respecto a '{mail['subject']}'. Nos pondremos en contacto a la brevedad.\n\nSaludos."
    
    return {
        "status": "success",
        "jarvis_response": respuesta,
        "message": "Correo procesado y respondido por el enjambre."
    }

# ============ PROXY INVERSO AL HUD (Space-Z) ============
import httpx
from fastapi.responses import StreamingResponse

# Creamos el cliente HTTPX para reenviar peticiones
proxy_client = httpx.AsyncClient(base_url="https://e1w4j5vf8fj0-d.space-z.ai")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def reverse_proxy(path: str, request: Request):
    # Evitar hacer proxy a las rutas de la API de FastAPI o docs
    if path.startswith("api/") or path.startswith("docs") or path.startswith("openapi.json"):
        raise HTTPException(status_code=404, detail="Ruta de API no encontrada")
        
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    
    # Preparar los headers quitando 'host' para que httpx asigne el de Space-Z
    headers = dict(request.headers)
    headers.pop("host", None)
    
    # Reenviar el request a Space-Z
    req = proxy_client.build_request(
        request.method,
        url,
        headers=headers,
        content=request.stream()
    )
    
    resp = await proxy_client.send(req, stream=True)
    
    # Retornar la respuesta al cliente tal cual viene de Space-Z
    return StreamingResponse(
        resp.aiter_raw(),
        status_code=resp.status_code,
        headers=resp.headers
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

