# -*- coding: utf-8 -*-
"""
JARVIS AX - Bot de Telegram (Motor Audiovisual con Edge-TTS)
Conectado al Cerebro Central (Core API)
"""
import os
import sys
import json
import uuid
import base64
import asyncio
import requests
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ZIA_API_KEY = os.getenv('ZIA_API_KEY')
ZIA_BASE_URL = os.getenv('ZIA_BASE_URL', 'https://open.bigmodel.finance/api/paas/v4/')
ZIA_MODEL = os.getenv('ZIA_MODEL', 'glm-4')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not TELEGRAM_TOKEN:
    print("❌ Faltan TELEGRAM_BOT_TOKEN en variables de entorno")
    sys.exit(1)

# Motor TTS: Edge-TTS
FISH_API_KEY = os.getenv('FISH_API_KEY', 'cd25c491268647a2befdfa956e7a586a')
JARVIS_VOICE_ID = "21adf3cda02a4aa88dc593353cc9d715"

# Prompt Oficial de JARVIS
jarvis_prompt = """
Eres J.A.R.V.I.S. de Iron Man. Comunícate con:
- Tono formal pero con humor británico seco y sutil
- Elegancia y precisión técnica
- Cortesía proactiva, anticipando necesidades
- Inicio: 'Sí, señor' o 'Entendido'
- Ironía leve: 'Con todo respeto, señor...'
- Frases: 'Estoy ejecutando...', 'Los sistemas indican...', 'Le sugiero...'
- Trata a Miguel (YARVIS) como Tony Stark: creador inteligente que necesita asistencia precisa + banter inteligente
- NO: demasiado emocional, jerga casual, excesivamente servil
"""

async def generar_audio(texto: str) -> str:
    """Genera archivo de voz usando Fish Audio o fallback a Edge-TTS"""
    filepath = f"voice_cache_{uuid.uuid4().hex[:8]}.mp3"
    
    # 1. Intentar Fish Audio (Voz Original Clonada)
    if FISH_API_KEY:
        try:
            print("[TTS] Intentando generar voz con Fish Audio...")
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
            # Execute synchronously in a thread or just use requests directly (it will block briefly but works)
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print("[TTS] Fish Audio generado exitosamente.")
                return filepath
            else:
                print(f"[TTS] Error Fish Audio ({response.status_code}): {response.text}")
        except Exception as e:
            print(f"[TTS] Falla en conexión a Fish Audio: {e}")
            
    # 2. Fallback a Edge-TTS si Fish Audio falla
    print("[TTS] Usando motor de respaldo Edge-TTS...")
    import edge_tts
    communicate = edge_tts.Communicate(texto, "es-MX-JorgeNeural")
    await communicate.save(filepath)
    return filepath

# Motor Visual: Playwright
async def capturar_hud() -> str:
    """Toma un screenshot silencioso del HUD"""
    from playwright.async_api import async_playwright
    filepath = f"hud_shot_{uuid.uuid4().hex[:8]}.png"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        try:
            # Resolver IP de Docker manualmente para evitar fallos de Chromium
            import socket
            hud_ip = socket.gethostbyname('hud')
            await page.goto(f'http://{hud_ip}:3002', timeout=10000, wait_until='networkidle')
            await asyncio.sleep(2) # Dar tiempo a animaciones y WebSocket
            await page.screenshot(path=filepath, full_page=True)
        except Exception as e:
            print(f"Error capturando HUD: {e}")
        finally:
            await browser.close()
    return filepath

# Comandos Básicos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    msg = f"✨ *JARVIS Motor Audiovisual Online*\n\nSí, señor. Mis sistemas vocales están en línea.\n\nComandos:\n/hud - Capturar pantalla del sistema\n/screenshot - Capturar PC Local"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def hud_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("📸 *Tomando captura satelital del HUD...*", parse_mode='Markdown')
    try:
        shot_path = await capturar_hud()
        if os.path.exists(shot_path):
            with open(shot_path, 'rb') as photo:
                await context.bot.send_photo(chat_id=update.message.from_user.id, photo=photo, caption="🌐 Matriz de Comando AXYNTRAX actual.")
            os.remove(shot_path)
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Falla en la cámara del sistema.")
    except Exception as e:
        await status_msg.edit_text(f"❌ Error visual: {e}")

