from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="JARVIS AX")

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend'))

from arquitecto_hibrido import iniciar_arquitecto_bg

@app.on_event("startup")
async def startup_event():
    print("======================================")
    print(" INICIANDO JARVIS AX (CLOUD MODE) ")
    print("======================================")
    import httpx
    try:
        from scheduler import start_scheduler
        start_scheduler()
        iniciar_arquitecto_bg()
        
        # Iniciar loop de broadcast de tareas en RAM hacia los WebSockets
        import asyncio
        from queue_manager import pop_task
        import json
        async def broadcast_tasks_loop():
            while True:
                task = pop_task()
                if task:
                    await broadcast(json.dumps(task))
                await asyncio.sleep(1)
        asyncio.create_task(broadcast_tasks_loop())
        print("[*] Loop de broadcast de tareas iniciado.")
    except Exception as e:
        print(f"[JARVIS] Error iniciando scheduler: {e}")

    domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if domain and telegram_token:
        webhook_url = f"https://{domain}/tasks/telegram/webhook"
        api_url = f"https://api.telegram.org/bot{telegram_token}/setWebhook?url={webhook_url}"
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(api_url)
                print(f"[*] Telegram Webhook configurado en {webhook_url}: {resp.json()}")
            except Exception as e:
                print(f"[!] Fallo al configurar Telegram Webhook: {e}")

from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import Depends

security = HTTPBasic()

HUD_USER = os.getenv("HUD_USER")
HUD_PASS = os.getenv("HUD_PASS")

if not HUD_USER or not HUD_PASS:
    # Auto-generar credenciales seguras para esta ejecución si no existen
    HUD_USER = "admin_temp"
    HUD_PASS = secrets.token_urlsafe(12)
    print("="*50)
    print(f"⚠️ ATENCIÓN: No se encontraron HUD_USER o HUD_PASS en .env")
    print(f"🔐 Creadas credenciales temporales por seguridad:")
    print(f"User: {HUD_USER}")
    print(f"Pass: {HUD_PASS}")
    print("="*50)

def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    # correct_username = secrets.compare_digest(credentials.username, HUD_USER)
    # correct_password = secrets.compare_digest(credentials.password, HUD_PASS)
    # if not (correct_username and correct_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Basic"},
    #     )
    return credentials.username

from fastapi.staticfiles import StaticFiles

futuristic_assets = os.path.join(FRONTEND_DIR, "futuristic", "assets")
if os.path.exists(futuristic_assets):
    app.mount("/assets", StaticFiles(directory=futuristic_assets), name="assets")

@app.get("/")
def serve_hud():
    hud_path = os.path.join(FRONTEND_DIR, "hud_jarvis_web.html")
    if os.path.exists(hud_path):
        return FileResponse(hud_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "JARVIS HUD no encontrado"}

