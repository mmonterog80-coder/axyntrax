from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
import os
import requests
import json
from reasoning_engine import run_chain_of_thought
# Asumiendo que el Secrets Broker ya maneja el fetch, pero para velocidad del Webhook:
# Usaremos las variables de entorno directamente si el broker tarda.

router = APIRouter()

META_VERIFY_TOKEN = os.environ.get("META_VERIFY_TOKEN", "JARVIS_AX_IG_WEBHOOK_SECRET")
META_PAGE_ACCESS_TOKEN = os.environ.get("META_PAGE_ACCESS_TOKEN", "")

# ---------------------------------------------------------
# AXYNTRAX SALESBOT - WEBHOOK DE WHATSAPP / INSTAGRAM
# ---------------------------------------------------------

@router.get("/webhook/whatsapp")
async def verify_webhook(request: Request):
    """
    Punto de verificación para Meta (Facebook/WhatsApp).
    Meta envía un hub.challenge que debemos devolver si el token coincide.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == META_VERIFY_TOKEN:
            print("WEBHOOK DE META VERIFICADO CON ÉXITO")
            return int(challenge)
        else:
            raise HTTPException(status_code=403, detail="Verify token mismatch")
    return "AXYNTRAX Webhook Online"

@router.post("/webhook/whatsapp")
async def receive_message(request: Request):
    """
    Recepción de mensajes en tiempo real desde clientes potenciales.
    Zia y Gemini procesarán el mensaje y responderán para cerrar la venta.
    """
    try:
        body = await request.json()
        print(f"[NUEVO MENSAJE B2B]: {json.dumps(body, indent=2)}")
        
        # Parseo básico del payload de WhatsApp Business API
        if body.get("object"):
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    if "messages" in value:
                        for msg in value["messages"]:
                            sender_id = msg.get("from")
                            text = msg.get("text", {}).get("body", "")
                            
                            print(f"-> Cliente {sender_id} dice: {text}")
                            
                            # 1. ORQUESTACIÓN COGNITIVA (Zia + Gemini)
                            task_desc = f"El cliente {sender_id} acaba de enviar un mensaje a la empresa: '{text}'. Eres AXYNTRAX SalesBot. Redacta una respuesta vendedora y persuasiva B2B."
                            reasoning_result = run_chain_of_thought(task_desc)
                            
                            # Usamos la "strategy" de Gemini como respuesta
                            reply_text = reasoning_result.get("strategy", "Hola, soy el asistente autónomo de AXYNTRAX. En breve lo atenderemos.")
                            
                            # 2. ENVIAR RESPUESTA VÍA API DE WHATSAPP
                            send_whatsapp_message(sender_id, reply_text)
                            
        return {"status": "ok"}
    except Exception as e:
        print("Error procesando mensaje de Meta:", e)
        return {"status": "error"}

def send_whatsapp_message(phone_number: str, message: str):
    """Envía la respuesta al cliente usando la Graph API de Meta"""
    if not META_PAGE_ACCESS_TOKEN:
        print("ERROR: META_PAGE_ACCESS_TOKEN no está configurado.")
        return

    # IMPORTANTE: Reemplaza "YOUR_PHONE_NUMBER_ID" con el ID real provisto por Meta
    phone_number_id = os.environ.get("META_PHONE_NUMBER_ID", "TEST_ID") 
    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {META_PAGE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }
    
    try:
        # En producción esto dispararía el POST real.
        # response = requests.post(url, headers=headers, json=data)
        # print("Mensaje enviado:", response.status_code)
        print(f"[SIMULACRO ENVÍO WHATSAPP] A {phone_number}: {message}")
    except Exception as e:
        print(f"Error al enviar mensaje de WhatsApp: {e}")
