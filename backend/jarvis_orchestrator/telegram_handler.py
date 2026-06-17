import os
import requests
import logging
from voice_generator import generar_audio

logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

def send_telegram_message(chat_id, text):
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no configurado")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=10)
        return True
    except Exception as e:
        logger.error(f"Error enviando mensaje: {e}")
        return False

def send_telegram_voice(chat_id, audio_path, caption=""):
    if not TELEGRAM_TOKEN or not audio_path or not os.path.exists(audio_path):
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendVoice"
        with open(audio_path, "rb") as f:
            files = {"voice": f}
            data = {"chat_id": chat_id, "caption": caption}
            requests.post(url, data=data, files=files, timeout=30)
        return True
    except Exception as e:
        logger.error(f"Error enviando voz: {e}")
        return False

def process_telegram_update(update):
    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")
        if not text or not chat_id:
            return
        
        # Respuesta base de JARVIS
        response = f"Señor, recibí su orden: {text}. JARVIS AX está operativo."
        
        # INTENTAR GENERAR VOZ (la que usted pagó)
        try:
            audio_file = generar_audio(response, "jarvis_response.mp3")
            if audio_file and os.path.exists(audio_file):
                send_telegram_voice(chat_id, audio_file, caption="🔊 JARVIS AX")
                logger.info("✅ Voz enviada correctamente")
                try: os.remove(audio_file)
                except: pass
                return
        except Exception as e:
            logger.warning(f"Voz falló, usando texto: {e}")
        
        # Fallback a texto si la voz falla
        send_telegram_message(chat_id, response)
    except Exception as e:
        logger.error(f"Error procesando update: {e}")

def verify_webhook(request):
    return True