@app.get("/landing")
def serve_landing():
    landing_path = os.path.join(FRONTEND_DIR, "futuristic", "index.html")
    if os.path.exists(landing_path):
        return FileResponse(landing_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    return {"message": "Futuristic Web no encontrado"}

@app.get("/logo.ico")
def serve_logo_ico():
    return FileResponse(os.path.join(FRONTEND_DIR, "futuristic", "logo.ico"))

@app.get("/logo.png")
def serve_logo_png():
    return FileResponse(os.path.join(FRONTEND_DIR, "futuristic", "logo.png"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ai/status")
def ai_status():
    """Devuelve el estado online de todas las IAs registradas."""
    from plan_generator import get_ai_status
    return get_ai_status()

@app.post("/tts")
async def tts_endpoint(body: dict):
    """Convierte texto a voz usando el motor centralizado (Fish Audio / OpenAI / ElevenLabs)."""
    text = body.get("text", "")
    if not text:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No text provided")
        
    from voice_generator import generar_audio
    import re
    
    # Limpiar el texto para que el TTS no se trabe con símbolos raros del código
    texto_limpio = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,;:!? \n]', '', text)
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
    
    if len(texto_limpio) > 800:
        texto_limpio = texto_limpio[:800] + "... Fin de la lectura."
        
    audio_path = generar_audio(texto_limpio)
    
    if audio_path.startswith("[Error"):
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=audio_path)
        
    from fastapi.responses import FileResponse
    return FileResponse(audio_path, media_type="audio/mpeg")

@app.post("/ai/test")
def ai_test(body: dict):
    """Prueba rápida de enrutamiento con un objetivo dado."""
    from plan_generator import generate_plan
    objective = body.get("objective", "Hola")
    result = generate_plan(objective, module="test", action_type="execute")
    return {"result": result}

from tasks import router
app.include_router(router, prefix="/tasks")

@app.get("/api/meta/webhook")
async def verify_meta_webhook(request: Request):
    """Verificación del webhook para Meta (Facebook/WhatsApp/Instagram)"""
    verify_token = os.getenv("META_VERIFY_TOKEN", "AXYNTRAX_META_SECURE_TOKEN_2026")
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == verify_token:
            print("[META] Webhook verificado exitosamente.")
            from fastapi.responses import Response
            return Response(content=challenge, status_code=200)
        else:
            raise HTTPException(status_code=403, detail="Token de verificación inválido")
    raise HTTPException(status_code=400, detail="Faltan parámetros hub")

@app.post("/api/meta/webhook")
async def receive_meta_webhook(request: Request):
    """Recepción de eventos desde Meta"""
    try:
        body = await request.json()
        print(f"[META] Evento recibido: {body}")
        
        from queue_manager import push_task
        push_task("meta_event", body)
        
        return {"status": "success"}
    except Exception as e:
        print(f"[META] Error procesando evento: {e}")
        return {"status": "error", "message": str(e)}

from fastapi import WebSocket, WebSocketDisconnect, Depends, Header
from fastapi.security import APIKeyHeader

EDGE_SECRET_TOKEN = os.getenv("EDGE_SECRET_TOKEN", "axyntrax-edge-super-secret-2026")
api_key_header = APIKeyHeader(name="X-Edge-Token", auto_error=False)

def verify_edge_token(x_edge_token: str = Depends(api_key_header)):
    if not x_edge_token or x_edge_token != EDGE_SECRET_TOKEN:
        raise HTTPException(status_code=403, detail="Acceso denegado: Token de Edge inválido.")
    return x_edge_token

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = None):
    await websocket.accept()
    # Autenticación inicial vía query param o primer mensaje
    if token != EDGE_SECRET_TOKEN:
        auth_msg = await websocket.receive_text()
        if auth_msg != f"AUTH:{EDGE_SECRET_TOKEN}":
            await websocket.close(code=1008)
            return

    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Aquí procesaremos respuestas asíncronas del Agente Local en el futuro
            print(f"[EDGE-WS] Mensaje recibido del PC local: {data}")
    except WebSocketDisconnect:
        clients.remove(websocket)

async def broadcast(message: str):
    for client in list(clients):
        try:
            await client.send_text(message)
        except:
            clients.remove(client)

from pydantic import BaseModel
from state_manager import global_state

class EdgeResponse(BaseModel):
    output: str
    error: bool

@app.get("/edge/commands")
def get_edge_commands(token: str = Depends(verify_edge_token)):
    # El PC local hace polling a esta ruta. Actualizamos su ping.
    global_state.update_pc_ping()
    
    cmd = global_state.pop_edge_command()
    if cmd:
        return {"command": cmd}
    return {"command": None}

@app.post("/edge/response")
def post_edge_response(resp: EdgeResponse, token: str = Depends(verify_edge_token)):
    global_state.update_pc_ping()
    global_state.push_edge_response(resp.output)
    return {"status": "ok"}

from fastapi import Request
import openai

@app.post("/ask-deepseek")
async def ask_deepseek(request: Request):
    body = await request.json()
    pregunta = body.get("pregunta", "")
    if not pregunta:
        raise HTTPException(status_code=400, detail="Falta 'pregunta'")
    try:
        client = openai.OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com/v1")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": pregunta}],
            temperature=0.3,
            max_tokens=500
        )
        return {"respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class BroadcastMessage(BaseModel):
    message: str

@app.post("/webhook/telegram_broadcast")
async def telegram_broadcast(body: BroadcastMessage):
    """Permite al frontend Next.js enviar alertas al canal de Telegram (ej. pagos de Stripe)"""
    from telegram_handler import send_telegram_message, send_telegram_voice
    from voice_generator import generar_audio
    
    chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
    if not chat_id:
        return {"error": "TELEGRAM_ALLOWED_CHAT_ID no configurado"}
        
    # Enviar texto
    send_telegram_message(chat_id, body.message)
    
    # Enviar voz
    audio_path = generar_audio(body.message.replace("✅", "").replace("\n", ". "))
    if audio_path and not audio_path.startswith("[Error"):
        send_telegram_voice(chat_id, audio_path)
        
    return {"status": "broadcasted"}