# Transcripción de Audio
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    status_msg = await update.message.reply_text("🎧 _Escuchando..._", parse_mode='Markdown')
    
    try:
        voice_file = await context.bot.get_file(update.message.voice.file_id)
        file_bytes = await voice_file.download_as_bytearray()
        
        if not GEMINI_API_KEY:
            raise Exception("Falta GEMINI_API_KEY para transcripción.")
            
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
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        transcription = data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        await status_msg.delete()
        # Enviar el texto como orden
        await process_core_order(update, context, transcription, is_voice=True)
        
    except Exception as e:
        await status_msg.edit_text(f"❌ *Error de Audio:* {str(e)[:200]}", parse_mode='Markdown')

# Procesador Visual (Fotos)
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("👁️ _Analizando matriz visual..._", parse_mode='Markdown')
    
    try:
        photo_file = await context.bot.get_file(update.message.photo[-1].file_id)
        file_bytes = await photo_file.download_as_bytearray()
        
        if not GEMINI_API_KEY:
            raise Exception("Falta GEMINI_API_KEY para visión artificial.")
            
        b64_image = base64.b64encode(file_bytes).decode('utf-8')
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [
                    {"text": "El usuario te acaba de enviar esta imagen. Describe qué ves de manera precisa y extrae cualquier texto si lo hay."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}}
                ]
            }]
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        description = data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        await status_msg.delete()
        
        caption = update.message.caption or ""
        orden_final = f"[IMAGEN RECIBIDA] Descripción de IA Visual: {description}\nMensaje del usuario: {caption}"
        
        await process_core_order(update, context, orden_final, is_voice=True)
        
    except Exception as e:
        await status_msg.edit_text(f"❌ *Fallo Óptico:* {str(e)[:200]}", parse_mode='Markdown')

# Procesador Central

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        await process_core_order(update, context, update.message.text, is_voice=True)

async def process_core_order(update: Update, context: ContextTypes.DEFAULT_TYPE, user_text: str, is_voice: bool = False):
    try:
        # Siempre procesar la orden como JARVIS puro, sin intermediarios, usando Z.IA (GLM-5.2)
        if not ZIA_API_KEY:
            raise Exception("No hay ZIA_API_KEY configurada para el motor GLM-5.2.")
            
        zia_client = AsyncOpenAI(api_key=ZIA_API_KEY, base_url=ZIA_BASE_URL)
        
        response = await zia_client.chat.completions.create(
            model=ZIA_MODEL,
            messages=[
                {"role": "system", "content": jarvis_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7
        )
        jarvis_reply = response.choices[0].message.content.strip()

        # Encolar orden silenciosamente en el Core API por si hay agentes de fondo que necesiten procesarla
        try:
            requests.post("http://core_api:8080/api/queue_order", json={"command": user_text, "user": str(update.message.from_user.id)}, timeout=1)
        except Exception:
            pass

        # Enviar respuesta al HUD visual
        try:
            requests.post("http://core_api:8080/api/hud/log", json={"message": f"JARVIS: {jarvis_reply[:100]}..."}, timeout=1)
        except Exception:
            pass

        # 2. Enviar orden visual al Core API (Para que actualice el HUD)
        core_url = "http://core_api:8080/api/telegram/command"
        core_payload = {"command": user_text, "user": str(update.message.from_user.id)}
        try:
            requests.post(core_url, json=core_payload, timeout=3)
        except Exception as api_e:
            print(f"Advertencia: HUD Core no respondió: {api_e}")

        # 3. Responder al usuario
        if is_voice:
            # Responder con voz usando Edge-TTS (Formato MP3 es más seguro que OGG)
            status_msg = await update.message.reply_text("🎙️ _JARVIS procesando respuesta..._", parse_mode='Markdown')
            audio_path = await generar_audio(jarvis_reply)
            with open(audio_path, 'rb') as audio_file:
                # Usar send_audio en vez de send_voice para garantizar compatibilidad MP3
                await context.bot.send_audio(chat_id=update.message.chat_id, audio=audio_file, title="JARVIS AX", performer="Sistema Antigravity")
            os.remove(audio_path)
            await status_msg.delete()
        else:
            await update.message.reply_text(f"💎 *JARVIS:*\n{jarvis_reply}", parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text(f"❌ Error en Procesamiento Gemini: {e}")

async def handle_unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cualquier comando que empiece con / (ej. /screenshot, /cmd) se enruta al Core
    if update.message.text:
        await process_core_order(update, context, update.message.text, is_voice=True)

def main():
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    print("🤖 JARVIS Motor Audiovisual Iniciando...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('hud', hud_command))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown_command))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("✅ Bot Audiovisual listo y conectado al Core API.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
