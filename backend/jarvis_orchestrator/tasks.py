from fastapi import APIRouter, HTTPException
from models import TaskCreate, TaskResponse, TaskStatus
from db import create_task, get_task, update_task_status, get_next_pending_task
import os
from telegram_handler import process_telegram_update, send_telegram_message

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
    result = send_telegram_message(chat_id, text)
    return result
