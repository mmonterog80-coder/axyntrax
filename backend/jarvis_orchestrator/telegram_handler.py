import logging
import os
import requests
from fastapi import HTTPException

logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

def send_telegram_message(chat_id: str, text: str):
    """Envía un mensaje de texto simple al chat de Telegram."""
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        logger.error(f"Error enviando mensaje a Telegram: {e}")

def process_telegram_update(update: dict):
    """Procesa una actualización entrante de Telegram."""
    try:
        if "message" not in update:
            return
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        
        # Aquí va la lógica de JARVIS para responder.
        # En esta versión siempre contesta con texto.
        respuesta = "Recibí tu mensaje. JARVIS AX está operativo."
        send_telegram_message(chat_id, respuesta)
    except Exception as e:
        logger.error(f"Error procesando update: {e}")
        raise HTTPException(status_code=500, detail="Error interno procesando Telegram")