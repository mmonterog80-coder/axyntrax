import os
import requests
import threading
from uuid import uuid4
from voice_generator import reproducir_audio

def verify_webhook(mode: str, token: str, challenge: str):
    """Verifica el webhook de Meta usando el META_VERIFY_TOKEN."""
    verify_token = os.getenv("META_VERIFY_TOKEN")
    if mode == "subscribe" and token == verify_token:
        print("[*] Webhook de Instagram verificado exitosamente.")
        return int(challenge)
    return False

def send_instagram_message(recipient_id: str, text: str):
    """Envia un DM de respuesta usando la API de Meta."""
    page_access_token = os.getenv("META_PAGE_ACCESS_TOKEN")
    if not page_access_token:
        print("[!] Token de acceso a Meta no configurado.")
        return {"error": "META_PAGE_ACCESS_TOKEN no configurado"}
        
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={page_access_token}"
    
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[!] Error enviando mensaje por IG: {e}")
        return {"error": str(e)}

def process_instagram_update(body: dict):
    """Extrae la informacion del webhook entrante de Instagram."""
    if body.get("object") == "instagram":
        entries = body.get("entry", [])
        for entry in entries:
            messaging_events = entry.get("messaging", [])
            for event in messaging_events:
                if "message" in event and "text" in event["message"]:
                    sender_id = event["sender"]["id"]
                    text = event["message"]["text"]
                    handle_incoming_message(sender_id, text)

def handle_incoming_message(sender_id: str, text: str):
    """Procesa el mensaje de IG y lo envia al orquestador."""
    print(f"[*] Mensaje de Instagram recibido: {text}")
    
    # Respuesta automatica inicial
    response = f"🤖 JARVIS AX: Procesando orden desde IG: '{text}'..."
    send_instagram_message(sender_id, response)
    
    # Reproducir en la PC local
    try:
        reproducir_audio(f"Mensaje de Instagram: {text}")
    except Exception:
        pass
        
    def create_task_bg():
        import uuid
        # Crear un UUID consistente basado en el sender_id para tener memoria a largo plazo (CRM)
        persistent_session_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(sender_id)))
        
        payload = {
            "session_id": persistent_session_id,
            "origin": "instagram",
            "task": {
                "phase": 1,
                "module": "chat",
                "action_type": "execute",
                "objective": text,
                "context": {
                    "model_preference": "deepseek-coder",
                    "files_allowed": [],
                    "risk_level": "low",
                    "ig_sender_id": sender_id
                }
            }
        }
        try:
            orchestrator_url = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")
            r = requests.post(f"{orchestrator_url}/tasks/", json=payload, timeout=30)
            if r.status_code == 201:
                plan = r.json().get("plan", "Sin plan generado")
                send_instagram_message(sender_id, f"📋 Plan JARVIS:\n{plan}\n\n⚙️ Ejecutando...")
                try:
                    reproducir_audio(plan)
                except:
                    pass
            else:
                send_instagram_message(sender_id, f"❌ Error del orquestador: {r.text}")
        except Exception as e:
            send_instagram_message(sender_id, f"❌ Error interno al contactar orquestador: {e}")

    threading.Thread(target=create_task_bg).start()
