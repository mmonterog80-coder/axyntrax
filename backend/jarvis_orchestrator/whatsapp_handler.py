import os
import requests

WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v19.0/{WHATSAPP_PHONE_ID}/messages"

def send_whatsapp_message(to_number: str, text: str) -> dict:
    """Envía un mensaje de WhatsApp al número especificado."""
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "text",
        "text": {"body": text}
    }
    try:
        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_whatsapp_message(body: dict) -> tuple:
    """
    Procesa un mensaje entrante de WhatsApp.
    Retorna (from_number, message_text).
    """
    try:
        entry = body.get("entry", [])[0]
        change = entry.get("changes", [])[0]
        message = change.get("value", {}).get("messages", [])[0]
        from_number = message.get("from")
        text = message.get("text", {}).get("body", "")
        return from_number, text
    except (IndexError, KeyError, TypeError):
        return None, None

def handle_incoming_message(from_number: str, text: str):
    """
    Aquí se conecta con el orquestador.
    Por ahora, un eco inteligente que crea una tarea.
    """
    # Podríamos llamar a POST /tasks internamente o importar create_task
    response_text = f"🤖 JARVIS AX recibió tu mensaje: '{text}'. Estoy procesando tu solicitud."
    send_whatsapp_message(from_number, response_text)
