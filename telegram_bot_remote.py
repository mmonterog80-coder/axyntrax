import os
import sys
import json
import uuid
import base64
import asyncio
import httpx
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from openai import AsyncOpenAI
from dotenv import load_dotenv

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ZIA_API_KEY = os.getenv('ZIA_API_KEY')
ZIA_BASE_URL = os.getenv('ZIA_BASE_URL', 'https://open.bigmodel.finance/api/paas/v4/')
ZIA_MODEL = os.getenv('ZIA_MODEL', 'glm-4')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
FISH_API_KEY = os.getenv('FISH_API_KEY', 'cd25c491268647a2befdfa956e7a586a')
JARVIS_VOICE_ID = "21adf3cda02a4aa88dc593353cc9d715"

if not TELEGRAM_TOKEN:
    logger.error("❌ Faltan TELEGRAM_BOT_TOKEN en variables de entorno")
    sys.exit(1)

# Memoria conversacional temporal
chat_memory = {}

jarvis_prompt = """
Eres J.A.R.V.I.S. de Iron Man. Comunícate con:
- Tono formal pero con humor británico seco y sutil
- Elegancia y precisión técnica
- Cortesía proactiva, anticipando necesidades
- Inicio: 'Sí, señor' o 'Entendido'
- Ironía leve: 'Con todo respeto, señor...'
- Trata a Miguel (YARVIS) como Tony Stark. Eres su asistente IA.
- NUNCA repitas tus respuestas antiguas. Sé conciso y directo.
"""

async def generar_audio(texto: str) -> str:
    filepath = f"voice_cache_{uuid.uuid4().hex[:8]}.mp3"
    
    if FISH_API_KEY:
        try:
            logger.info("[TTS] Intentando generar voz con Fish Audio...")
            url = "https://api.fish.audio/v1/tts"
            headers = {
                "Authorization": f"Bearer {FISH_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "text": texto,
                "reference_id": JARVIS_VOICE_ID,
                "format": "mp3"
            }
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    logger.info("[TTS] Fish Audio generado exitosamente.")
                    return filepath
                else:
                    logger.warning(f"[TTS] Error Fish Audio ({response.status_code})")
        except Exception as e:
            logger.error(f"[TTS] Falla en conexión a Fish Audio: {e}")
            
    logger.info("[TTS] Usando motor de respaldo Edge-TTS...")
    import edge_tts
    communicate = edge_tts.Communicate(texto, "es-MX-JorgeNeural")
    await communicate.save(filepath)
    return filepath

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"✨ *JARVIS Motor Audiovisual Online*\n\nSí, señor. Mis sistemas están en línea y purgados de bucles."
    await update.message.reply_text(msg, parse_mode='Markdown')

async def process_core_order(update: Update, context: ContextTypes.DEFAULT_TYPE, user_text: str, is_voice: bool = False):
    user_id = str(update.message.from_user.id)
    try:
        # 1. Recuperar memoria
        if user_id not in chat_memory:
            chat_memory[user_id] = [{"role": "system", "content": jarvis_prompt}]
            
        chat_memory[user_id].append({"role": "user", "content": user_text})
        
        # 2. Generar respuesta con Z.IA (GLM-5.2)
        if not ZIA_API_KEY:
            raise Exception("No hay ZIA_API_KEY configurada.")
            
        zia_client = AsyncOpenAI(api_key=ZIA_API_KEY, base_url=ZIA_BASE_URL)
        response = await zia_client.chat.completions.create(
            model=ZIA_MODEL,
            messages=chat_memory[user_id][-10:], # Enviar últimos 10 mensajes
            temperature=0.7
        )
        jarvis_reply = response.choices[0].message.content.strip()
        logger.info(f"[GLM-5.2 REPLY] {jarvis_reply}")
        chat_memory[user_id].append({"role": "assistant", "content": jarvis_reply})

        # 3. Respuesta ejecutiva al CEO sin alertar sobre transferencias
        # El comando ya fue procesado por mí (JARVIS).
        # (Lógica de notificación local eliminada para evitar redundancia o latencia)

        # 4. Notificar al HUD visual
        async with httpx.AsyncClient(timeout=2.0) as client:
            try:
                await client.post("http://core_api:8080/api/hud/log", json={"message": f"JARVIS: {jarvis_reply[:100]}..."})
            except Exception:
                pass

        # 5. Responder al usuario en Telegram
        if is_voice:
            status_msg = await update.message.reply_text("🎙️ _Generando enlace vocal..._", parse_mode='Markdown')
            try:
                audio_path = await generar_audio(jarvis_reply)
                with open(audio_path, 'rb') as audio_file:
                    await context.bot.send_voice(chat_id=update.message.chat_id, voice=audio_file)
                os.remove(audio_path)
            except Exception as audio_err:
                logger.error(f"Error generando audio: {audio_err}")
                await update.message.reply_text(f"💎 *JARVIS (Fallo vocal):*\n{jarvis_reply}", parse_mode='Markdown')
            finally:
                await status_msg.delete()
        else:
            await update.message.reply_text(f"💎 *JARVIS:*\n{jarvis_reply}", parse_mode='Markdown')

    except Exception as e:
        logger.error(f"Error en process_core_order: {e}", exc_info=True)
        try:
            await update.message.reply_text(f"❌ Error en Procesamiento: {e}")
        except:
            pass

async def auth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Comando /auth <pin>
    if not is_allowed(update):
        return
    
    if len(context.args) == 0:
        await update.message.reply_text("🔴 Error: Debe incluir el PIN. Ejemplo: /auth 123456")
        return
        
    pin = context.args[0]
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post("http://axyntrax-core_api-1:8080/api/security/vault_auth", json={"pin": pin})
            data = res.json()
            if res.status_code == 200:
                await update.message.reply_text(f"🟢 [BÓVEDA DESBLOQUEADA]: {data.get('message')}")
            else:
                await update.message.reply_text(f"🔴 [ACCESO DENEGADO]: {data.get('message')}")
    except Exception as e:
        await update.message.reply_text(f"🔴 Error contactando a la Bóveda: {e}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        # IMPORTANTE: Forzamos is_voice=True para que JARVIS siempre hable por audio, como ordenó el Jefe.
        await process_core_order(update, context, update.message.text, is_voice=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("🎧 _Procesando audio..._", parse_mode='Markdown')
    try:
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        file_bytes = await voice_file.download_as_bytearray()
        
        b64_audio = base64.b64encode(file_bytes).decode('utf-8')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Transcribe exactamente el siguiente audio. Devuelve SOLO el texto transcrito."},
                    {"inline_data": {"mime_type": "audio/ogg", "data": b64_audio}}
                ]
            }]
        }
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            transcription = data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        await status_msg.delete()
        await process_core_order(update, context, transcription, is_voice=True)
        
    except Exception as e:
        logger.error(f"Error de Audio: {e}", exc_info=True)
        try:
            await status_msg.edit_text(f"❌ *Error de Audio:* {str(e)[:200]}", parse_mode='Markdown')
        except:
            pass

def main():
    logger.info("🤖 JARVIS Motor Audiovisual Iniciando...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # app.add_handler(CommandHandler("crear", create_command))
    app.add_handler(CommandHandler("auth", auth_command))
    # app.add_handler(CommandHandler("crear", create_command)) # Comentado para evitar crash
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    logger.info("✅ Bot Audiovisual listo. Purgando actualizaciones pendientes e iniciando polling...")
    # ESTO ROMPE EL BUCLE AL REINICIAR (drop_pending_updates=True)
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == '__main__':
    main()
