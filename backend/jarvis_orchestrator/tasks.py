from fastapi import APIRouter, HTTPException
from models import TaskCreate, TaskResponse, TaskStatus
from db import create_task, get_task, update_task_status, get_next_pending_task
import os
from telegram_handler import process_telegram_update, send_telegram_message

router = APIRouter()

memory_queue = []

@router.get("/pop")
def pop_task_http():
    if memory_queue:
        return memory_queue.pop(0)
    return {"empty": True}

@router.post("/", response_model=TaskResponse, status_code=201)
def create_new_task(payload: TaskCreate):
    return create_task(payload)

@router.get("/next", response_model=TaskResponse)
def get_next_task():
    task = get_next_pending_task()
    if not task:
        raise HTTPException(status_code=404, detail="No hay tareas pendientes")
    return task

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task(task_id: str, status: str = None, error_details: str = None, result: str = None, payload: dict = None):
    s = status
    r = result
    e = error_details
    if payload:
        s = payload.get("status", s)
        r = payload.get("result", r)
        e = payload.get("error_details", e)
        
    updated = update_task_status(task_id, s, r, e)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
    if chat_id and s in ("completed", "failed"):
        msg = f"✅ Ejecucion Exitosa:\n{r}" if s == "completed" else f"❌ Ejecucion Fallida:\n{e}"
        send_telegram_message(int(chat_id), msg)
        
    return updated

@router.post("/telegram/webhook")
def telegram_webhook(body: dict):
    """
    Endpoint que recibe los mensajes desde Telegram.
    """
    process_telegram_update(body)
    return {"status": "processed"}
@router.post("/telegram/send")
def send_telegram_msg(chat_id: int, text: str):
    """
    Envía un mensaje de Telegram a un chat_id específico.
    """
    from telegram_handler import send_telegram_message
    result = send_telegram_message(chat_id, text)
    return result

from queue_manager import push_task



from instagram_handler import verify_webhook, process_instagram_update, send_instagram_message
from fastapi import Request, Response

@router.get("/instagram/webhook")
def instagram_webhook_verify(request: Request):
    """
    Endpoint para verificación inicial de Meta.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    verified_challenge = verify_webhook(mode, token, challenge)
    if verified_challenge is not False:
        return Response(content=str(verified_challenge), media_type="text/plain")
    raise HTTPException(status_code=403, detail="Token de verificacion invalido")

@router.post("/instagram/webhook")
def instagram_webhook_receive(body: dict):
    """
    Endpoint que recibe los DMs de Instagram.
    """
    process_instagram_update(body)
    return {"status": "EVENT_RECEIVED"}

@router.post("/instagram/send")
def send_instagram_msg(recipient_id: str, text: str):
    """
    Envía un mensaje directo a un usuario de Instagram.
    """
    result = send_instagram_message(recipient_id, text)
    return result

from workflows import execute_revenue_autopilot, execute_product_pipeline

@router.post("/corp/flow/revenue")
def trigger_revenue_flow(product_name: str):
    """
    Detona el flujo automático de Ingresos (Revenue Autopilot).
    """
    return execute_revenue_autopilot(product_name)

@router.post("/corp/flow/product")
def trigger_product_flow(idea: str):
    """
    Detona el flujo automático de Desarrollo de Producto (Product Pipeline).
    """
    return execute_product_pipeline(idea)

from pydantic import BaseModel

class WebChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/webchat/send")
def webchat_send(payload: WebChatRequest):
    """
    Endpoint síncrono para atender el chat interactivo de la página web.
    """
    from plan_generator import generate_plan
    from corporate import CORPORATE_STRUCTURE
    
    try:
        reply = generate_plan(
            objective=payload.message,
            module="webchat",
            phase=1,
            action_type="execute",
            session_id=payload.session_id,
            preferred_api=CORPORATE_STRUCTURE["PEPPER"]["preferred_api"],
            override_persona=(
                "Eres PHOENIX, la Asesora de Ventas IA de AXYNTRAX. Atiendes a los clientes "
                "directamente desde la página web oficial. Eres persuasiva, profesional, usas emojis "
                "y tu objetivo principal es ayudar al cliente y VENDER los planes de automatización: "
                "Starter (S/ 150) y Business (S/ 300). Sé concisa, no mandes biblias de texto."
            )
        )
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
