from fastapi import APIRouter, HTTPException
from models import TaskCreate, TaskResponse, TaskStatus
from db import create_task, get_task, update_task_status, get_next_pending_task
import os
from whatsapp_handler import process_whatsapp_message, handle_incoming_message

router = APIRouter()

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
def update_task(task_id: str, status: TaskStatus, error_details: str = None, result: str = None):
    updated = update_task_status(task_id, status.value, result, error_details)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return updated

@router.post("/whatsapp/webhook")
def whatsapp_webhook(body: dict):
    """
    Endpoint que recibe los mensajes de WhatsApp desde Meta.
    """
    from_number, text = process_whatsapp_message(body)
    if from_number and text:
        # Crear una tarea en segundo plano (podríamos usar BackgroundTasks)
        # Por simplicidad, respondemos inmediatamente y procesamos después
        handle_incoming_message(from_number, text)
        return {"status": "processed"}
    return {"status": "ignored"}

@router.get("/whatsapp/webhook")
def verify_webhook(hub_mode: str = None, hub_challenge: str = None, hub_verify_token: str = None):
    """
    Verificación del webhook para Meta (requiere token de verificación).
    """
    VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "jarvis_ax_verify")
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge) if hub_challenge else "ok"
    return "Verification failed", 403
