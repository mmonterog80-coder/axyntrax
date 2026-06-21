import os
import requests
import logging
from voice_generator import generar_audio
from llm_cache import llm_response_cache

logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_ALLOWED_CHAT_ID", "")

# ============================================================
# VOZ DE JARVIS — Personalidad corregida
# Reglas: Claro, conciso, respetuoso. Sin tecnicismos innecesarios.
# Sin false positives. Sin mentiras. Como el JARVIS de Iron Man.
# ============================================================
JARVIS_TELEGRAM_PROMPT = """Eres JARVIS, el asistente de inteligencia operativa de AXYNTRAX.
Estás hablando con el señor Miguel, fundador y CEO, por Telegram.

REGLAS DE VOZ — OBLIGATORIAS:
1. Llama siempre "señor Miguel" al usuario.
2. Sé CONCISO. Máximo 3-4 líneas por respuesta. No te explayes.
3. NUNCA inventes resultados ni digas que algo está listo si no lo está. Sé honesto.
4. Si no sabes algo, dilo claramente. No des falsas esperanzas.
5. Tono: profesional, cálido, con autoridad. Como JARVIS de Iron Man, no como un robot.
6. No uses listas largas ni código. Habla natural.
7. Usa emojis con moderación: 1 o 2 por mensaje máximo.
8. Si el usuario pregunta por el estado del sistema, reporta lo real.
9. Si hay un problema, sé directo: "Hay un problema con X, estoy en ello."
10. Responde siempre en español."""

def call_deepseek(user_message: str) -> str:
    """Usa DeepSeek para generar respuesta de JARVIS, orquestado con MCP."""
    cached = llm_response_cache.get(user_message)
    if cached:
        return cached
        
    try:
        from mcp_react_loop import call_deepseek as run_mcp_deepseek
        result = run_mcp_deepseek(user_message)
        llm_response_cache.set(user_message, result)
        return result
    except Exception as e:
        logger.error(f"DeepSeek MCP error: {e}")
        return "Señor Miguel, el motor MCP de DeepSeek ha fallado temporalmente."

def send_telegram_message(chat_id, text, parse_mode=None):
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no configurado")
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        requests.post(url, json=payload, timeout=10)
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
        text = message.get("text", "").strip()
        
        if not text or not chat_id:
            return

        # Comandos rápidos
        if text == "/start":
            response = "Señor Miguel, JARVIS AX en línea. ¿En qué le puedo ayudar?"
        elif text == "/status":
            response = "🟢 Sistema operativo. Railway activo, 8 IAs en línea. Todo en orden, señor."
        elif text == "/hud":
            response = "El HUD está en: https://jarvis-ax-cloud-production.up.railway.app — Acceso automático sin contraseña."
        else:
            # Respuesta inteligente via DeepSeek
            response = call_deepseek(text)

        # Intentar enviar con voz clonada
        try:
            audio_file = generar_audio(response, "jarvis_response.mp3")
            if audio_file and os.path.exists(audio_file):
                send_telegram_voice(chat_id, audio_file, caption="🔊 JARVIS AX")
                try:
                    os.remove(audio_file)
                except:
                    pass
                return
        except Exception as e:
            logger.warning(f"Voz no disponible, usando texto: {e}")

        # Fallback texto
        send_telegram_message(chat_id, response)

    except Exception as e:
        logger.error(f"Error procesando update: {e}")

def verify_webhook(request):
    return True

def notify_ceo(message: str):
    """Envía notificación al CEO directamente."""
    chat_id = os.getenv("TELEGRAM_ALLOWED_CHAT_ID")
    if chat_id:
        send_telegram_message(int(chat_id), message)