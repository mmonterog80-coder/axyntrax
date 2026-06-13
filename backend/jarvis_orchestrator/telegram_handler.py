import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_telegram_message(chat_id: int, text: str):
    """Envía un mensaje de Telegram al chat_id especificado."""
    if not TELEGRAM_TOKEN:
        return {"error": "Token de Telegram no configurado"}
        
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_telegram_update(update: dict):
    """Procesa un webhook entrante desde Telegram."""
    message = update.get("message")
    if not message:
        return
    
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    
    # Seguridad: Solo responder si el chat_id es el permitido (o si aún no se ha configurado ninguno)
    allowed_chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
    if allowed_chat_id and str(chat_id) != allowed_chat_id:
        print(f"⚠️ Intento de acceso no autorizado desde chat_id: {chat_id}")
        return
    
    # Si es el primer mensaje y no hay chat_id configurado, lo mostramos en consola para que el admin lo guarde
    if not allowed_chat_id:
        print(f"🔐 NUEVO CHAT DETECTADO. Si eres tú, copia este número en TELEGRAM_ALLOWED_CHAT_ID: {chat_id}")

    if chat_id and text:
        handle_incoming_message(chat_id, text)

def handle_incoming_message(chat_id: int, text: str):
    """Aquí conectaremos con el orquestador."""
    response = f"🤖 JARVIS AX (Telegram) recibió tu mensaje: '{text}'. Estoy procesando tu solicitud."
    send_telegram_message(chat_id, response)
