# -*- coding: utf-8 -*-
import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI
import requests
import json

# Configuración
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
FISH_API_KEY = os.getenv('FISH_API_KEY')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Inicializar clientes
deepseek_client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url='https://api.deepseek.com')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🤖 JARVIS AX está operativo. ¿En qué puedo ayudarte?')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    
    # Verificar que sea el usuario autorizado
    if CHAT_ID and str(user_id) != CHAT_ID:
        return
    
    # Generar respuesta inteligente con DeepSeek
    try:
        response = deepseek_client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {'role': 'system', 'content': 'Eres JARVIS, un asistente IA avanzado y útil. Responde de forma concisa y profesional.'},
                {'role': 'user', 'content': user_message}
            ],
            max_tokens=500
        )
        jarvis_response = response.choices[0].message.content
        
        # Intentar generar audio con FISH
        try:
            fish_response = requests.post(
                'https://api.fish.audio/v1/tts',
                headers={
                    'Authorization': f'Bearer {FISH_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'text': jarvis_response,
                    'format': 'mp3'
                }
            )
            
            if fish_response.status_code == 200:
                # Enviar audio
                with open('temp_audio.mp3', 'wb') as f:
                    f.write(fish_response.content)
                await update.message.reply_audio('temp_audio.mp3')
                os.remove('temp_audio.mp3')
            else:
                # Si falla FISH, enviar texto
                await update.message.reply_text(jarvis_response)
                
        except Exception as e:
            print(f'Error generando audio: {e}')
            await update.message.reply_text(jarvis_response)
            
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print('🤖 Bot de JARVIS iniciado...')
    app.run_polling()

if __name__ == '__main__':
    main()
