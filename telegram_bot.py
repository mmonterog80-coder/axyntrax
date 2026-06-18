# -*- coding: utf-8 -*-
"""
JARVIS AX - Bot de Telegram REAL
Funciona con DeepSeek, memoria básica y router de intención
"""
import os
import sys
from datetime import datetime
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from openai import OpenAI

# Configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
FISH_API_KEY = os.getenv('FISH_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not TELEGRAM_TOKEN or not DEEPSEEK_API_KEY:
    print("❌ Faltan TELEGRAM_BOT_TOKEN o DEEPSEEK_API_KEY en variables de entorno")
    sys.exit(1)

# Cliente DeepSeek
deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url='https://api.deepseek.com')

# Cliente Supabase (opcional)
supabase = None
try:
    from supabase import create_client
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase conectado")
except Exception as e:
    print(f"⚠️ Supabase no disponible: {e}")

# Memoria simple en memoria (por usuario)
user_memory = {}

# Router de intención
def detect_rubric(message):
    """Detecta de qué rubro habla el usuario"""
    message_lower = message.lower()
    
    vet_keywords = ['veterinaria', 'mascota', 'perro', 'gato', 'cita veterinaria', 'vacuna', 'pet', 'animal']
    legal_keywords = ['abogado', 'legal', 'demanda', 'contrato', 'juicio', 'caso', 'cliente legal']
    dental_keywords = ['dental', 'dentista', 'odontologia', 'muela', 'diente', 'ortodoncia', 'limpieza dental']
    
    for kw in vet_keywords:
        if kw in message_lower:
            return 'veterinario'
    for kw in legal_keywords:
        if kw in message_lower:
            return 'legal'
    for kw in dental_keywords:
        if kw in message_lower:
            return 'dental'
    
    return 'general'

# Prompts por rubro
PROMPTS = {
    'veterinario': 'Eres JARVIS AX especializado en gestión veterinaria (VetManager). Ayudas con agenda de citas, historial de mascotas, vacunas, recetas y facturación. Responde en español, conciso y profesional.',
    'legal': 'Eres JARVIS AX especializado en gestión legal (LegalDesk). Ayudas con gestión de casos, plazos procesales, documentos legales y facturación por horas. Responde en español, preciso y formal.',
    'dental': 'Eres JARVIS AX especializado en gestión dental (DentalFlow). Ayudas con agenda, odontograma, planes de tratamiento, presupuestos y recordatorios. Responde en español, claro y empático.',
    'general': 'Eres JARVIS AX, asistente IA empresarial de AXYNTRAX Automation. Responde profesional, útil y conciso en español.'
}

# Comandos
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    
    msg = f"🤖 *JARVIS AX Online*\n\n"
    msg += f"Hola {user_name}, soy tu asistente IA.\n\n"
    msg += "*Comandos:*\n"
    msg += "/estado - Ver sistema\n"
    msg += "/ayuda - Esta ayuda\n"
    msg += "/vet - Modo veterinario\n"
    msg += "/legal - Modo legal\n"
    msg += "/dental - Modo dental\n\n"
    msg += "Escríbeme normalmente y detecto el rubro automáticamente."
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def estado_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "✅ *Sistema Operativo*\n\n"
    msg += "🤖 Bot Telegram: Activo\n"
    msg += "🧠 DeepSeek: Conectado\n"
    msg += "️ Supabase: " + ("Conectado" if supabase else "No disponible") + "\n"
    msg += "🎤 Fish Audio: " + ("Configurado" if FISH_API_KEY else "No configurado") + "\n\n"
    msg += "_Respuesta inteligente activa_"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str):
    user_id = update.message.from_user.id
    user_memory[user_id] = mode
    mode_names = {'vet': 'Veterinario', 'legal': 'Legal', 'dental': 'Dental'}
    await update.message.reply_text(f"✅ Modo cambiado a: *{mode_names.get(mode, mode)}*", parse_mode='Markdown')

async def vet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, 'vet')

async def legal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, 'legal')

async def dental_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await set_mode(update, context, 'dental')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text
    
    if not user_message or not user_message.strip():
        return
    
    # Detectar rubro (manual o automático)
    rubric = user_memory.get(user_id, 'general')
    if rubric == 'general':
        rubric = detect_rubric(user_message)
    
    # Construir prompt con contexto
    system_prompt = PROMPTS.get(rubric, PROMPTS['general'])
    
    # Agregar memoria reciente si existe
    recent = user_memory.get(f'{user_id}_history', [])
    if recent:
        system_prompt += "\n\nContexto reciente de la conversación:\n"
        for msg in recent[-5:]:
            system_prompt += f"- {msg}\n"
    
    try:
        # Llamar a DeepSeek
        response = deepseek.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        jarvis_response = response.choices[0].message.content
        
        # Guardar en memoria
        if f'{user_id}_history' not in user_memory:
            user_memory[f'{user_id}_history'] = []
        user_memory[f'{user_id}_history'].append(f"User: {user_message}")
        user_memory[f'{user_id}_history'].append(f"JARVIS: {jarvis_response}")
        user_memory[f'{user_id}_history'] = user_memory[f'{user_id}_history'][-10:]
        
        # Enviar respuesta
        await update.message.reply_text(jarvis_response)
        
        # Guardar en Supabase si está disponible
        if supabase:
            try:
                supabase.table('qwen_results').insert({
                    'order_type': f'chat_{rubric}',
                    'payload': {'user': user_id, 'message': user_message[:500], 'response': jarvis_response[:500]},
                    'status': 'success'
                }).execute()
            except Exception as e:
                print(f"Error guardando en Supabase: {e}")
        
    except Exception as e:
        error_msg = str(e)
        await update.message.reply_text(f"❌ Error: {error_msg[:200]}")
        print(f"Error procesando mensaje: {error_msg}")

def main():
    print("🤖 Iniciando JARVIS AX Bot de Telegram...")
    print(f"Token configurado: {'Sí' if TELEGRAM_TOKEN else 'No'}")
    print(f"DeepSeek configurado: {'Sí' if DEEPSEEK_API_KEY else 'No'}")
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Comandos
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('ayuda', help_command))
    app.add_handler(CommandHandler('estado', estado_command))
    app.add_handler(CommandHandler('vet', vet_command))
    app.add_handler(CommandHandler('legal', legal_command))
    app.add_handler(CommandHandler('dental', dental_command))
    
    # Mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot listo y escuchando mensajes...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
