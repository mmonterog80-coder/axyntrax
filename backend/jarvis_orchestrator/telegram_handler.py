import os
import requests
from uuid import uuid4
import threading

from voice_generator import generar_audio, reproducir_audio
from state_manager import global_state

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_telegram_message(chat_id: int, text: str):
    """Envía un mensaje de Telegram al chat_id especificado."""
    if not TELEGRAM_TOKEN:
        return {"error": "Token de Telegram no configurado"}
        
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def send_telegram_voice(chat_id: int, audio_path: str):
    """Envía una nota de voz a Telegram."""
    if not TELEGRAM_TOKEN or not os.path.exists(audio_path):
        return {"error": "Token o archivo no disponible"}
    url = f"{TELEGRAM_API_URL}/sendVoice"
    try:
        with open(audio_path, 'rb') as voice_file:
            response = requests.post(url, data={'chat_id': chat_id}, files={'voice': voice_file})
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return {"error": str(e)}

def download_telegram_file(file_id: str, save_path: str):
    """Descarga un archivo desde los servidores de Telegram."""
    url = f"{TELEGRAM_API_URL}/getFile?file_id={file_id}"
    r = requests.get(url)
    if r.status_code == 200:
        file_path = r.json().get("result", {}).get("file_path")
        if file_path:
            download_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_path}"
            r_down = requests.get(download_url)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(r_down.content)
            return True
    return False

def process_telegram_update(update: dict):
    """Procesa un webhook entrante desde Telegram (Texto, Foto o Video)."""
    message = update.get("message")
    if not message:
        return
    
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")
    
    allowed_chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
    if allowed_chat_id and str(chat_id) != allowed_chat_id:
        print(f"⚠️ Intento de acceso no autorizado desde chat_id: {chat_id}")
        return
    
    if not allowed_chat_id:
        print(f"NUEVO CHAT DETECTADO. Guarda este numero en TELEGRAM_ALLOWED_CHAT_ID: {chat_id}")

    if chat_id:
        # 1. INTERCEPTOR MULTIMODAL (Fotos y Videos)
        file_id = None
        media_type = None
        extension = "jpg"
        
        if "photo" in message:
            # photo es un array de resoluciones, tomamos la más alta
            file_id = message["photo"][-1]["file_id"]
            media_type = "image"
        elif "video" in message:
            file_id = message["video"]["file_id"]
            media_type = "video"
            extension = "mp4"
            
        if file_id:
            msg = "👁️ Ojos activados. Descargando y visualizando el material. Dame un momento, señor."
            send_telegram_message(chat_id, msg)
            audio_path = generar_audio(msg.replace("👁️ ", ""))
            if audio_path and not audio_path.startswith("[Error"):
                send_telegram_voice(chat_id, audio_path)
                
            def process_media_bg():
                try:
                    from multimodal_analyzer import procesar_multimedia
                    save_path = os.path.join(os.path.dirname(__file__), "..", "tmp_media", f"{uuid4()}.{extension}")
                    if download_telegram_file(file_id, save_path):
                        resumen = procesar_multimedia(save_path, media_type=media_type)
                        send_telegram_message(chat_id, resumen)
                        
                        # Generar y enviar voz del resumen (solo los primeros 500 caracteres para no saturar)
                        texto_voz = resumen.replace("*", "").replace("👁️", "")[:500] + "... Fin del resumen."
                        audio_resumen_path = generar_audio(texto_voz)
                        if audio_resumen_path and not audio_resumen_path.startswith("[Error"):
                            send_telegram_voice(chat_id, audio_resumen_path)
                            
                        # Limpiar disco
                        try:
                            os.remove(save_path)
                        except:
                            pass
                    else:
                        send_telegram_message(chat_id, "❌ Error al descargar el material de Telegram.")
                except Exception as e:
                    send_telegram_message(chat_id, f"❌ Error procesando multimedia: {e}")
                    
            threading.Thread(target=process_media_bg).start()
            return
            
        # 2. INTERCEPTOR DE TEXTO TRADICIONAL
        if text:
            handle_incoming_message(chat_id, text)

def handle_incoming_message(chat_id: int, text: str):
    """Manejo de texto clásico."""
    text_lower = text.lower()
    if "qué están haciendo" in text_lower or "que estan haciendo" in text_lower or text_lower in ["status", "estado"]:
        pc_status = "🟢 ONLINE" if global_state.is_pc_online() else "🔴 OFFLINE"
        response = (
            f"📊 **REPORTE DE ESTADO CORPORATIVO** 📊\n\n"
            f"💻 **PC Local (Edge):** {pc_status}\n"
            f"☁️ **Nube (Railway):** {global_state.cloud_status}\n\n"
            f"🤖 **IA a cargo:** {global_state.active_ai}\n"
            f"🎯 **Misión actual:** {global_state.active_project}"
        )
        send_telegram_message(chat_id, response)
        
        texto_voz = "Reporte de estado corporativo. " + ("Sistemas locales en línea. " if global_state.is_pc_online() else "Sistemas locales fuera de línea. ") + f"Inteligencia a cargo: {global_state.active_ai}."
        audio_path = generar_audio(texto_voz)
        if audio_path and not audio_path.startswith("[Error"):
            send_telegram_voice(chat_id, audio_path)
        return

    response = f"🤖 JARVIS AX: Recibí tu orden: '{text}'. Procesando..."
    send_telegram_message(chat_id, response)
    
    # Enviar voz de confirmación
    audio_conf = generar_audio("Recibí tu orden, procesando de inmediato señor.")
    if audio_conf and not audio_conf.startswith("[Error"):
        send_telegram_voice(chat_id, audio_conf)
    
    try:
        if not os.getenv("RAILWAY_ENVIRONMENT"):
            reproducir_audio("Recibí tu orden, procesando de inmediato señor.")
    except:
        pass
    
    def create_task_bg():
        payload = {
            "session_id": str(uuid4()),
            "origin": "telegram",
            "task": {
                "phase": 1,
                "module": "chat",
                "action_type": "execute",
                "objective": text,
                "context": {
                    "model_preference": "deepseek-coder",
                    "files_allowed": [],
                    "risk_level": "low"
                }
            }
        }
        try:
            orchestrator_url = os.getenv("ORCHESTRATOR_URL", "http://localhost:8000")
            r = requests.post(f"{orchestrator_url}/tasks/", json=payload, timeout=30)
            if r.status_code == 201:
                plan = r.json().get("plan", "Sin plan generado")
                send_telegram_message(chat_id, f"📋 Plan generado por JARVIS:\n{plan}\n\n⚙️ Ejecutando...")
                
                import re
                texto_limpio = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ.,;:!? \n]', '', plan)
                texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
                
                # Si es muy largo, cortarlo para que la nota de voz no demore mucho
                if len(texto_limpio) > 800:
                    texto_limpio = texto_limpio[:800] + "... Fin del reporte principal."
                    
                audio_plan = generar_audio(texto_limpio)
                if audio_plan and not audio_plan.startswith("[Error"):
                    send_telegram_voice(chat_id, audio_plan)
            else:
                send_telegram_message(chat_id, f"❌ Error del orquestador: {r.text}")
        except Exception as e:
            send_telegram_message(chat_id, f"❌ Error interno al contactar orquestador: {e}")

    threading.Thread(target=create_task_bg).start()
